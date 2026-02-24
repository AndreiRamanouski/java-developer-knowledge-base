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

### Section 2: Java Concurrency & Multithreading

**Thread creation and lifecycle**
- Thread vs Runnable vs Callable
- Thread states (NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED)
- Thread priorities and scheduling
- Daemon threads vs user threads
- Thread.sleep() vs Object.wait()
- Thread.join() and thread coordination
- Virtual threads (Project Loom - Java 19+)
- Executor framework and thread pools

**ThreadPoolExecutor parameters (corePoolSize, maximumPoolSize, keepAliveTime)**
- ExecutorService types (fixed, cached, single, scheduled)
- BlockingQueue implementations (LinkedBlockingQueue, ArrayBlockingQueue, SynchronousQueue)
- RejectedExecutionHandler strategies
- ForkJoinPool and work-stealing
- Custom thread factories
- Thread pool sizing formula
- CompletableFuture and async programming

**Creating CompletableFuture (supplyAsync, runAsync)**
- Chaining operations (thenApply, thenAccept, thenRun)
- Combining futures (thenCombine, thenCompose, allOf, anyOf)
- Exception handling (exceptionally, handle, whenComplete)
- Custom executors with CompletableFuture
- Avoiding blocking operations
- Real-world patterns
- Lock implementations (ReentrantLock, ReadWriteLock)

**Lock vs synchronized**
- ReentrantLock fairness
- tryLock() with timeout
- Condition variables
- ReadWriteLock for read-heavy scenarios
- StampedLock (optimistic reads)
- Lock-free algorithms
- Concurrent collections deep dive

**ConcurrentHashMap implementation (segments, buckets, CAS)**
- CopyOnWriteArrayList use cases
- BlockingQueue implementations comparison
- ConcurrentLinkedQueue (non-blocking)
- ConcurrentSkipListMap (sorted, concurrent)
- When to use each collection
- Performance benchmarks
- Atomic classes and CAS operations

**AtomicInteger, AtomicLong, AtomicReference**
- Compare-and-swap (CAS) algorithm
- ABA problem and AtomicStampedReference
- LongAdder vs AtomicLong (high contention)
- FieldUpdater for existing classes
- Building lock-free data structures
- Performance implications
- Synchronizers (CountDownLatch, CyclicBarrier, Semaphore, Phaser)

**CountDownLatch for one-time events**
- CyclicBarrier for recurring synchronization
- Semaphore for resource limiting
- Phaser for dynamic parties
- Exchanger for thread pairs
- Use case comparison
- Real-world examples
- ThreadLocal and context propagation

**ThreadLocal usage and patterns**
- InheritableThreadLocal for child threads
- ThreadLocal memory leaks (in thread pools)
- Context propagation in async code
- RequestContextHolder in Spring
- MDC (Mapped Diagnostic Context) in logging
- Cleaning up ThreadLocal
- Deadlock, livelock, and starvation

**Deadlock conditions (mutual exclusion, hold and wait, no preemption, circular wait)**
- Detecting deadlocks (jstack, VisualVM)
- Deadlock prevention strategies
- Livelock scenarios
- Thread starvation and fairness
- Dining philosophers problem
- Real-world deadlock debugging
- Memory models and concurrent programming patterns

**Java Memory Model (JMM)**
- Visibility, atomicity, ordering
- Safe publication patterns
- Producer-consumer pattern
- Thread-safe singleton patterns
- Immutability for concurrency
- Concurrent design principles
- Fork/Join framework

**RecursiveTask vs RecursiveAction**
- Work-stealing algorithm
- When to use Fork/Join vs ExecutorService
- Parallel streams implementation
- Common pitfalls (too many tasks, blocking)
- Performance tuning
- Real-world use cases
- Advanced concurrency patterns

**Double-checked locking (correct implementation)**
- Spin locks and busy waiting
- Lock striping (ConcurrentHashMap)
- Read-copy-update (RCU) pattern
- Disruptor pattern (LMAX)
- Actor model concepts
- Reactive programming paradigms

---

**Internal implementation of HashMap**
- Array + LinkedList/TreeNode structure
- Hash function and bucket selection
- Collision handling (chaining, treeify at threshold 8)
- Load factor and resizing (rehashing)
- Java 8+ improvements (balanced trees)
- equals() and hashCode() contract
- Common pitfalls and best practices
- TreeMap, LinkedHashMap, and specialized maps

**TreeMap (Red-Black tree implementation)**
- NavigableMap operations
- LinkedHashMap (insertion order, access order)
- LRU cache implementation
- WeakHashMap for cache scenarios
- IdentityHashMap (reference equality)
- EnumMap performance benefits
- ArrayList vs LinkedList - when to use each

**Internal structure comparison**
- Big O complexity analysis
- Random access vs sequential access
- Memory overhead
- Insertion/deletion performance
- Iterator performance
- Real-world decision criteria
- HashSet, TreeSet, LinkedHashSet internals

**HashSet backed by HashMap**
- TreeSet backed by TreeMap
- LinkedHashSet maintaining order
- Custom comparators and Comparable
- Set operations performance
- Choosing the right Set implementation
- Queue and Deque implementations

**PriorityQueue (heap implementation)**
- ArrayDeque vs LinkedList as Deque
- BlockingQueue for producer-consumer
- DelayQueue for scheduling
- TransferQueue semantics
- Choosing the right Queue
- Comparable vs Comparator

**Natural ordering with Comparable**
- Custom ordering with Comparator
- Comparator chaining (thenComparing)
- Comparator.comparing() method references
- Null handling in comparisons
- Sorting stability
- Performance considerations
- Collection performance and Big O analysis

**Time complexity for each operation**
- Space complexity considerations
- Amortized analysis (ArrayList resizing)
- Cache locality and memory access patterns
- Benchmarking collections (JMH)
- Choosing optimal data structure
- Immutable collections and defensive copying

**Collections.unmodifiableXXX()**
- List.of(), Set.of(), Map.of() (Java 9+)
- Guava ImmutableList, ImmutableMap
- Defensive copying strategies
- Performance of immutable collections
- When to use immutability

---

## Contributing

Found an error, have a better example, or want to add a missing section? See the [Contributing Guide](../CONTRIBUTING.md).