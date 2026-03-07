# Java Knowledge Base

A comprehensive reference for Java developers covering core internals, modern features, enterprise patterns, and specialized topics. All examples use Java 17+ unless otherwise noted.

---

## Contents

- Part I: Core Java Mastery
- Part II: Modern Java Features
- Part III: Enterprise Java
- Part IV: Specialized Topics
- Part V: Interviews & Soft Skills
- Part VI: Cutting Edge & Future

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

**Section 7: Reflection & Dynamic Programming**
- Core Reflection API
- Annotations and annotation processing
- Proxy pattern and dynamic proxies
- Method handles and invokedynamic
- Metaprogramming techniques

---

### PART II: MODERN JAVA FEATURES

**Section 1: Java 8 - Lambdas & Streams**
- Lambda expressions deep dive
- Stream API fundamentals
- Advanced stream operations
- Parallel streams and performance
- Optional and null handling
- Method references and constructor references
- Functional interfaces in java.util.function
- Default and static methods in interfaces

**Section 2: Java 9-11 Features**
- Module system (Jigsaw)
- Collection factory methods
- Try-with-resources improvements
- Process API enhancements
- HTTP/2 Client API (Java 11)
- New String methods and compact strings

**Section 3: Java 12-17 Features**
- Switch expressions (Java 12-14)
- Text blocks (Java 13-15)
- Records (Java 14-16)
- Pattern matching for instanceof (Java 16)
- Sealed classes (Java 17)
- Helpful NullPointerExceptions (Java 14)
- New methods in core libraries

**Section 4: Java 18-21 Features**
- Virtual threads (Project Loom - Java 19-21)
- Pattern matching for switch (Java 21)
- Record patterns (Java 19-21)
- Sequenced collections (Java 21)
- String templates (preview)

**Section 5: Java 22-25 Features**
- Unnamed variables and patterns (Java 22)
- Statements before super() (Java 22)
- Foreign Function & Memory API (finalized Java 22)
- Structured concurrency (Java 23+)
- Scoped values (Java 23+)
- Class-file API (preview Java 22-23)
- String templates (second preview Java 23)
- Stream gatherers (Java 22-23)

**Section 6: JVM Languages & Interop**
 - Kotlin interoperability
- Scala interoperability
- Groovy in Java projects
- GraalVM and native images

**Section 7: Performance & Optimization**
- JMH (Java Microbenchmark Harness)
- Profiling techniques
- Memory optimization strategies
- CPU optimization techniques
- Lazy initialization patterns
- String optimization
- Collection performance tuning
- Caching strategies
- Async and non-blocking optimization
- JVM tuning for performance

---

### PART III: ENTERPRISE JAVA

**Section 1: Design Patterns in Java**
- Creational patterns
- Structural patterns
- Behavioral patterns
- Concurrency patterns
- Functional patterns
- Anti-patterns to avoid
- SOLID principles in Java
- DRY, KISS, YAGNI principles
- Dependency Injection patterns
- Resource management patterns
- Error handling patterns
- Testing patterns

**Section 2: Testing & Quality**
- JUnit 5 advanced features
- Mocking frameworks (Mockito, EasyMock)
- Testing best practices
- Integration testing strategies
- Property-based testing
- Mutation testing
- Test coverage analysis
- Performance testing

**Section 3: Build Tools & Dependency Management**
- Maven deep dive
- Gradle fundamentals
- Dependency management strategies
- Build optimization

**Section 4: Logging & Monitoring**
- Logging frameworks (SLF4J, Logback, Log4j2)
- Effective logging strategies
- Application monitoring
- Distributed tracing

**Section 5: Security in Java**
- Java Cryptography Architecture (JCA)
- Secure coding practices
- SSL/TLS in Java
- Java Security Manager (deprecated but important)
- Deserialization vulnerabilities
- Dependency vulnerabilities

**Section 6: Code Quality & Maintainability**
- Static analysis tools
- Code smells and refactoring
- Clean code principles
- Documentation strategies
- Code review best practices
- Technical debt management

---

## Contributing

Found an error, have a better example, or want to add a missing section? See the [Contributing Guide](../CONTRIBUTING.md).