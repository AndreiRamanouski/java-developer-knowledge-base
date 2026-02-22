# Java Knowledge Base

A comprehensive reference for Java developers covering core internals, modern features, enterprise patterns, and specialized topics. All examples use Java 17+ unless otherwise noted.

---

## Contents

- Part I: Core Java Mastery
- Part II: Modern Java Features
- Part III: Enterprise Java
- Part IV: Specialized Topics

---

## Part I: Core Java Mastery

### Section 1: Java Memory Model & Internals

**JVM memory architecture deep dive**
- Heap (Young Gen, Old Gen, Metaspace)
- Stack memory (thread-local)
- Method area and constant pool
- Direct memory and off-heap
- Memory allocation strategies
- Escape analysis and stack allocation
- String pool internals (heap vs constant pool)
- Garbage collection algorithms and tuning

**Serial, Parallel, CMS, G1GC, ZGC, Shenandoah**
- GC phases: mark, sweep, compact
- Stop-the-world pauses
- Generational hypothesis
- GC tuning parameters (-Xms, -Xmx, -XX:NewRatio)
- GC logs analysis
- When to choose which GC
- Object lifecycle and memory leaks

**Object creation (new, reflection, cloning, deserialization)**
- Object initialization order
- Reachability and finalization
- Weak, Soft, Phantom references
- Memory leak patterns (listeners, caches, ThreadLocal)
- Heap dump analysis (MAT, VisualVM)
- Preventing memory leaks
- ClassLoader hierarchy and mechanism

**Bootstrap, Extension, Application classloaders**
- Parent delegation model
- Custom classloaders
- Class loading phases (loading, linking, initialization)
- ClassNotFoundException vs NoClassDefFoundError
- OSGi and modular classloading
- Hot reloading and class unloading
- Java bytecode and JIT compilation

**Bytecode structure and instructions**
- javap for bytecode inspection
- JIT (C1, C2 compilers)
- Tiered compilation
- Inlining and method compilation
- Deoptimization scenarios
- JVM intrinsics
- Volatile, synchronized, and happens-before

**Memory visibility problems**
- volatile semantics (read/write barriers)
- synchronized implementation (monitor, biased locking)
- happens-before relationship
- Lock coarsening and lock elision
- Double-checked locking (broken without volatile)
- Performance implications
- Object layout and memory overhead

**Object header (mark word, class pointer)**
- Field alignment and padding
- Compressed oops (-XX:+UseCompressedOops)
- Array object layout
- Memory footprint calculation
- JOL (Java Object Layout) tool
- Memory optimization techniques
- Stack vs heap allocation

**When objects go to stack (escape analysis)**
- Scalar replacement
- Stack frame structure
- StackOverflowError causes and prevention
- Thread stack sizing (-Xss)
- Stack unwinding and exception handling
- Performance comparison
- Native memory and DirectByteBuffer

**Native memory vs heap memory**
- DirectByteBuffer allocation and cleanup
- Memory-mapped files (MappedByteBuffer)
- Native memory leaks
- Off-heap caching (Ehcache, Chronicle Map)
- sun.misc.Unsafe usage (deprecated)
- Foreign Memory Access API (JEP 393)
- JVM flags and performance tuning

**Diagnostic flags (-XX:+PrintFlagsFinal)**
- Heap sizing recommendations
- GC tuning for throughput vs latency
- JIT compiler flags
- Profiling with JFR (Java Flight Recorder)
- Monitoring with JMX
- Production troubleshooting checklist

---

## Contributing

Found an error, have a better example, or want to add a missing section? See the [Contributing Guide](../CONTRIBUTING.md).