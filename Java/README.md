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

**JVM Memory Architecture**
- Heap (Young Gen, Old Gen, Metaspace)
- Stack memory (thread-local)
- Method area and constant pool
- Direct memory and off-heap
- Memory allocation strategies
- Escape analysis and stack allocation
- String pool internals (heap vs constant pool)

**Garbage Collection Algorithms and Tuning**
- Serial, Parallel, CMS, G1GC, ZGC, Shenandoah
- GC phases: mark, sweep, compact
- Stop-the-world pauses
- Generational hypothesis
- GC tuning parameters (-Xms, -Xmx, -XX:NewRatio)
- GC logs analysis
- When to choose which GC

**Object Lifecycle and Memory Leaks**
- Object creation (new, reflection, cloning, deserialization)
- Object initialization order
- Reachability and finalization
- Weak, Soft, Phantom references
- Memory leak patterns (listeners, caches, ThreadLocal)
- Heap dump analysis (MAT, VisualVM)
- Preventing memory leaks

**ClassLoader Hierarchy and Mechanism**
- Bootstrap, Extension, Application classloaders
- Parent delegation model
- Custom classloaders
- Class loading phases (loading, linking, initialization)
- ClassNotFoundException vs NoClassDefFoundError
- OSGi and modular classloading
- Hot reloading and class unloading

**Java Bytecode and JIT Compilation**
- Bytecode structure and instructions
- javap for bytecode inspection
- JIT (C1, C2 compilers)
- Tiered compilation
- Inlining and method compilation
- Deoptimization scenarios
- JVM intrinsics

**Volatile, Synchronized, and Happens-Before**
- Memory visibility problems
- volatile semantics (read/write barriers)
- synchronized implementation (monitor, biased locking)
- happens-before relationship
- Lock coarsening and lock elision
- Double-checked locking (broken without volatile)
- Performance implications

**Object Layout and Memory Overhead**
- Object header (mark word, class pointer)
- Field alignment and padding
- Compressed oops (-XX:+UseCompressedOops)
- Array object layout
- Memory footprint calculation
- JOL (Java Object Layout) tool
- Memory optimization techniques

**Stack vs Heap Allocation**
- When objects go to stack (escape analysis)
- Scalar replacement
- Stack frame structure
- StackOverflowError causes and prevention
- Thread stack sizing (-Xss)
- Stack unwinding and exception handling
- Performance comparison

**Native Memory and DirectByteBuffer**
- Native memory vs heap memory
- DirectByteBuffer allocation and cleanup
- Memory-mapped files (MappedByteBuffer)
- Native memory leaks
- Off-heap caching (Ehcache, Chronicle Map)
- sun.misc.Unsafe usage (deprecated)
- Foreign Memory Access API (JEP 393)

**JVM Flags and Performance Tuning**
- Diagnostic flags (-XX:+PrintFlagsFinal)
- Heap sizing recommendations
- GC tuning for throughput vs latency
- JIT compiler flags
- Profiling with JFR (Java Flight Recorder)
- Monitoring with JMX
- Production troubleshooting checklist

---

### Section 2: Concurrency & Multithreading

**Thread Creation and Lifecycle**
- Thread vs Runnable vs Callable
- Thread states (NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED)
- Thread priorities and scheduling
- Daemon threads vs user threads
- Thread.sleep() vs Object.wait()
- Thread.join() and thread coordination
- Virtual threads (Project Loom - Java 19+)

**Executor Framework and Thread Pools**
- ThreadPoolExecutor parameters (corePoolSize, maximumPoolSize, keepAliveTime)
- ExecutorService types (fixed, cached, single, scheduled)
- BlockingQueue implementations (LinkedBlockingQueue, ArrayBlockingQueue, SynchronousQueue)
- RejectedExecutionHandler strategies
- ForkJoinPool and work-stealing
- Custom thread factories
- Thread pool sizing formula

**CompletableFuture and Async Programming**
- Creating CompletableFuture (supplyAsync, runAsync)
- Chaining operations (thenApply, thenAccept, thenRun)
- Combining futures (thenCombine, thenCompose, allOf, anyOf)
- Exception handling (exceptionally, handle, whenComplete)
- Custom executors with CompletableFuture
- Avoiding blocking operations
- Real-world patterns

**Lock Implementations (ReentrantLock, ReadWriteLock)**
- Lock vs synchronized
- ReentrantLock fairness
- tryLock() with timeout
- Condition variables
- ReadWriteLock for read-heavy scenarios
- StampedLock (optimistic reads)
- Lock-free algorithms

**Concurrent Collections Deep Dive**
- ConcurrentHashMap implementation (segments, buckets, CAS)
- CopyOnWriteArrayList use cases
- BlockingQueue implementations comparison
- ConcurrentLinkedQueue (non-blocking)
- ConcurrentSkipListMap (sorted, concurrent)
- When to use each collection
- Performance benchmarks

**Atomic Classes and CAS Operations**
- AtomicInteger, AtomicLong, AtomicReference
- Compare-and-swap (CAS) algorithm
- ABA problem and AtomicStampedReference
- LongAdder vs AtomicLong (high contention)
- FieldUpdater for existing classes
- Building lock-free data structures
- Performance implications

**Synchronizers (CountDownLatch, CyclicBarrier, Semaphore, Phaser)**
- CountDownLatch for one-time events
- CyclicBarrier for recurring synchronization
- Semaphore for resource limiting
- Phaser for dynamic parties
- Exchanger for thread pairs
- Use case comparison
- Real-world examples

**ThreadLocal and Context Propagation**
- ThreadLocal usage and patterns
- InheritableThreadLocal for child threads
- ThreadLocal memory leaks (in thread pools)
- Context propagation in async code
- RequestContextHolder in Spring
- MDC (Mapped Diagnostic Context) in logging
- Cleaning up ThreadLocal

**Deadlock, Livelock, and Starvation**
- Deadlock conditions (mutual exclusion, hold and wait, no preemption, circular wait)
- Detecting deadlocks (jstack, VisualVM)
- Deadlock prevention strategies
- Livelock scenarios
- Thread starvation and fairness
- Dining philosophers problem
- Real-world deadlock debugging

**Memory Models and Concurrent Programming Patterns**
- Java Memory Model (JMM)
- Visibility, atomicity, ordering
- Safe publication patterns
- Producer-consumer pattern
- Thread-safe singleton patterns
- Immutability for concurrency
- Concurrent design principles

**Fork/Join Framework**
- RecursiveTask vs RecursiveAction
- Work-stealing algorithm
- When to use Fork/Join vs ExecutorService
- Parallel streams implementation
- Common pitfalls (too many tasks, blocking)
- Performance tuning
- Real-world use cases

**Advanced Concurrency Patterns**
- Double-checked locking (correct implementation)
- Spin locks and busy waiting
- Lock striping (ConcurrentHashMap)
- Read-copy-update (RCU) pattern
- Disruptor pattern (LMAX)
- Actor model concepts
- Reactive programming paradigms

---

### Section 3: Collections Framework Mastery

**Internal Implementation of HashMap**
- Array + LinkedList/TreeNode structure
- Hash function and bucket selection
- Collision handling (chaining, treeify at threshold 8)
- Load factor and resizing (rehashing)
- Java 8+ improvements (balanced trees)
- equals() and hashCode() contract
- Common pitfalls and best practices

**TreeMap, LinkedHashMap, and Specialized Maps**
- TreeMap (Red-Black tree implementation)
- NavigableMap operations
- LinkedHashMap (insertion order, access order)
- LRU cache implementation
- WeakHashMap for cache scenarios
- IdentityHashMap (reference equality)
- EnumMap performance benefits

**ArrayList vs LinkedList**
- Internal structure comparison
- Big O complexity analysis
- Random access vs sequential access
- Memory overhead
- Insertion/deletion performance
- Iterator performance
- Real-world decision criteria

**HashSet, TreeSet, LinkedHashSet Internals**
- HashSet backed by HashMap
- TreeSet backed by TreeMap
- LinkedHashSet maintaining order
- Custom comparators and Comparable
- Set operations performance
- Choosing the right Set implementation

**Queue and Deque Implementations**
- PriorityQueue (heap implementation)
- ArrayDeque vs LinkedList as Deque
- BlockingQueue for producer-consumer
- DelayQueue for scheduling
- TransferQueue semantics
- Choosing the right Queue

**Comparable vs Comparator**
- Natural ordering with Comparable
- Custom ordering with Comparator
- Comparator chaining (thenComparing)
- Comparator.comparing() method references
- Null handling in comparisons
- Sorting stability
- Performance considerations

**Collection Performance and Big O Analysis**
- Time complexity for each operation
- Space complexity considerations
- Amortized analysis (ArrayList resizing)
- Cache locality and memory access patterns
- Benchmarking collections (JMH)
- Choosing optimal data structure

**Immutable Collections and Defensive Copying**
- Collections.unmodifiableXXX()
- List.of(), Set.of(), Map.of() (Java 9+)
- Guava ImmutableList, ImmutableMap
- Defensive copying strategies
- Performance of immutable collections
- When to use immutability

---

### Section 4: Generics & Type System

**Generics Fundamentals and Type Erasure**
- Generic classes, interfaces, methods
- Type parameters (T, E, K, V)
- Type erasure at compile time
- Bridge methods
- Raw types (legacy compatibility)
- Reification vs erasure
- Limitations due to erasure

**Bounded Type Parameters and Wildcards**
- Upper bounds (extends)
- Lower bounds (super)
- Unbounded wildcards (?)
- PECS (Producer Extends Consumer Super)
- Multiple bounds
- Generic methods vs generic classes
- Real-world examples

**Generic Type Inference and Diamond Operator**
- Type inference in method calls
- Diamond operator (<>) in Java 7+
- Target typing in Java 8+
- Type witness in method calls
- Improved type inference in newer Java versions
- When inference fails

**Reified Generics Workarounds**
- Type tokens and TypeReference
- Passing Class<T> as parameter
- Guava TypeToken
- Jackson TypeReference
- Creating generic arrays
- Reflection with generics

**Covariance and Contravariance**
- Arrays are covariant (ArrayStoreException risk)
- Generics are invariant
- Wildcard variance
- Producer (covariance) vs Consumer (contravariance)
- Return type covariance in methods
- Real-world application

**Advanced Generic Patterns**
- Recursive type bounds (Enum<E extends Enum<E>>)
- Self-referential generics
- Generic builder pattern
- Type-safe heterogeneous containers
- Generic singleton pattern
- Generic factory pattern

---

### Section 5: Exception Handling & Error Management

**Exception Hierarchy and Best Practices**
- Throwable → Error vs Exception
- Checked vs unchecked exceptions
- When to use each type
- Custom exception design
- Exception chaining (getCause())
- Suppressed exceptions
- Exception translation in layers

**Try-with-Resources and AutoCloseable**
- Automatic resource management
- AutoCloseable vs Closeable
- Multiple resources in try-with-resources
- Suppressed exceptions in TWR
- Resource ordering and closing
- Custom AutoCloseable implementations
- Before Java 7 patterns

**Exception Handling Anti-Patterns**
- Catching Exception or Throwable
- Empty catch blocks
- Using exceptions for flow control
- Losing stack traces
- Rethrowing without context
- Exception swallowing
- Correct patterns

**Error Handling in Async and Functional Code**
- CompletableFuture exception handling
- Stream exception handling
- Optional instead of exceptions
- Either/Try monads (Vavr)
- Checked exceptions in lambdas
- Sneaky throws pattern
- Best practices for async errors

---

### Section 6: I/O, NIO, and Serialization

**Traditional I/O vs NIO vs NIO.2**
- Blocking I/O (streams)
- Non-blocking I/O (channels, selectors)
- Asynchronous I/O (AsynchronousChannel)
- Buffer management
- Direct vs heap buffers
- Memory-mapped files
- When to use each approach

**Files, Paths, and Modern File Operations**
- Path vs File
- Files utility class
- Walking file trees
- File attributes and permissions
- Watching directory changes (WatchService)
- Symbolic links handling
- Efficient file copying

**Serialization Mechanisms**
- Java serialization (Serializable)
- serialVersionUID importance
- transient and static fields
- Custom serialization (writeObject, readObject)
- Externalizable for full control
- Serialization proxy pattern
- Security concerns

**Alternative Serialization (JSON, Protobuf, Avro)**
- Jackson for JSON
- Gson alternatives
- Protocol Buffers
- Apache Avro
- MessagePack
- Performance comparison
- Schema evolution

**Network Programming Fundamentals**
- Socket and ServerSocket
- NIO sockets with Selector
- URL and URLConnection
- HTTP client (Java 11+)
- SSL/TLS configuration
- Connection pooling
- Timeout handling

---

### Section 7: Reflection & Dynamic Programming

**Core Reflection API**
- Class.forName() and classloading
- Getting fields, methods, constructors
- Accessing private members (setAccessible)
- Method invocation (invoke)
- Creating instances dynamically
- Generic type inspection
- Performance overhead

**Annotations and Annotation Processing**
- Built-in annotations (@Override, @Deprecated, @FunctionalInterface)
- Meta-annotations (@Target, @Retention, @Inherited)
- Custom annotations
- Annotation processing at compile time (APT)
- Runtime annotation processing
- Annotation inheritance
- Real-world annotation frameworks

**Proxy Pattern and Dynamic Proxies**
- java.lang.reflect.Proxy
- InvocationHandler implementation
- Proxy limitations (interfaces only)
- CGLIB for class proxies
- ByteBuddy for advanced cases
- Spring AOP proxy mechanisms
- Performance considerations

**Method Handles and invokedynamic**
- MethodHandle vs Reflection
- MethodHandles.Lookup
- invokedynamic bytecode instruction
- Lambda implementation via invokedynamic
- Performance benefits
- Use cases
- JVM optimization

**Metaprogramming Techniques**
- Code generation (JavaPoet, ByteBuddy)
- Bytecode manipulation (ASM, Javassist)
- Compile-time code generation
- Runtime code generation
- Use cases (ORM, serialization, mocking)
- Trade-offs and risks

---

## Part II: Modern Java Features

### Section 8: Java 8 — Lambdas & Streams

**Lambda Expressions Deep Dive**
- Functional interfaces
- Lambda syntax variations
- Method references (::)
- Capturing variables (effectively final)
- Lambda vs anonymous inner classes
- Serializable lambdas
- Performance characteristics

**Stream API Fundamentals**
- Creating streams (of, generate, iterate)
- Intermediate operations (map, filter, flatMap)
- Terminal operations (collect, reduce, forEach)
- Short-circuiting operations (findFirst, anyMatch)
- Stream pipeline optimization
- Stream reusability (or lack thereof)

**Advanced Stream Operations**
- groupingBy and partitioningBy
- Collectors.toMap() with merge function
- Custom collectors
- Downstream collectors
- teeing collector (Java 12+)
- Parallel streams considerations

**Parallel Streams and Performance**
- When to use parallel streams
- ForkJoinPool and parallelism
- Common pool sizing
- Performance pitfalls
- Boxing overhead
- Benchmarking streams (JMH)
- Sequential vs parallel decision

**Optional and Null Handling**
- Creating Optional (of, ofNullable, empty)
- Consuming values (ifPresent, orElse, orElseGet, orElseThrow)
- Transforming (map, flatMap, filter)
- Optional as return type only
- Optional anti-patterns
- Optional vs @Nullable annotations

**Method References and Constructor References**
- Static method references
- Instance method references
- Arbitrary object method references
- Constructor references
- Array constructor references
- When to use vs lambdas

**Functional Interfaces in java.util.function**
- Predicate, Function, Consumer, Supplier
- BiFunction, BiConsumer, BiPredicate
- UnaryOperator, BinaryOperator
- Primitive specializations (IntPredicate, etc.)
- Composing functions (andThen, compose)
- Custom functional interfaces

**Default and Static Methods in Interfaces**
- Default method syntax
- Multiple inheritance of behavior
- Diamond problem resolution
- Static methods in interfaces
- Interface evolution
- Defender methods pattern

---

### Section 9: Java 9–11 Features

**Module System (Jigsaw)**
- module-info.java syntax
- requires, exports, opens
- Services (provides, uses)
- Modular JDK
- Unnamed and automatic modules
- Migration strategies
- Benefits and challenges

**Collection Factory Methods**
- List.of(), Set.of(), Map.of()
- Map.ofEntries() for more entries
- Immutability guarantees
- Null handling
- Performance vs traditional collections
- Use cases

**Try-with-Resources Improvements**
- Effectively final variables
- Cleaner syntax in Java 9
- Multiple resources
- Resource ordering

**Process API Enhancements**
- ProcessHandle for process control
- Process information (PID, arguments, etc.)
- ProcessBuilder improvements
- Destroying processes
- Monitoring processes

**HTTP/2 Client API (Java 11)**
- HttpClient creation and configuration
- Synchronous vs asynchronous requests
- Request builders
- Response handling
- WebSocket support
- HTTP/2 features
- Comparison with libraries

**New String Methods and Compact Strings**
- isBlank(), lines(), strip()
- repeat(), indent()
- Compact Strings (Java 9)
- String deduplication
- Performance improvements

---

### Section 10: Java 12–17 Features

**Switch Expressions (Java 12–14)**
- New switch syntax (->)
- yield keyword
- Pattern matching in switch (preview)
- Exhaustiveness checking
- Multiple labels
- Statement vs expression

**Text Blocks (Java 13–15)**
- Multiline strings with """
- Indentation handling
- Escape sequences
- Use cases (SQL, JSON, HTML)

**Records (Java 14–16)**
- Compact syntax for data carriers
- Canonical constructor
- Component accessors
- equals(), hashCode(), toString()
- Validation in compact constructor
- Records vs classes
- Records with interfaces

**Pattern Matching for instanceof (Java 16)**
- Type test and cast in one
- Scope of pattern variables
- Combining with logical operators
- Nested patterns
- Performance benefits

**Sealed Classes (Java 17)**
- permits clause
- Restricting inheritance
- Pattern matching exhaustiveness
- Abstract sealed classes
- Sealed interfaces
- Use cases (ADTs, state machines)

**Helpful NullPointerExceptions (Java 14)**
- Precise NPE messages
- -XX:+ShowCodeDetailsInExceptionMessages
- Debugging improvements
- Before vs after comparison

**New Methods in Core Libraries**
- Stream.toList() (Java 16)
- Files.mismatch() (Java 12)
- String.transform() (Java 12)
- Predicate.not() (Java 11)
- Collection.toArray(IntFunction)
- Duration/Instant enhancements

---

### Section 11: Java 18–21 Features

**Virtual Threads (Project Loom — Java 19–21)**
- Virtual threads vs platform threads
- Creating virtual threads
- Structured concurrency (preview)
- Scoped values (preview)
- Performance characteristics
- When to use virtual threads
- Migration strategies

**Pattern Matching for Switch (Java 21)**
- Patterns in switch cases
- Guarded patterns
- Record patterns
- Exhaustiveness and coverage
- Null handling in switch
- Real-world examples

**Record Patterns (Java 19–21)**
- Deconstructing records
- Nested record patterns
- Pattern matching in instanceof
- Use cases and examples

**Sequenced Collections (Java 21)**
- SequencedCollection interface
- SequencedSet, SequencedMap
- Reversed views
- addFirst(), addLast()
- Uniform API for ordered collections

**String Templates (Preview)**
- STR processor
- FMT processor
- Custom processors
- Use cases
- Security considerations

---

### Section 11B: Java 22–25 Features

**Unnamed Variables and Patterns (Java 22)**
- Underscore _ for unused variables
- Unnamed patterns in switch
- Pattern matching improvements
- Use cases for readability
- Lambda parameters
- Exception parameters
- Try-with-resources

**Statements Before super() (Java 22)**
- Pre-construction validation
- Field initialization before super
- Constructor flexibility
- Use cases and patterns
- Limitations and rules

**Foreign Function & Memory API (Finalized Java 22)**
- MemorySegment and MemoryLayout
- Arena-based memory management
- Calling native functions without JNI
- SegmentAllocator strategies
- Interoperability with C libraries
- Performance vs JNI
- Safety guarantees and restrictions

**Structured Concurrency (Java 23+)**
- StructuredTaskScope finalization
- ShutdownOnSuccess and ShutdownOnFailure
- Exception handling in structured tasks
- Scope inheritance
- Cancellation propagation
- Real-world patterns (parallel API calls, fork-join workflows)
- vs traditional ExecutorService

**Scoped Values (Java 23+)**
- ScopedValue vs ThreadLocal
- Immutable context propagation
- Per-thread, per-scope binding
- Performance benefits (no cleanup needed)
- Inheritance rules
- Use cases (user context, transaction context)
- Integration with virtual threads

**Class-File API (Preview Java 22–23)**
- Parsing and generating class files
- Bytecode manipulation without ASM
- ClassFile, MethodModel, CodeModel
- Constant pool handling
- Use cases (instrumentation, code generation)
- Performance characteristics

**String Templates (Second Preview Java 23)**
- STR, FMT, RAW processors
- Custom template processors
- Expression interpolation
- SQL injection prevention patterns
- JSON/XML generation
- Internationalization support
- Security considerations

**Stream Gatherers (Java 22–23)**
- Custom intermediate operations
- Gatherer interface
- Stateful vs stateless gatherers
- Window operations
- Fixed-size batching
- Custom collectors alternative
- Performance considerations

---

### Section 12: JVM Languages & Interop

**Kotlin Interoperability**
- Calling Kotlin from Java
- Calling Java from Kotlin
- Data classes vs records
- Null safety interop
- Extension functions visibility
- Companion objects
- Coroutines in mixed projects

**Scala Interoperability**
- Java-Scala type mapping
- Case classes in Java
- Traits vs interfaces
- Scala collections in Java
- Functional programming patterns

**Groovy in Java Projects**
- Groovy scripts in Java apps
- Dynamic typing interop
- Groovy closures
- DSL creation
- Testing with Spock
- Gradle build scripts

**GraalVM and Native Images**
- Ahead-of-time compilation
- Native image constraints
- Reflection configuration
- Startup time improvements
- Memory footprint reduction
- Polyglot capabilities
- Use cases for native images

---

### Section 13: Performance & Optimization

**JMH (Java Microbenchmark Harness)**
- Writing benchmarks
- Warmup and measurement iterations
- State management
- Avoiding dead code elimination
- Blackhole and constant folding
- Interpreting results
- Common pitfalls

**Profiling Techniques**
- Sampling vs instrumentation
- Async-profiler
- Java Flight Recorder
- VisualVM and Mission Control
- CPU profiling
- Memory profiling
- Lock contention analysis

**Memory Optimization Strategies**
- Object pooling (when appropriate)
- Primitive specialization
- Avoiding autoboxing
- String interning
- Weak references for caches
- Off-heap memory
- Memory-mapped files

**CPU Optimization Techniques**
- Loop unrolling
- Branch prediction awareness
- Cache line awareness
- False sharing prevention (@Contended)
- Algorithm complexity optimization
- Data structure selection
- Avoiding allocations in hot paths

**Lazy Initialization Patterns**
- Double-checked locking (correct way)
- Lazy holder idiom
- Initialization-on-demand
- Supplier-based lazy
- AtomicReference lazy
- Performance trade-offs

**String Optimization**
- StringBuilder vs StringBuffer vs +
- String.intern() use cases
- String deduplication
- Compact strings
- Avoiding string concatenation in loops
- Regular expression compilation

**Collection Performance Tuning**
- Initial capacity sizing
- Load factor tuning
- Choosing appropriate implementation
- Avoiding list.contains() in loops
- Primitive collections (Trove, Eclipse Collections)
- Memory overhead comparison

**Caching Strategies**
- Memoization pattern
- Guava cache
- Caffeine cache
- Cache eviction policies
- Cache warming
- Distributed caching considerations
- Cache coherence

**Async and Non-Blocking Optimization**
- CompletableFuture best practices
- Avoiding blocking operations
- Reactive programming benefits
- Thread pool sizing
- Queue selection
- Backpressure handling

**JVM Tuning for Performance**
- Heap sizing strategies
- GC selection and tuning
- JIT compiler optimization
- Compressed oops
- Escape analysis
- Inline optimization
- Monitoring and measuring impact

---

## Part III: Enterprise Java

### Section 14: Design Patterns in Java

**Creational Patterns**
- Singleton (thread-safe implementations)
- Factory Method vs Abstract Factory
- Builder pattern (fluent API, telescoping constructor)
- Prototype pattern and cloning
- Object pool pattern
- Dependency Injection

**Structural Patterns**
- Adapter pattern (interface adaptation)
- Decorator pattern (I/O streams example)
- Proxy pattern (static, dynamic, CGLIB)
- Composite pattern (file system example)
- Bridge pattern
- Facade pattern

**Behavioral Patterns**
- Strategy pattern (functional interfaces)
- Observer pattern (listeners, PropertyChangeSupport)
- Command pattern
- Template method pattern
- Chain of responsibility
- State pattern
- Iterator pattern (internal workings)

**Concurrency Patterns**
- Thread pool pattern
- Producer-consumer pattern
- Read-write lock pattern
- Double-checked locking (correct implementation)
- Thread-safe lazy initialization
- Future pattern
- Active object pattern

**Functional Patterns**
- Monad pattern (Optional, Stream, CompletableFuture)
- Function composition
- Partial application and currying
- Immutable objects pattern
- Persistent data structures
- Loan pattern (try-with-resources)

**Anti-Patterns to Avoid**
- God object
- Spaghetti code
- Lava flow
- Golden hammer
- Circular dependencies
- Premature optimization
- Not invented here syndrome

**SOLID Principles in Java**
- Single Responsibility Principle
- Open/Closed Principle
- Liskov Substitution Principle
- Interface Segregation Principle
- Dependency Inversion Principle
- Real-world examples
- Violations and refactoring

**DRY, KISS, YAGNI**
- Don't Repeat Yourself
- Keep It Simple, Stupid
- You Aren't Gonna Need It
- Applying in real projects
- Balancing principles
- When to violate principles

**Dependency Injection Patterns**
- Constructor injection
- Setter injection
- Interface injection
- Service locator anti-pattern
- DI containers (Spring, Guice, Dagger)
- Manual DI

**Resource Management Patterns**
- Try-with-resources
- Dispose pattern
- Object pool pattern
- Resource leak prevention
- Finalizer and cleaner (avoid)
- Weak reference cleanup

**Error Handling Patterns**
- Fail fast vs fail safe
- Exception translation
- Checked vs unchecked strategy
- Null object pattern vs Optional
- Try-Success-Failure pattern
- Circuit breaker pattern

**Testing Patterns**
- Test doubles (mock, stub, spy, fake)
- Builder pattern for tests
- Object mother pattern
- Test data builders
- Fixture setup patterns
- Parameterized tests

---

### Section 15: Testing & Quality

**JUnit 5 Advanced Features**
- @ParameterizedTest (CSV, Method, ValueSource)
- @RepeatedTest
- @TestFactory (dynamic tests)
- @Nested tests
- Test lifecycle (@BeforeAll, @BeforeEach, etc.)
- Conditional test execution
- Test ordering

**Mocking Frameworks (Mockito, EasyMock)**
- Mock vs Spy vs Stub
- @Mock, @InjectMocks
- when-thenReturn stubbing
- Argument matchers
- Verification (verify, times, never)
- Mocking static methods
- Best practices and anti-patterns

**Testing Best Practices**
- Arrange-Act-Assert pattern
- Given-When-Then pattern
- Test naming conventions
- Test independence
- Avoiding test interdependencies
- Fast tests vs slow tests
- Test pyramids

**Integration Testing Strategies**
- Spring Boot test slices
- Testcontainers for dependencies
- Database testing (H2, Testcontainers)
- REST API testing (MockMvc, RestAssured)
- Message queue testing
- Test data management

**Property-Based Testing**
- JUnit QuickCheck
- jqwik framework
- Generating test data
- Shrinking failures
- Use cases for property tests
- Complementing example-based tests

**Mutation Testing**
- PITest configuration
- Mutation operators
- Interpreting mutation scores
- Improving test quality
- CI integration

**Test Coverage Analysis**
- JaCoCo configuration
- Line vs branch coverage
- Coverage goals (realistic targets)
- Coverage limitations
- Uncovered code analysis
- Integration with build tools

**Performance Testing**
- JMH for microbenchmarks
- JMeter for load testing
- Gatling for complex scenarios
- Profiling in tests
- CI performance regression detection

---

### Section 16: Build Tools & Dependency Management

**Maven Deep Dive**
- POM structure and inheritance
- Dependency scopes (compile, provided, test, runtime)
- Dependency management vs dependencies
- Plugin configuration
- Multi-module projects
- Profiles for environments
- Repository management

**Gradle Fundamentals**
- Groovy vs Kotlin DSL
- Task dependencies
- Build lifecycle phases
- Multi-project builds
- Custom tasks
- Plugin development
- Performance optimization (build cache, daemon)

**Dependency Management Strategies**
- Transitive dependencies
- Dependency conflicts resolution
- Version ranges (avoid)
- BOM (Bill of Materials)
- Dependency exclusions
- Enforcing versions
- Vulnerability scanning (OWASP Dependency Check)

**Build Optimization**
- Incremental builds
- Parallel execution
- Build cache (Gradle)
- Module splitting
- Fat JAR vs thin JAR
- Native image builds

---

### Section 17: Logging & Monitoring

**Logging Frameworks (SLF4J, Logback, Log4j2)**
- SLF4J abstraction layer
- Logback configuration
- Log4j2 async logging
- Performance comparison
- Structured logging (JSON)
- Log levels and usage
- MDC (Mapped Diagnostic Context)

**Effective Logging Strategies**
- What to log and what not to log
- Log levels (TRACE, DEBUG, INFO, WARN, ERROR)
- Parameterized logging
- Avoid string concatenation
- Logging exceptions properly
- Performance considerations
- PII and security in logs

**Application Monitoring**
- JMX and MBeans
- Metrics (Micrometer)
- Health checks
- Custom metrics
- Prometheus integration
- Grafana dashboards
- Alerting strategies

**Distributed Tracing**
- OpenTelemetry
- Trace context propagation
- Span creation and attributes
- Jaeger and Zipkin
- Correlation IDs
- Performance impact
- Sampling strategies

---

### Section 18: Security in Java

**Java Cryptography Architecture (JCA)**
- MessageDigest for hashing
- Cipher for encryption/decryption
- KeyGenerator and SecureRandom
- Digital signatures
- Certificate management
- Provider architecture
- Best practices

**Secure Coding Practices**
- Input validation
- SQL injection prevention (PreparedStatement)
- XSS prevention
- CSRF protection
- Authentication and authorization
- Secure password storage (bcrypt, Argon2)
- Secrets management

**SSL/TLS in Java**
- SSLContext configuration
- TrustManager and KeyManager
- Certificate validation
- Hostname verification
- Cipher suite selection
- TLS version selection
- Mutual TLS (mTLS)

**Java Security Manager**
- Security policies
- Permissions (FilePermission, SocketPermission)
- Sandboxing untrusted code
- Why it's deprecated
- Alternatives (containers, OS-level)

**Deserialization Vulnerabilities**
- Gadget chains
- ObjectInputStream risks
- SerialKiller and filters
- Alternatives to Java serialization
- Safe deserialization practices

**Dependency Vulnerabilities**
- OWASP Top 10
- Dependency scanning tools
- CVE tracking
- Keeping dependencies updated
- Security policies in builds
- Security audits

---

### Section 19: Code Quality & Maintainability

**Static Analysis Tools**
- SonarQube configuration and rules
- SpotBugs (FindBugs successor)
- PMD and custom rules
- Checkstyle for formatting
- Error Prone (Google)
- Integrating into build

**Code Smells and Refactoring**
- Long methods
- Large classes
- Duplicate code
- Feature envy
- Data clumps
- Primitive obsession
- Refactoring catalog

**Clean Code Principles**
- Meaningful names
- Small functions/methods
- Comments vs self-documenting code
- Error handling clarity
- Dependency management
- SOLID in practice
- The Boy Scout Rule

**Documentation Strategies**
- Javadoc best practices
- When to document and when not to
- README files
- Architecture Decision Records (ADR)
- API documentation (Swagger/OpenAPI)
- Living documentation

**Code Review Best Practices**
- What to look for in reviews
- Giving constructive feedback
- Automated checks before review
- Review checklist
- Small, focused changes
- Review turnaround time

**Technical Debt Management**
- Identifying technical debt
- Quantifying debt
- Prioritizing debt paydown
- Balancing features vs refactoring
- Preventing debt accumulation
- Communicating debt to stakeholders

---

## Part IV: Specialized Topics

### Section 20: Functional Programming in Java

**Pure Functions and Immutability**
- Defining pure functions
- Benefits of immutability
- Immutable collections
- Persistent data structures
- Copy-on-write strategies
- Performance implications

**Higher-Order Functions**
- Functions as parameters
- Functions as return values
- Function composition
- Currying in Java
- Partial application
- Real-world examples

**Monads in Java**
- Optional monad
- Stream monad
- CompletableFuture monad
- Try monad (Vavr)
- Either monad
- Monad laws
- Practical applications

**Functional Error Handling**
- Optional for nullable values
- Either for success/failure
- Try for exception handling
- Result types
- Railway-oriented programming
- Avoiding checked exceptions

**Lazy Evaluation**
- Stream lazy evaluation
- Supplier for deferred computation
- Memoization
- Infinite streams
- Benefits and trade-offs

**Functional Libraries (Vavr, Guava)**
- Vavr collections
- Pattern matching in Vavr
- Function composition
- Tuple types
- Try and Either
- Lazy values

---

### Section 21: Reactive Programming

**Reactive Streams Specification**
- Publisher, Subscriber, Subscription, Processor
- Backpressure handling
- Cold vs hot publishers
- Marble diagrams
- TCK (Technology Compatibility Kit)

**Project Reactor Fundamentals**
- Mono vs Flux
- Creating publishers
- Transforming operators (map, flatMap, filter)
- Combining operators (zip, merge, concat)
- Error handling operators
- Schedulers and threading

**RxJava Patterns**
- Observable, Flowable, Single, Maybe, Completable
- Schedulers (io, computation, newThread)
- Operators comparison with Reactor
- Backpressure strategies
- Testing with TestScheduler

**Reactive Design Patterns**
- Request-response pattern
- Fire-and-forget pattern
- Stream processing pattern
- Event sourcing with reactive
- CQRS with reactive

**Reactive vs Imperative**
- When to use reactive
- Performance implications
- Learning curve
- Debugging challenges
- Migration strategies

**Testing Reactive Code**
- StepVerifier in Reactor
- TestSubscriber in RxJava
- Virtual time
- Testing error scenarios
- Testing backpressure

---

### Section 22: Microservices Patterns

**Service Communication**
- REST vs gRPC vs GraphQL
- Synchronous vs asynchronous
- Service mesh (Istio, Linkerd)
- API Gateway pattern
- Backend for Frontend (BFF)

**Service Discovery and Load Balancing**
- Client-side discovery (Eureka, Consul)
- Server-side discovery
- Load balancing algorithms
- Health checks
- Circuit breaker pattern

**Resilience Patterns**
- Circuit breaker (Resilience4j, Hystrix)
- Retry with backoff
- Timeout strategies
- Bulkhead pattern
- Rate limiting
- Failover and fallback

**Distributed Transactions**
- Saga pattern (choreography vs orchestration)
- Two-phase commit (2PC) problems
- Eventual consistency
- Compensating transactions
- Outbox pattern

**Configuration Management**
- Spring Cloud Config
- Consul KV
- Environment-specific configs
- Dynamic configuration updates
- Secrets management (Vault)

**Observability in Microservices**
- Distributed tracing (Zipkin, Jaeger)
- Centralized logging (ELK, Splunk)
- Metrics aggregation (Prometheus)
- Service mesh observability
- Correlation IDs

---

### Section 23: Data Structures & Algorithms

**Tree Structures**
- Binary trees, BST, AVL, Red-Black
- B-trees and B+ trees
- Trie for string search
- Segment tree
- Tree traversals (DFS, BFS)
- LCA (Lowest Common Ancestor)

**Graph Algorithms**
- Graph representations (adjacency list/matrix)
- BFS and DFS
- Dijkstra's shortest path
- Bellman-Ford algorithm
- Topological sort
- Cycle detection
- Minimum spanning tree (Kruskal, Prim)

**Sorting Algorithms**
- QuickSort, MergeSort, HeapSort
- Stability in sorting
- TimSort (Java's default)
- Radix sort for integers
- Custom comparators
- Sorting complexity analysis

**Search Algorithms**
- Binary search variations
- Searching in rotated arrays
- KMP string matching
- Rabin-Karp algorithm
- Trie-based search
- A* search algorithm

**Dynamic Programming Patterns**
- Memoization vs tabulation
- Fibonacci variants
- Knapsack problem
- Longest common subsequence
- Matrix chain multiplication
- Recognizing DP problems

**Advanced Data Structures**
- Union-Find (Disjoint Set)
- Bloom filters
- LRU cache implementation
- Skip list
- Fenwick tree (BIT)
- Suffix array and suffix tree

**String Algorithms**
- String matching (KMP, Boyer-Moore)
- Regular expression implementation
- Longest palindromic substring
- Edit distance (Levenshtein)
- Anagram detection
- String permutations

**Bit Manipulation**
- Bitwise operators (AND, OR, XOR, NOT)
- Bit masking techniques
- Counting set bits
- Power of 2 checks
- Bitwise tricks
- Bit manipulation problems

---

### Section 24: System Design

**Scalability Fundamentals**
- Horizontal vs vertical scaling
- Load balancing strategies
- Caching layers (CDN, application, database)
- Database replication and sharding
- Stateless vs stateful services
- Asynchronous processing

**Database Design Decisions**
- SQL vs NoSQL trade-offs
- Normalization vs denormalization
- ACID vs BASE
- CAP theorem
- Choosing data stores
- Polyglot persistence

**Caching Strategies**
- Cache-aside (lazy loading)
- Write-through cache
- Write-behind cache
- Refresh-ahead cache
- Cache invalidation strategies
- Distributed caching
- Cache coherence

**Message Queues and Event Streaming**
- Kafka vs RabbitMQ vs SQS
- At-least-once vs exactly-once
- Message ordering guarantees
- Dead letter queues
- Event-driven architecture
- CQRS and Event Sourcing

**Rate Limiting and Throttling**
- Token bucket algorithm
- Leaky bucket algorithm
- Fixed window vs sliding window
- Distributed rate limiting
- API quotas
- Backpressure handling

**High Availability and Disaster Recovery**
- Redundancy and replication
- Failover strategies
- Backup and restore
- Multi-region deployment
- Chaos engineering
- RTO and RPO targets

---

### Section 25: Spring Framework Deep Dive

**Spring Core Container**
- ApplicationContext vs BeanFactory
- Bean lifecycle callbacks
- Bean scopes (singleton, prototype, request, session)
- FactoryBean vs @Bean
- @Configuration and @Component
- Circular dependencies resolution

**Spring AOP**
- Proxy mechanisms (JDK dynamic proxy, CGLIB)
- Aspect, Advice, Pointcut, Join point
- @Before, @After, @Around, @AfterReturning, @AfterThrowing
- Pointcut expressions
- AspectJ vs Spring AOP
- AOP use cases (logging, transaction, security)

**Spring Transaction Management**
- @Transactional internals
- Propagation levels
- Isolation levels
- Rollback rules
- Programmatic transactions
- Transaction synchronization
- Common pitfalls

**Spring Boot Auto-Configuration**
- @SpringBootApplication breakdown
- Auto-configuration mechanism
- Conditional annotations (@ConditionalOnClass, etc.)
- Customizing auto-configuration
- Auto-configuration report
- Creating custom starters

**Spring Data JPA Advanced**
- Custom repositories
- Specifications for dynamic queries
- Query methods naming conventions
- @EntityGraph for N+1 problem
- Projections (interface, DTO, dynamic)
- Auditing with @CreatedDate, @LastModifiedDate
- Soft deletes

**Spring WebFlux**
- Reactive programming model
- Router functions vs annotated controllers
- WebClient for reactive HTTP
- Backpressure handling
- Error handling in reactive
- Testing reactive endpoints

**Spring Security Internals**
- Security filter chain
- Authentication providers
- UserDetailsService
- Password encoders
- JWT implementation
- OAuth2 resource server
- Method security (@PreAuthorize, @Secured)

**Spring Boot Production Features**
- Actuator endpoints
- Metrics with Micrometer
- Health indicators
- Custom actuator endpoints
- Application events
- @ConfigurationProperties validation
- Externalized configuration

---

## Contributing

Found an error, have a better example, or want to add a missing section? See the [Contributing Guide](../CONTRIBUTING.md).