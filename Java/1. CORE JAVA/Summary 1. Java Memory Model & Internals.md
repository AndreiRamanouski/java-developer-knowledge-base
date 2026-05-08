
# 1. Java Memory Model & Internals

---

## Summary

### Key Takeaways

**Heap Memory:**

- Young Gen: Eden (new objects) + Survivor (survived GC)
- Old Gen: Long-lived objects
- Metaspace: Class metadata, static variables
- Minor GC fast, Major GC slow

**Stack Memory:**

- One per thread
- Stores primitives and references
- Method call frames
- LIFO structure

**Direct Memory:**

- Off-heap, native memory
- Faster I/O
- Manual management
- Not GC'd

**Optimizations:**

- TLAB: Fast thread-local allocation
- Escape Analysis: Stack allocation possible
- Scalar Replacement: Eliminate object creation
- Lock Elision: Remove unnecessary locks

**String Pool:**

- In heap (Java 7+)
- Reuses string literals
- intern() for manual pooling
- String deduplication with G1 GC

### Memory Tuning Flags

```bash
# Heap sizes
-Xms2g                    # Initial heap
-Xmx4g                    # Maximum heap
-Xmn1g                    # Young generation size

# Metaspace
-XX:MetaspaceSize=128m    # Initial metaspace
-XX:MaxMetaspaceSize=512m # Maximum metaspace

# Stack size
-Xss512k                  # Stack size per thread

# Direct memory
-XX:MaxDirectMemorySize=1g

# GC options
-XX:NewRatio=2            # Old/Young ratio
-XX:SurvivorRatio=8       # Eden/Survivor ratio
-XX:MaxTenuringThreshold=15 # GCs before promotion

# String pool
-XX:StringTableSize=100000

# TLAB
-XX:+UseTLAB
-XX:TLABSize=256k

# Escape analysis
-XX:+DoEscapeAnalysis
-XX:+EliminateAllocations

# String deduplication
-XX:+UseG1GC
-XX:+UseStringDeduplication
```

---

# 2. Java Garbage Collection Algorithms and Tuning


## Summary

### Quick Reference

```bash
# Serial GC (small heaps, single CPU)
-XX:+UseSerialGC -Xms512m -Xmx512m

# Parallel GC (throughput, batch processing)
-XX:+UseParallelGC -Xms4g -Xmx4g -XX:GCTimeRatio=99

# G1 GC (general purpose, low latency)
-XX:+UseG1GC -Xms8g -Xmx8g -XX:MaxGCPauseMillis=200

# ZGC (ultra-low latency, large heaps)
-XX:+UseZGC -Xms32g -Xmx32g

# Shenandoah GC (ultra-low latency, alternative to ZGC)
-XX:+UseShenandoahGC -Xms32g -Xmx32g

# Enable GC logging
-Xlog:gc*:file=gc.log:time,uptime,level,tags
```

### Key Takeaways

**Generational Hypothesis:**

- Most objects die young
- Focus GC on young generation
- Collect young gen frequently, old gen rarely

**GC Phases:**

- Mark: Find live objects
- Sweep: Reclaim dead object memory
- Compact: Eliminate fragmentation

**Collector Choice:**

- Small heap → Serial GC
- Throughput → Parallel GC
- Low latency → G1 GC
- Ultra-low latency → ZGC/Shenandoah

**Tuning Goals:**

- Minimize pause times
- Maximize throughput
- Reduce GC frequency
- Avoid Full GCs

### Common Issues and Solutions

|Issue|Symptom|Solution|
|---|---|---|
|Frequent Young GCs|GC every 1-2s|Increase Young Gen size|
|Long Young GC pauses|Pauses > 100ms|Increase Survivor space|
|Frequent Full GCs|Full GC every few minutes|Increase heap or fix memory leak|
|Long Full GC pauses|Pauses > 1s|Switch to low-latency GC|
|High GC overhead|>10% time in GC|Increase heap or optimize code|
|Allocation failures|OutOfMemoryError|Increase heap size|

---

# 3. Java Object Lifecycle and Memory Leaks


## Summary

### Object Lifecycle

```java
/**
 * COMPLETE OBJECT LIFECYCLE:
 * 
 * 1. Creation:
 *    - new keyword
 *    - Reflection
 *    - Cloning
 *    - Deserialization
 * 
 * 2. Initialization:
 *    - Static initializers (class loading)
 *    - Instance initializers
 *    - Constructor chain (parent → child)
 * 
 * 3. Usage:
 *    - Strongly reachable
 *    - Accessed via references
 * 
 * 4. Reachability Change:
 *    - Softly reachable (memory-sensitive)
 *    - Weakly reachable (next GC)
 *    - Phantom reachable (post-finalization)
 * 
 * 5. Finalization (deprecated):
 *    - finalize() called
 *    - Can resurrect object
 * 
 * 6. Cleanup:
 *    - Cleaner runs (Java 9+)
 *    - Native resources released
 * 
 * 7. Reclamation:
 *    - Memory returned to heap
 *    - Available for new objects
 */
```

### Memory Leak Patterns Summary

|Pattern|Symptom|Heap Dump|Fix|
|---|---|---|---|
|**Listener Leak**|Growing ArrayList|Large ArrayList of listeners|Remove listeners or use WeakReference|
|**Cache Leak**|Growing HashMap|Large HashMap with many entries|Add size limit or TTL|
|**ThreadLocal Leak**|Memory per thread|ThreadLocalMap with large entries|Call ThreadLocal.remove()|
|**ClassLoader Leak**|Multiple class versions|Multiple ClassLoader instances|Clean up ThreadLocal and listeners|
|**Static Collection**|Constant memory growth|Static field with large collection|Use instance field or bound size|
|**Inner Class Leak**|Outer object not GC'd|Inner class holds outer reference|Use static inner class|
|**Stream Leak**|File handle exhaustion|Open streams in dominator tree|Use try-with-resources|

### Tools Comparison

|Tool|Best For|Learning Curve|Features|
|---|---|---|---|
|**Eclipse MAT**|Deep analysis|Medium|Leak suspects, OQL, dominator tree|
|**VisualVM**|Live monitoring|Low|Real-time charts, profiling|
|**JProfiler**|Professional use|High|Advanced profiling, comparison|
|**YourKit**|Production analysis|High|CPU/memory profiling, telemetry|
|**jmap/jhat**|Quick checks|Low|Command-line, basic analysis|

### Quick Reference

```bash
# Take heap dump
jcmd <pid> GC.heap_dump heap.hprof

# Analyze with jhat (built-in)
jhat heap.hprof
# Open http://localhost:7000

# Find memory leaks (Linux)
jmap -histo:live <pid> | head -20

# Monitor memory in real-time
jstat -gcutil <pid> 1000
```

---

# 4. Java ClassLoader Hierarchy and Mechanism


## Summary

### ClassLoader Hierarchy

```
Bootstrap ClassLoader (null)
    ↓ parent
Platform/Extension ClassLoader
    ↓ parent
Application ClassLoader
    ↓ parent
Custom ClassLoaders
```

### Parent Delegation Flow

```
1. Check if already loaded (cache)
2. Delegate to parent ClassLoader
3. If parent can't load, try self
4. If still can't load, throw ClassNotFoundException
```

### Class Loading Phases

```
1. LOADING
   - Locate .class file
   - Read bytes
   - defineClass()
   
2. LINKING
   a. Verification: Verify bytecode
   b. Preparation: Allocate statics (default values)
   c. Resolution: Resolve symbolic references
   
3. INITIALIZATION
   - Execute static initializers
   - Set explicit values
```

### Key Differences

|Aspect|ClassNotFoundException|NoClassDefFoundError|
|---|---|---|
|Type|Exception (checked)|Error (unchecked)|
|When|Explicit loading|Implicit loading|
|Cause|Class not found|Was found, now missing or init failed|
|Can catch|Yes|No (shouldn't)|
|Recovery|Possible|Difficult|

### Common Issues

|Issue|Cause|Solution|
|---|---|---|
|ClassNotFoundException|Wrong classpath|Add to classpath|
|NoClassDefFoundError|Missing dependency|Include all dependencies|
|ClassCastException|Same class, different ClassLoaders|Use single ClassLoader|
|LinkageError|Class loaded twice|Check ClassLoader hierarchy|
|Memory leak|ClassLoader not GC'd|Clear all references|

### Best Practices

1. **Use parent delegation** (don't break unless necessary)
2. **Override findClass()** (not loadClass())
3. **Clean up resources** (close ClassLoaders)
4. **Avoid static references** (prevent leaks)
5. **Monitor with -verbose:class**
6. **Use try-with-resources** (URLClassLoader implements Closeable)
7. **Test hot reloading** (watch for memory leaks)

---

# 5. Java Bytecode and JIT Compilation


## Summary

### Bytecode Quick Reference

```
LOAD:     iload, lload, fload, dload, aload
STORE:    istore, lstore, fstore, dstore, astore
ARITHMETIC: iadd, isub, imul, idiv, irem, ineg
COMPARISON: ifeq, ifne, iflt, ifle, ifgt, ifge
INVOKE:   invokevirtual, invokespecial, invokestatic, invokeinterface
OBJECTS:  new, newarray, anewarray, getfield, putfield
CONTROL:  goto, if_icmp*, return, ireturn
STACK:    dup, pop, swap
```

### JIT Compilation Levels

|Level|Name|Compiler|Profiling|Optimizations|Use Case|
|---|---|---|---|---|---|
|0|Interpreter|None|Yes|None|Startup|
|1|C1 Simple|C1|No|Basic|Quick compile|
|2|C1 Limited|C1|Limited|Basic|Rarely used|
|3|C1 Full|C1|Full|Basic|Collect profile|
|4|C2|C2|No|Aggressive|Peak performance|

### Key Performance Concepts

1. **Tiered Compilation**: Combines fast startup (C1) with peak performance (C2)
2. **Inlining**: Eliminates method call overhead, enables further optimizations
3. **Escape Analysis**: Scalar replacement, lock elision, stack allocation
4. **Deoptimization**: Falls back to interpreter when assumptions invalid
5. **Intrinsics**: Hand-optimized native implementations of critical methods

### Optimization Checklist

- ✅ Keep hot methods small (< 35 bytes)
- ✅ Use final methods/classes when possible
- ✅ Avoid megamorphic call sites
- ✅ Profile before optimizing
- ✅ Let JIT do its job (don't micro-optimize)
- ✅ Use intrinsic methods (Math, System.arraycopy, etc.)
- ✅ Maintain type stability (avoid deoptimization)

### JVM Flags Reference

```bash
# Compilation monitoring
-XX:+PrintCompilation          # Show compilations
-XX:+PrintInlining              # Show inlining decisions
-XX:+LogCompilation             # Detailed XML log

# Compilation control
-XX:+TieredCompilation          # Enable tiered (default)
-XX:TieredStopAtLevel=N         # Stop at level N
-XX:CompileThreshold=N          # C2 threshold (default: 10000)

# Inlining control
-XX:MaxInlineSize=N             # Max inline size (default: 35)
-XX:FreqInlineSize=N            # Hot method size (default: 325)

# Deoptimization monitoring
-XX:+PrintDeoptimization        # Show deoptimization
-XX:+TraceDeoptimization        # Detailed deopt info
```

---

# 6. Java Volatile, Synchronized, and Happens-Before


## Summary

### Key Concepts

**Memory Visibility:**

- Each thread has CPU cache
- Without synchronization, changes may not be visible
- Requires volatile or synchronized

**Volatile:**

- Guarantees visibility and ordering
- Read/write are atomic
- NOT atomic for compound operations (++, +=)
- Memory barriers prevent reordering
- Faster than synchronized

**Synchronized:**

- Provides mutual exclusion
- Guarantees visibility (like volatile)
- Uses monitor locks
- Three states: Biased, Lightweight, Heavyweight
- JIT optimizations: Lock coarsening, lock elision

**Happens-Before:**

- Defines visibility and ordering guarantees
- Key rules: Program order, monitor lock, volatile, thread start/join
- Use transitivity to build chains

**Double-Checked Locking:**

- Broken without volatile
- Requires volatile for correctness
- Better alternatives: Holder class idiom, enum singleton

### Performance Characteristics

|Operation|Single-Threaded|Multi-Threaded|Notes|
|---|---|---|---|
|Normal field|1ns|N/A|Not thread-safe|
|Volatile read|5-10ns|5-10ns|Thread-safe reads|
|Volatile write|10-20ns|10-20ns|Thread-safe writes|
|Synchronized (uncontended)|25-50ns|25-50ns|Biased locking|
|Synchronized (contended)|N/A|1000+ns|Context switch|
|AtomicInteger|20ns|50-200ns|CAS operations|
|ConcurrentHashMap|Varies|Fast|Lock striping|

### Best Practices

**Synchronization:**

- ✅ Use synchronized for mutual exclusion
- ✅ Use volatile for visibility only (no compound ops)
- ✅ Keep critical sections small
- ✅ Use concurrent collections when possible
- ✅ Consider ReadWriteLock for read-heavy workloads
- ✅ Profile before optimizing

**Correctness:**

- ✅ Always use volatile with double-checked locking
- ✅ Establish happens-before relationships
- ✅ Acquire locks in consistent order (avoid deadlock)
- ✅ Prefer immutability when possible
- ✅ Use java.util.concurrent over manual synchronization

**Performance:**

- ✅ Measure with JMH
- ✅ Profile with VisualVM or Flight Recorder
- ✅ Trust JIT optimizations (lock elision, coarsening)
- ✅ Don't prematurely optimize
- ✅ Use AtomicInteger over synchronized int

### Common Pitfalls

**❌ Volatile without understanding limitations:**

```java
private volatile int counter = 0;
public void increment() {
    counter++;  // NOT ATOMIC! Data race!
}
```

**❌ Double-checked locking without volatile:**

```java
private static Resource instance;  // Missing volatile!
public static Resource getInstance() {
    if (instance == null) {
        synchronized(...) {
            if (instance == null) {
                instance = new Resource();  // Broken!
            }
        }
    }
    return instance;
}
```

**❌ Inconsistent lock ordering:**

```java
// Thread 1: lock(A); lock(B);
// Thread 2: lock(B); lock(A);  // DEADLOCK!
```

### JVM Flags Reference

```bash
# Lock monitoring
-XX:+PrintBiasedLockingStatistics
-XX:+PrintEliminateAllocations
-XX:+PrintEliminateLocks

# Lock configuration
-XX:+UseBiasedLocking           # Enable biased locking (default in Java 8-14)
-XX:-UseBiasedLocking           # Disable biased locking
-XX:BiasedLockingStartupDelay=0 # Enable biased locking immediately

# Profiling
-XX:+UnlockDiagnosticVMOptions
-XX:+LogCompilation
```

---

# 7. Java Object Layout and Memory Overhead


## Summary

### Key Concepts

**Object Header:**

- Mark word: 8 bytes (hash, age, lock state)
- Class pointer: 4 bytes (compressed) or 8 bytes
- Total: 12-16 bytes per object

**Field Alignment:**

- Fields ordered by size: long (8) → int/float (4) → short/char (2) → byte/boolean (1)
- Objects aligned to 8-byte boundary
- Padding fills gaps

**Compressed Oops:**

- Reduces references from 8 to 4 bytes
- Works for heaps < 32GB
- 40% memory savings for reference-heavy code
- Enabled by default

**Arrays:**

- Additional 4-byte length field
- Minimum 16 bytes (empty array)
- Element alignment by type
- Multi-dimensional = nested arrays (high overhead)

**Memory Overhead:**

- Empty object: 16 bytes
- Object with one int: 24 bytes (50% overhead)
- Object with 8 bytes data: 32 bytes (75% efficiency)

### Size Quick Reference

|Type|Size (bytes)|Example|
|---|---|---|
|boolean, byte|1|boolean flag|
|short, char|2|short count|
|int, float|4|int value|
|long, double|8|long timestamp|
|reference (compressed)|4|Object ref|
|reference (uncompressed)|8|Object ref|
|Object header (compressed)|12|mark + klass|
|Object header (uncompressed)|16|mark + klass|
|Array header (compressed)|16|header + length|

### Optimization Techniques

**Best Practices:**

1. ✅ Use primitive arrays over object arrays (75% savings)
2. ✅ Pack booleans into bytes/ints (87% savings)
3. ✅ Pool immutable objects (99% savings)
4. ✅ Intern duplicate strings (99% savings)
5. ✅ Use primitive collections (63% savings)
6. ✅ Avoid boxing in hot paths (75% savings)
7. ✅ Consider struct-of-arrays layout (27% savings + performance)
8. ✅ Store timestamps as long (87% savings)
9. ✅ Use enums over strings (93% savings)
10. ✅ Keep heap < 32GB for compressed oops

**JOL Commands:**

```java
// Single object
ClassLayout.parseInstance(obj).toPrintable()

// Object graph
GraphLayout.parseInstance(obj).toPrintable()
GraphLayout.parseInstance(obj).totalSize()
GraphLayout.parseInstance(obj).toFootprint()

// VM info
VM.current().details()
```

**JVM Flags:**

```bash
# Compressed oops
-XX:+UseCompressedOops          # Enable (default if heap < 32GB)
-XX:-UseCompressedOops          # Disable
-XX:+PrintCompressedOopsMode    # Print compression mode

# Compressed class pointers
-XX:+UseCompressedClassPointers # Enable (default)
-XX:CompressedClassSpaceSize=1g # Set class space size

# Object alignment
-XX:ObjectAlignmentInBytes=8    # Set alignment (default 8)

# Debugging
-XX:+PrintFlagsFinal            # Print all flags
java -XX:+PrintFlagsFinal -version | grep Compressed
```

### Common Pitfalls

**❌ Using Object arrays for primitives:**

```java
Integer[] arr = new Integer[1000];  // 16KB
int[] arr = new int[1000];          // 4KB (75% savings!)
```

**❌ Many boolean fields:**

```java
class Flags {
    boolean f1, f2, f3, f4, f5, f6, f7, f8;  // 8 bytes + overhead
}
// Better: byte flags = 0; // 1 byte, use bitwise operations
```

**❌ Heap > 32GB without consideration:**

```java
// -Xmx40g → Compressed oops OFF → 50% more memory for references!
// Better: Use multiple JVMs or accept the cost
```

**❌ Ignoring alignment:**

```java
class Bad {
    byte b1; long l1; byte b2; long l2;  // 40 bytes (padding)
}
class Good {
    long l1, l2; byte b1, b2;            // 40 bytes (but JVM reorders anyway)
}
```

---

# 8. Java Stack vs Heap Allocation


### Best Practices

**Optimization:**

1. ✅ Keep objects local when possible (enable escape analysis)
2. ✅ Use primitives instead of objects in hot paths
3. ✅ Avoid unnecessary object creation in loops
4. ✅ Let JIT do its job (avoid premature manual optimization)
5. ✅ Profile before optimizing

**Stack Management:**

1. ✅ Prefer iteration over recursion
2. ✅ Add depth limits to recursive algorithms
3. ✅ Size stacks based on application needs
4. ✅ Monitor thread count vs stack size trade-off
5. ✅ Test with realistic workloads

**Exception Handling:**

1. ✅ Never use exceptions for flow control
2. ✅ Catch specific exceptions, not `Exception`
3. ✅ Avoid throwing in hot paths
4. ✅ Keep stack traces shallow when possible
5. ✅ Consider error codes or Optional for frequent errors

### Common Pitfalls

**❌ Assuming all objects are heap-allocated:**

```java
// This might be stack-allocated or scalar replaced:
Point p = new Point(1, 2);
return p.x + p.y;
```

**❌ Disabling escape analysis:**

```java
// Don't do this unless you have a very good reason:
-XX:-DoEscapeAnalysis
```

**❌ Infinite recursion:**

```java
public void recurse() {
    recurse();  // StackOverflowError!
}
```

**❌ Using exceptions for flow control:**

```java
// Bad: 10,000x slower than if-check
try {
    return map.get(key);
} catch (NullPointerException e) {
    return defaultValue;
}
```

---

# 9. Java Native Memory and DirectByteBuffer

## Summary

### Key Concepts

**Native vs Heap Memory:**

- Heap: GC-managed, automatic, safer, GC pauses
- Native: Manual, larger allocations, no GC, faster for I/O

**DirectByteBuffer:**

- Wrapper around native memory
- Automatic cleanup via Cleaner (delayed)
- Manual cleanup recommended for large buffers
- Limited by -XX:MaxDirectMemorySize

**Memory-Mapped Files:**

- OS maps file to memory
- Fast random access (10x faster than traditional I/O)
- Ideal for large files (>1GB)
- Inter-process communication

**Off-Heap Caching:**

- Ehcache: Tiered (heap/off-heap/disk), automatic
- Chronicle Map: Lock-free, persistent, predictable

**Foreign Memory API:**

- Modern replacement for Unsafe
- Type-safe, automatic cleanup, better performance
- Arena-based lifecycle management
- FFI for native calls

### Performance Characteristics

|Operation|Heap|DirectBuffer|Foreign API|Mapped File|
|---|---|---|---|---|
|Sequential write|2 ns|4 ns|3 ns|3 ns|
|Sequential read|1 ns|2 ns|1.5 ns|1.5 ns|
|Random access|3 ns|5 ns|4 ns|10 ns|
|Allocation|10 ns|1000 ns|500 ns|10000 ns|
|GC impact|High|None|None|None|

### Use Case Guide

**Use Heap When:**

- Data < 1GB
- Short-lived objects
- GC pauses acceptable
- Normal application objects

**Use DirectByteBuffer When:**

- I/O operations (NIO)
- Network buffers
- Medium-sized data (10MB-1GB)
- JDK < 14

**Use Foreign Memory API When:**

- JDK 19+
- Type safety important
- Better performance needed
- Native library integration

**Use Memory-Mapped Files When:**

- Large files (>1GB)
- Random access patterns
- Inter-process communication
- File-backed data

**Use Off-Heap Caching When:**

- Cache > 1GB
- GC pauses unacceptable
- Low latency required
- Persistence needed

### JVM Flags Reference

```bash
# Direct memory limits
-XX:MaxDirectMemorySize=2g          # Max direct buffer memory

# Native memory tracking
-XX:NativeMemoryTracking=summary    # Enable tracking (summary)
-XX:NativeMemoryTracking=detail     # Enable tracking (detail)

# Then use:
jcmd <pid> VM.native_memory summary
jcmd <pid> VM.native_memory detail

# Monitoring
jcmd <pid> GC.heap_info             # Heap info
jcmd <pid> VM.info                  # VM info

# Java 17+ Unsafe access
--add-exports java.base/sun.misc=ALL-UNNAMED
--add-exports java.base/jdk.internal.ref=ALL-UNNAMED
```

### Best Practices

**DirectByteBuffer:**

1. ✅ Always clean large buffers manually
2. ✅ Use try-with-resources pattern
3. ✅ Set -XX:MaxDirectMemorySize
4. ✅ Monitor native memory growth
5. ✅ Pool buffers when possible

**Memory-Mapped Files:**

1. ✅ Use for large files (>100MB)
2. ✅ Always close FileChannel
3. ✅ Call force() for critical writes
4. ✅ Consider OS page cache size
5. ✅ Test on target platform

**Off-Heap Caching:**

1. ✅ Use tiered caching (heap + off-heap)
2. ✅ Size appropriately
3. ✅ Monitor hit rates
4. ✅ Measure serialization overhead
5. ✅ Consider Chronicle Map for >10GB

**Foreign Memory API:**

1. ✅ Use Arena.ofConfined() by default
2. ✅ Prefer Foreign API over Unsafe
3. ✅ Use ValueLayout for type safety
4. ✅ Leverage try-with-resources
5. ✅ Test thoroughly (newer API)

### Common Pitfalls

**❌ Forgetting to clean DirectByteBuffer:**

```java
ByteBuffer buffer = ByteBuffer.allocateDirect(1024 * 1024);
// LEAK: Never cleaned, waits for GC
```

**❌ Not closing FileChannel:**

```java
FileChannel channel = file.getChannel();
MappedByteBuffer buffer = channel.map(...);
// LEAK: Channel never closed
```

**❌ Exceeding MaxDirectMemorySize:**

```java
// -XX:MaxDirectMemorySize=1g
ByteBuffer buffer = ByteBuffer.allocateDirect(2_000_000_000);
// OutOfMemoryError: Direct buffer memory
```

**❌ Using Unsafe in new code:**

```java
Unsafe.allocateMemory(1024);  // DEPRECATED, will be removed
// Use Foreign Memory API instead
```

---

# 10. JVM Flags and Performance Tuning

## Summary

### Flag Categories Quick Reference

```bash
# HEAP SIZING
-Xms<size>                          # Initial heap
-Xmx<size>                          # Maximum heap
-Xmn<size>                          # Young generation size
-XX:MaxRAMPercentage=75.0           # Heap as % of RAM

# GC SELECTION
-XX:+UseSerialGC                    # Serial GC (single thread)
-XX:+UseParallelGC                  # Parallel GC (throughput)
-XX:+UseG1GC                        # G1 GC (balanced, default)
-XX:+UseZGC                         # ZGC (ultra-low latency)
-XX:+UseShenandoahGC                # Shenandoah (low latency)

# GC TUNING
-XX:MaxGCPauseMillis=200            # Pause time goal
-XX:GCTimeRatio=19                  # Throughput goal (5% GC)
-XX:ParallelGCThreads=8             # Parallel GC threads
-XX:ConcGCThreads=2                 # Concurrent GC threads

# JIT COMPILATION
-XX:+TieredCompilation              # Tiered compilation (default)
-XX:CompileThreshold=10000          # C2 compilation threshold
-XX:ReservedCodeCacheSize=512m      # Code cache size

# DIAGNOSTIC
-XX:+HeapDumpOnOutOfMemoryError     # Dump heap on OOM
-XX:HeapDumpPath=/var/dumps         # Dump location
-XX:+ExitOnOutOfMemoryError         # Exit on OOM
-XX:StartFlightRecording=...        # Enable JFR

# LOGGING
-Xlog:gc*:file=gc.log:time          # GC logging
-XX:+PrintFlagsFinal                # Print all flags
-XX:+PrintCommandLineFlags          # Print modified flags

# JMX
-Dcom.sun.management.jmxremote                  # Enable JMX
-Dcom.sun.management.jmxremote.port=9010        # JMX port
-Dcom.sun.management.jmxremote.authenticate=true # Auth required
```

### Performance Tuning Priorities

**Priority 1: Correctness**

1. No OutOfMemoryErrors under load
2. No deadlocks or livelocks
3. Stable under sustained traffic
4. Recovers from errors

**Priority 2: Meets SLAs**

1. Latency within targets (P50, P99, P99.9)
2. Throughput meets requirements
3. GC pauses acceptable
4. Resource usage reasonable

**Priority 3: Optimization**

1. Reduce allocation rate
2. Tune GC parameters
3. Optimize hot code paths
4. Improve cache hit rates

### Common Issues and Solutions

|Issue|Symptoms|Solution|
|---|---|---|
|High heap usage|Heap >80%, frequent GC|Increase heap or fix memory leak|
|Long GC pauses|Pauses >1s|Lower pause goal, increase heap, tune GC|
|Frequent GC|GC >1/sec|Increase young gen, reduce allocation|
|OOM|Application crashes|Analyze heap dump, fix leak, increase heap|
|High CPU|CPU >80%|Profile with JFR, optimize hot methods|
|Thread contention|Slow performance|Thread dump, reduce lock scope|
|Slow startup|Minutes to start|Reduce classpath, use AOT, CDS|

### Monitoring Metrics

**Critical Metrics (Alert):**

- Heap usage >80%
- GC pause >1 second
- GC frequency >1/second
- OOM errors
- Thread deadlocks

**Important Metrics (Track):**

- Average GC pause time
- GC throughput (% time in GC)
- Allocation rate
- Thread count
- CPU usage
- Response time (P50, P99, P99.9)

**Nice-to-Have Metrics:**

- Code cache usage
- Metaspace usage
- Compilation time
- Safepoint time
- Direct buffer usage

---
