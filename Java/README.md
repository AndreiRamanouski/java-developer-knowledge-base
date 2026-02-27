# Java Knowledge Base

A comprehensive reference for Java developers covering core internals, modern features, enterprise patterns, and specialized topics. All examples use Java 17+ unless otherwise noted.

---

## Contents

- Part I: Core Java Mastery
- Part II: Modern Java Features
- Part III: Enterprise Java
- Part IV: Specialized Topics

---

### Part I: Core Java Mastery

**Section 1: Java Memory Model & Internals**
- JVM memory architecture deep dive
- Serial, Parallel, CMS, G1GC, ZGC, Shenandoah
- Object creation (new, reflection, cloning, deserialization)
- Bootstrap, Extension, Application classloaders
- Bytecode structure and instructions
- Memory visibility problems
- Object header (mark word, class pointer)
- When objects go to stack (escape analysis)
- Native memory vs heap memory
- Diagnostic flags (-XX:+PrintFlagsFinal)

**Section 2: Java Concurrency & Multithreading**
- Thread creation and lifecycle
- ThreadPoolExecutor parameters (corePoolSize, maximumPoolSize, keepAliveTime)
- Creating CompletableFuture (supplyAsync, runAsync)
- Lock vs synchronized
- ConcurrentHashMap implementation (segments, buckets, CAS)
- AtomicInteger, AtomicLong, AtomicReference
- CountDownLatch for one-time events
- ThreadLocal usage and patterns
- Deadlock conditions (mutual exclusion, hold and wait, no preemption, circular wait)
- Java Memory Model (JMM)
- RecursiveTask vs RecursiveAction
- Double-checked locking (correct implementation)

**Section 3: Collections Framework**
- Internal implementation of HashMap
- TreeMap (Red-Black tree implementation)
- Internal structure comparison
- HashSet backed by HashMap
- PriorityQueue (heap implementation)
- Natural ordering with Comparable
- Time complexity for each operation
- Collections.unmodifiableXXX()

**Section 4: Generics & Type System**
- Generics fundamentals and type erasure
- Upper bounds (extends)
- Type inference in method calls
- Type tokens and TypeReference
- Arrays are covariant (ArrayStoreException risk)
- Recursive type bounds (Enum<E extends Enum<E>>)

**Section 5: Exception Handling & Error Management**
- Exception hierarchy and best practices
- Automatic resource management
- Catching Exception or Throwable
- CompletableFuture exception handling

**Section 6: I/O, NIO, and Serialization**
- Traditional I/O vs NIO vs NIO.2
- Path vs File
- Java serialization (Serializable)
- Jackson for JSON
- Socket and ServerSocket

---

## Contributing

Found an error, have a better example, or want to add a missing section? See the [Contributing Guide](../CONTRIBUTING.md).