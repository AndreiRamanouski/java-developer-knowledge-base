# Java Knowledge Base

A comprehensive reference for Java developers covering core internals, modern features, enterprise patterns, and specialized topics. All examples use Java 17+ unless otherwise noted.

[← Back to the main README](../README.md)

---

## Contents

<!-- toc:start -->

### [1. Core Java](1.%20Core%20Java)

- [Summary 1. Java Memory Model & Internals](1.%20Core%20Java/Summary%201.%20Java%20Memory%20Model%20%26%20Internals.md)
- [Summary 2. Concurrency & Multithreading](1.%20Core%20Java/Summary%202.%20Concurrency%20%26%20Multithreading.md)
- [Summary 3. Collections Framework](1.%20Core%20Java/Summary%203.%20Collections%20Framework.md)
- [Summary 4. Generics & Type System](1.%20Core%20Java/Summary%204.%20Generics%20%26%20Type%20System.md)
- [Summary 5. Exception Handling & Error Management](1.%20Core%20Java/Summary%205.%20Exception%20Handling%20%26%20Error%20Management.md)
- [Summary 6. IO, NIO, and Serialization](1.%20Core%20Java/Summary%206.%20IO%2C%20NIO%2C%20and%20Serialization.md)
- [Summary 7. Reflection & Dynamic Programming](1.%20Core%20Java/Summary%207.%20Reflection%20%26%20Dynamic%20Programming.md)
- **[1. Java Memory Model & Internals](1.%20Core%20Java/1.%20Java%20Memory%20Model%20%26%20Internals)**
  - [1. JVM memory architecture deep dive](1.%20Core%20Java/1.%20Java%20Memory%20Model%20%26%20Internals/1.%20JVM%20memory%20architecture%20deep%20dive.md)
  - [2. Garbage collection algorithms and tuning](1.%20Core%20Java/1.%20Java%20Memory%20Model%20%26%20Internals/2.%20Garbage%20collection%20algorithms%20and%20tuning.md)
  - [3. Object lifecycle and memory leaks](1.%20Core%20Java/1.%20Java%20Memory%20Model%20%26%20Internals/3.%20Object%20lifecycle%20and%20memory%20leaks.md)
  - [4. ClassLoader hierarchy and mechanism](1.%20Core%20Java/1.%20Java%20Memory%20Model%20%26%20Internals/4.%20ClassLoader%20hierarchy%20and%20mechanism.md)
  - [5. Java bytecode and JIT compilation](1.%20Core%20Java/1.%20Java%20Memory%20Model%20%26%20Internals/5.%20Java%20bytecode%20and%20JIT%20compilation.md)
  - [6. Volatile, synchronized, and happens-before](1.%20Core%20Java/1.%20Java%20Memory%20Model%20%26%20Internals/6.%20Volatile%2C%20synchronized%2C%20and%20happens-before.md)
  - [7. Object layout and memory overhead](1.%20Core%20Java/1.%20Java%20Memory%20Model%20%26%20Internals/7.%20Object%20layout%20and%20memory%20overhead.md)
  - [8. Stack vs heap allocation](1.%20Core%20Java/1.%20Java%20Memory%20Model%20%26%20Internals/8.%20Stack%20vs%20heap%20allocation.md)
  - [9. Native memory and DirectByteBuffer](1.%20Core%20Java/1.%20Java%20Memory%20Model%20%26%20Internals/9.%20Native%20memory%20and%20DirectByteBuffer.md)
  - [10. JVM flags and performance tuning](1.%20Core%20Java/1.%20Java%20Memory%20Model%20%26%20Internals/10.%20JVM%20flags%20and%20performance%20tuning.md)
- **[2. Concurrency & Multithreading](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading)**
  - [1. Thread creation and lifecycle](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/1.%20Thread%20creation%20and%20lifecycle.md)
  - [2. Executor framework and thread pools](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/2.%20Executor%20framework%20and%20thread%20pools.md)
  - [3. CompletableFuture and async programming](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/3.%20CompletableFuture%20and%20async%20programming.md)
  - [4. Lock implementations (ReentrantLock, ReadWriteLock)](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/4.%20Lock%20implementations%20%28ReentrantLock%2C%20ReadWriteLock%29.md)
  - [5. Concurrent collections deep dive](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/5.%20Concurrent%20collections%20deep%20dive.md)
  - [6. Atomic classes and CAS operations](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/6.%20Atomic%20classes%20and%20CAS%20operations.md)
  - [7. Synchronizers (CountDownLatch, CyclicBarrier, Semaphore, Phaser)](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/7.%20Synchronizers%20%28CountDownLatch%2C%20CyclicBarrier%2C%20Semaphore%2C%20Phaser%29.md)
  - [8. ThreadLocal and context propagation](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/8.%20ThreadLocal%20and%20context%20propagation.md)
  - [9. Deadlock, livelock, and starvation](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/9.%20Deadlock%2C%20livelock%2C%20and%20starvation.md)
  - [10. Memory models and concurrent programming patterns](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/10.%20Memory%20models%20and%20concurrent%20programming%20patterns.md)
  - [11. Fork-Join framework](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/11.%20Fork-Join%20framework.md)
  - [12. Advanced concurrency patterns](1.%20Core%20Java/2.%20Concurrency%20%26%20Multithreading/12.%20Advanced%20concurrency%20patterns.md)
- **[3. Collections Framework](1.%20Core%20Java/3.%20Collections%20Framework)**
  - [1. Internal implementation of HashMap](1.%20Core%20Java/3.%20Collections%20Framework/1.%20Internal%20implementation%20of%20HashMap.md)
  - [2. TreeMap, LinkedHashMap, and specialized maps](1.%20Core%20Java/3.%20Collections%20Framework/2.%20TreeMap%2C%20LinkedHashMap%2C%20and%20specialized%20maps.md)
  - [3. ArrayList vs LinkedList - when to use each](1.%20Core%20Java/3.%20Collections%20Framework/3.%20ArrayList%20vs%20LinkedList%20-%20when%20to%20use%20each.md)
  - [4. HashSet, TreeSet, LinkedHashSet internals](1.%20Core%20Java/3.%20Collections%20Framework/4.%20HashSet%2C%20TreeSet%2C%20LinkedHashSet%20internals.md)
  - [5. Queue and Deque implementations](1.%20Core%20Java/3.%20Collections%20Framework/5.%20Queue%20and%20Deque%20implementations.md)
  - [6. Comparable vs Comparator](1.%20Core%20Java/3.%20Collections%20Framework/6.%20Comparable%20vs%20Comparator.md)
  - [7. Collection performance and Big O analysis](1.%20Core%20Java/3.%20Collections%20Framework/7.%20Collection%20performance%20and%20Big%20O%20analysis.md)
  - [8. Immutable collections and defensive copying](1.%20Core%20Java/3.%20Collections%20Framework/8.%20Immutable%20collections%20and%20defensive%20copying.md)
- **[4. Generics & Type System](1.%20Core%20Java/4.%20Generics%20%26%20Type%20System)**
  - [1. Generics fundamentals and type erasure](1.%20Core%20Java/4.%20Generics%20%26%20Type%20System/1.%20Generics%20fundamentals%20and%20type%20erasure.md)
  - [2. Bounded type parameters and wildcards](1.%20Core%20Java/4.%20Generics%20%26%20Type%20System/2.%20Bounded%20type%20parameters%20and%20wildcards.md)
  - [3. Generic type inference and diamond operator](1.%20Core%20Java/4.%20Generics%20%26%20Type%20System/3.%20Generic%20type%20inference%20and%20diamond%20operator.md)
  - [4. Reified generics workarounds](1.%20Core%20Java/4.%20Generics%20%26%20Type%20System/4.%20Reified%20generics%20workarounds.md)
  - [5. Covariance and contravariance](1.%20Core%20Java/4.%20Generics%20%26%20Type%20System/5.%20Covariance%20and%20contravariance.md)
  - [6. Advanced generic patterns](1.%20Core%20Java/4.%20Generics%20%26%20Type%20System/6.%20Advanced%20generic%20patterns.md)
- **[5. Exception Handling & Error Management](1.%20Core%20Java/5.%20Exception%20Handling%20%26%20Error%20Management)**
  - [1. Exception hierarchy and best practices](1.%20Core%20Java/5.%20Exception%20Handling%20%26%20Error%20Management/1.%20Exception%20hierarchy%20and%20best%20practices.md)
  - [2. Try-with-resources and AutoCloseable](1.%20Core%20Java/5.%20Exception%20Handling%20%26%20Error%20Management/2.%20Try-with-resources%20and%20AutoCloseable.md)
  - [3. Exception handling anti-patterns](1.%20Core%20Java/5.%20Exception%20Handling%20%26%20Error%20Management/3.%20Exception%20handling%20anti-patterns.md)
  - [4. Error handling in async and functional code](1.%20Core%20Java/5.%20Exception%20Handling%20%26%20Error%20Management/4.%20Error%20handling%20in%20async%20and%20functional%20code.md)
- **[6. IO, NIO, and Serialization](1.%20Core%20Java/6.%20IO%2C%20NIO%2C%20and%20Serialization)**
  - [1. Traditional IO vs NIO vs NIO.2](1.%20Core%20Java/6.%20IO%2C%20NIO%2C%20and%20Serialization/1.%20Traditional%20IO%20vs%20NIO%20vs%20NIO.2.md)
  - [2. Files, Paths, and modern file operations](1.%20Core%20Java/6.%20IO%2C%20NIO%2C%20and%20Serialization/2.%20Files%2C%20Paths%2C%20and%20modern%20file%20operations.md)
  - [3. Serialization mechanisms](1.%20Core%20Java/6.%20IO%2C%20NIO%2C%20and%20Serialization/3.%20Serialization%20mechanisms.md)
  - [4. Alternative serialization (JSON, Protobuf, Avro)](1.%20Core%20Java/6.%20IO%2C%20NIO%2C%20and%20Serialization/4.%20Alternative%20serialization%20%28JSON%2C%20Protobuf%2C%20Avro%29.md)
  - [5. Network programming fundamentals](1.%20Core%20Java/6.%20IO%2C%20NIO%2C%20and%20Serialization/5.%20Network%20programming%20fundamentals.md)
- **[7. Reflection & Dynamic Programming](1.%20Core%20Java/7.%20Reflection%20%26%20Dynamic%20Programming)**
  - [1. Core Reflection API](1.%20Core%20Java/7.%20Reflection%20%26%20Dynamic%20Programming/1.%20Core%20Reflection%20API.md)
  - [2. Annotations and annotation processing](1.%20Core%20Java/7.%20Reflection%20%26%20Dynamic%20Programming/2.%20Annotations%20and%20annotation%20processing.md)
  - [3. Proxy pattern and dynamic proxies](1.%20Core%20Java/7.%20Reflection%20%26%20Dynamic%20Programming/3.%20Proxy%20pattern%20and%20dynamic%20proxies.md)
  - [4. Method handles and invokedynamic](1.%20Core%20Java/7.%20Reflection%20%26%20Dynamic%20Programming/4.%20Method%20handles%20and%20invokedynamic.md)
  - [5. Metaprogramming techniques](1.%20Core%20Java/7.%20Reflection%20%26%20Dynamic%20Programming/5.%20Metaprogramming%20techniques.md)

### [2. Modern Java Features](2.%20Modern%20Java%20Features)

- **[1. Java 8 - Lambdas & Streams](2.%20Modern%20Java%20Features/1.%20Java%208%20-%20Lambdas%20%26%20Streams)**
  - [1. Lambda expressions deep dive](2.%20Modern%20Java%20Features/1.%20Java%208%20-%20Lambdas%20%26%20Streams/1.%20Lambda%20expressions%20deep%20dive.md)
  - [2. Stream API fundamentals](2.%20Modern%20Java%20Features/1.%20Java%208%20-%20Lambdas%20%26%20Streams/2.%20Stream%20API%20fundamentals.md)
  - [3. Advanced stream operations](2.%20Modern%20Java%20Features/1.%20Java%208%20-%20Lambdas%20%26%20Streams/3.%20Advanced%20stream%20operations.md)
  - [4. Parallel streams and performance](2.%20Modern%20Java%20Features/1.%20Java%208%20-%20Lambdas%20%26%20Streams/4.%20Parallel%20streams%20and%20performance.md)
  - [5. Optional and null handling](2.%20Modern%20Java%20Features/1.%20Java%208%20-%20Lambdas%20%26%20Streams/5.%20Optional%20and%20null%20handling.md)
  - [6. Method references and constructor references](2.%20Modern%20Java%20Features/1.%20Java%208%20-%20Lambdas%20%26%20Streams/6.%20Method%20references%20and%20constructor%20references.md)
  - [7. Functional interfaces in java.util.function](2.%20Modern%20Java%20Features/1.%20Java%208%20-%20Lambdas%20%26%20Streams/7.%20Functional%20interfaces%20in%20java.util.function.md)
  - [8. Default and static methods in interfaces](2.%20Modern%20Java%20Features/1.%20Java%208%20-%20Lambdas%20%26%20Streams/8.%20Default%20and%20static%20methods%20in%20interfaces.md)
- **[2. Java 9-11 Features](2.%20Modern%20Java%20Features/2.%20Java%209-11%20Features)**
  - [1. Module system (Jigsaw)](2.%20Modern%20Java%20Features/2.%20Java%209-11%20Features/1.%20Module%20system%20%28Jigsaw%29.md)
  - [2. Collection factory methods](2.%20Modern%20Java%20Features/2.%20Java%209-11%20Features/2.%20Collection%20factory%20methods.md)
  - [3. Try-with-resources improvements](2.%20Modern%20Java%20Features/2.%20Java%209-11%20Features/3.%20Try-with-resources%20improvements.md)
  - [4. Process API enhancements](2.%20Modern%20Java%20Features/2.%20Java%209-11%20Features/4.%20Process%20API%20enhancements.md)
  - [5. HTTP2 Client API (Java 11)](2.%20Modern%20Java%20Features/2.%20Java%209-11%20Features/5.%20HTTP2%20Client%20API%20%28Java%2011%29.md)
  - [6. New String methods and compact strings](2.%20Modern%20Java%20Features/2.%20Java%209-11%20Features/6.%20New%20String%20methods%20and%20compact%20strings.md)
- **[3. Java 12-17 Features](2.%20Modern%20Java%20Features/3.%20Java%2012-17%20Features)**
  - [1. Switch expressions (Java 12-14)](2.%20Modern%20Java%20Features/3.%20Java%2012-17%20Features/1.%20Switch%20expressions%20%28Java%2012-14%29.md)
  - [2. Text blocks (Java 13-15)](2.%20Modern%20Java%20Features/3.%20Java%2012-17%20Features/2.%20Text%20blocks%20%28Java%2013-15%29.md)
  - [3. Records (Java 14-16)](2.%20Modern%20Java%20Features/3.%20Java%2012-17%20Features/3.%20Records%20%28Java%2014-16%29.md)
  - [4. Pattern matching for instanceof (Java 16)](2.%20Modern%20Java%20Features/3.%20Java%2012-17%20Features/4.%20Pattern%20matching%20for%20instanceof%20%28Java%2016%29.md)
  - [5. Sealed classes (Java 17)](2.%20Modern%20Java%20Features/3.%20Java%2012-17%20Features/5.%20Sealed%20classes%20%28Java%2017%29.md)
  - [6. Helpful NullPointerExceptions (Java 14)](2.%20Modern%20Java%20Features/3.%20Java%2012-17%20Features/6.%20Helpful%20NullPointerExceptions%20%28Java%2014%29.md)
  - [7. New methods in core libraries](2.%20Modern%20Java%20Features/3.%20Java%2012-17%20Features/7.%20New%20methods%20in%20core%20libraries.md)
- **[4. Java 18-21 Features](2.%20Modern%20Java%20Features/4.%20Java%2018-21%20Features)**
  - [1. Virtual threads (Project Loom - Java 19-21)](2.%20Modern%20Java%20Features/4.%20Java%2018-21%20Features/1.%20Virtual%20threads%20%28Project%20Loom%20-%20Java%2019-21%29.md)
  - [2. Pattern matching for switch (Java 21)](2.%20Modern%20Java%20Features/4.%20Java%2018-21%20Features/2.%20Pattern%20matching%20for%20switch%20%28Java%2021%29.md)
  - [3. Record patterns (Java 19-21)](2.%20Modern%20Java%20Features/4.%20Java%2018-21%20Features/3.%20Record%20patterns%20%28Java%2019-21%29.md)
  - [4. Sequenced collections (Java 21)](2.%20Modern%20Java%20Features/4.%20Java%2018-21%20Features/4.%20Sequenced%20collections%20%28Java%2021%29.md)
- **[5. Java 22-25 Features](2.%20Modern%20Java%20Features/5.%20Java%2022-25%20Features)**
  - [1. Unnamed variables and patterns (Java 22)](2.%20Modern%20Java%20Features/5.%20Java%2022-25%20Features/1.%20Unnamed%20variables%20and%20patterns%20%28Java%2022%29.md)
  - [2. Flexible constructor bodies (Java 25)](2.%20Modern%20Java%20Features/5.%20Java%2022-25%20Features/2.%20Flexible%20constructor%20bodies%20%28Java%2025%29.md)
  - [3. Foreign Function & Memory API (finalized Java 22)](2.%20Modern%20Java%20Features/5.%20Java%2022-25%20Features/3.%20Foreign%20Function%20%26%20Memory%20API%20%28finalized%20Java%2022%29.md)
  - [4. Structured concurrency (Java 25 preview)](2.%20Modern%20Java%20Features/5.%20Java%2022-25%20Features/4.%20Structured%20concurrency%20%28Java%2025%20preview%29.md)
  - [5. Module import declarations (Java 25)](2.%20Modern%20Java%20Features/5.%20Java%2022-25%20Features/5.%20Module%20import%20declarations%20%28Java%2025%29.md)
  - [6. Scoped values (Java 25)](2.%20Modern%20Java%20Features/5.%20Java%2022-25%20Features/6.%20Scoped%20values%20%28Java%2025%29.md)
  - [7. Class-file API (Java 24)](2.%20Modern%20Java%20Features/5.%20Java%2022-25%20Features/7.%20Class-file%20API%20%28Java%2024%29.md)
  - [8. Compact source files and instance main methods (Java 25)](2.%20Modern%20Java%20Features/5.%20Java%2022-25%20Features/8.%20Compact%20source%20files%20and%20instance%20main%20methods%20%28Java%2025%29.md)
  - [9. Stream gatherers (Java 24)](2.%20Modern%20Java%20Features/5.%20Java%2022-25%20Features/9.%20Stream%20gatherers%20%28Java%2024%29.md)
  - [10. Other notable changes in Java 24-25](2.%20Modern%20Java%20Features/5.%20Java%2022-25%20Features/10.%20Other%20notable%20changes%20in%20Java%2024-25.md)
- **[6. JVM Languages & Interop](2.%20Modern%20Java%20Features/6.%20JVM%20Languages%20%26%20Interop)**
  - [1. Kotlin interoperability](2.%20Modern%20Java%20Features/6.%20JVM%20Languages%20%26%20Interop/1.%20Kotlin%20interoperability.md)
  - [2. Scala interoperability](2.%20Modern%20Java%20Features/6.%20JVM%20Languages%20%26%20Interop/2.%20Scala%20interoperability.md)
  - [3. Groovy in Java projects](2.%20Modern%20Java%20Features/6.%20JVM%20Languages%20%26%20Interop/3.%20Groovy%20in%20Java%20projects.md)
  - [4. GraalVM and native images](2.%20Modern%20Java%20Features/6.%20JVM%20Languages%20%26%20Interop/4.%20GraalVM%20and%20native%20images.md)
- **[7. Performance & Optimization](2.%20Modern%20Java%20Features/7.%20Performance%20%26%20Optimization)**
  - [1. JMH (Java Microbenchmark Harness)](2.%20Modern%20Java%20Features/7.%20Performance%20%26%20Optimization/1.%20JMH%20%28Java%20Microbenchmark%20Harness%29.md)
  - [2. Profiling techniques](2.%20Modern%20Java%20Features/7.%20Performance%20%26%20Optimization/2.%20Profiling%20techniques.md)
  - [3. Memory optimization strategies](2.%20Modern%20Java%20Features/7.%20Performance%20%26%20Optimization/3.%20Memory%20optimization%20strategies.md)
  - [4. CPU optimization techniques](2.%20Modern%20Java%20Features/7.%20Performance%20%26%20Optimization/4.%20CPU%20optimization%20techniques.md)
  - [5. Lazy initialization patterns](2.%20Modern%20Java%20Features/7.%20Performance%20%26%20Optimization/5.%20Lazy%20initialization%20patterns.md)
  - [6. String optimization](2.%20Modern%20Java%20Features/7.%20Performance%20%26%20Optimization/6.%20String%20optimization.md)
  - [7. Collection performance tuning](2.%20Modern%20Java%20Features/7.%20Performance%20%26%20Optimization/7.%20Collection%20performance%20tuning.md)
  - [8. Caching strategies](2.%20Modern%20Java%20Features/7.%20Performance%20%26%20Optimization/8.%20Caching%20strategies.md)
  - [9. Async and non-blocking optimization](2.%20Modern%20Java%20Features/7.%20Performance%20%26%20Optimization/9.%20Async%20and%20non-blocking%20optimization.md)
  - [10. JVM tuning for performance](2.%20Modern%20Java%20Features/7.%20Performance%20%26%20Optimization/10.%20JVM%20tuning%20for%20performance.md)

### [3. Enterprise Java](3.%20Enterprise%20Java)

- **[1. Design Patterns in Java](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java)**
  - [1. Creational patterns](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/1.%20Creational%20patterns.md)
  - [2. Structural patterns](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/2.%20Structural%20patterns.md)
  - [3. Behavioral patterns](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/3.%20Behavioral%20patterns.md)
  - [4. Concurrency patterns](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/4.%20Concurrency%20patterns.md)
  - [5. Functional patterns](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/5.%20Functional%20patterns.md)
  - [6. Anti-patterns to avoid](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/6.%20Anti-patterns%20to%20avoid.md)
  - [7. SOLID principles in Java](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/7.%20SOLID%20principles%20in%20Java.md)
  - [8. DRY, KISS, YAGNI principles](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/8.%20DRY%2C%20KISS%2C%20YAGNI%20principles.md)
  - [9. Dependency Injection patterns](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/9.%20Dependency%20Injection%20patterns.md)
  - [10. Resource management patterns](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/10.%20Resource%20management%20patterns.md)
  - [11. Error handling patterns](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/11.%20Error%20handling%20patterns.md)
  - [12. Testing patterns](3.%20Enterprise%20Java/1.%20Design%20Patterns%20in%20Java/12.%20Testing%20patterns.md)
- **[2. Testing & Quality](3.%20Enterprise%20Java/2.%20Testing%20%26%20Quality)**
  - [1. JUnit 5 advanced features](3.%20Enterprise%20Java/2.%20Testing%20%26%20Quality/1.%20JUnit%205%20advanced%20features.md)
  - [2. Mocking frameworks (Mockito, EasyMock)](3.%20Enterprise%20Java/2.%20Testing%20%26%20Quality/2.%20Mocking%20frameworks%20%28Mockito%2C%20EasyMock%29.md)
  - [3. Testing best practices](3.%20Enterprise%20Java/2.%20Testing%20%26%20Quality/3.%20Testing%20best%20practices.md)
  - [4. Integration testing strategies](3.%20Enterprise%20Java/2.%20Testing%20%26%20Quality/4.%20Integration%20testing%20strategies.md)
  - [5. Property-based testing](3.%20Enterprise%20Java/2.%20Testing%20%26%20Quality/5.%20Property-based%20testing.md)
  - [6. Mutation testing](3.%20Enterprise%20Java/2.%20Testing%20%26%20Quality/6.%20Mutation%20testing.md)
  - [7. Test coverage analysis](3.%20Enterprise%20Java/2.%20Testing%20%26%20Quality/7.%20Test%20coverage%20analysis.md)
  - [8. Performance testing](3.%20Enterprise%20Java/2.%20Testing%20%26%20Quality/8.%20Performance%20testing.md)
- **[3. Build Tools & Dependency Management](3.%20Enterprise%20Java/3.%20Build%20Tools%20%26%20Dependency%20Management)**
  - [1. Maven deep dive](3.%20Enterprise%20Java/3.%20Build%20Tools%20%26%20Dependency%20Management/1.%20Maven%20deep%20dive.md)
  - [2. Gradle fundamentals](3.%20Enterprise%20Java/3.%20Build%20Tools%20%26%20Dependency%20Management/2.%20Gradle%20fundamentals.md)
  - [3. Dependency management strategies](3.%20Enterprise%20Java/3.%20Build%20Tools%20%26%20Dependency%20Management/3.%20Dependency%20management%20strategies.md)
  - [4. Build optimization](3.%20Enterprise%20Java/3.%20Build%20Tools%20%26%20Dependency%20Management/4.%20Build%20optimization.md)
- **[4. Logging & Monitoring](3.%20Enterprise%20Java/4.%20Logging%20%26%20Monitoring)**
  - [1. Logging frameworks (SLF4J, Logback, Log4j2)](3.%20Enterprise%20Java/4.%20Logging%20%26%20Monitoring/1.%20Logging%20frameworks%20%28SLF4J%2C%20Logback%2C%20Log4j2%29.md)
  - [2. Effective logging strategies](3.%20Enterprise%20Java/4.%20Logging%20%26%20Monitoring/2.%20Effective%20logging%20strategies.md)
  - [3. Application monitoring](3.%20Enterprise%20Java/4.%20Logging%20%26%20Monitoring/3.%20Application%20monitoring.md)
  - [4. Distributed tracing](3.%20Enterprise%20Java/4.%20Logging%20%26%20Monitoring/4.%20Distributed%20tracing.md)
- **[5. Java Cryptography Architecture](3.%20Enterprise%20Java/5.%20Java%20Cryptography%20Architecture)**
  - [1. Java Cryptography Architecture (JCA)](3.%20Enterprise%20Java/5.%20Java%20Cryptography%20Architecture/1.%20Java%20Cryptography%20Architecture%20%28JCA%29.md)
  - [2. Secure coding practices](3.%20Enterprise%20Java/5.%20Java%20Cryptography%20Architecture/2.%20Secure%20coding%20practices.md)
  - [3. SSL and TLS in Java](3.%20Enterprise%20Java/5.%20Java%20Cryptography%20Architecture/3.%20SSL%20and%20TLS%20in%20Java.md)
  - [4. Java Security Manager (deprecated but important)](3.%20Enterprise%20Java/5.%20Java%20Cryptography%20Architecture/4.%20Java%20Security%20Manager%20%28deprecated%20but%20important%29.md)
  - [5. Deserialization vulnerabilities](3.%20Enterprise%20Java/5.%20Java%20Cryptography%20Architecture/5.%20Deserialization%20vulnerabilities.md)
  - [6. Dependency vulnerabilities](3.%20Enterprise%20Java/5.%20Java%20Cryptography%20Architecture/6.%20Dependency%20vulnerabilities.md)
- **[6. Code Quality and Maintainability](3.%20Enterprise%20Java/6.%20Code%20Quality%20and%20Maintainability)**
  - [1. Static analysis tools](3.%20Enterprise%20Java/6.%20Code%20Quality%20and%20Maintainability/1.%20Static%20analysis%20tools.md)
  - [2. Code smells and refactoring](3.%20Enterprise%20Java/6.%20Code%20Quality%20and%20Maintainability/2.%20Code%20smells%20and%20refactoring.md)
  - [3. Clean code principles](3.%20Enterprise%20Java/6.%20Code%20Quality%20and%20Maintainability/3.%20Clean%20code%20principles.md)
  - [4. Documentation strategies](3.%20Enterprise%20Java/6.%20Code%20Quality%20and%20Maintainability/4.%20Documentation%20strategies.md)
  - [5. Code review best practices](3.%20Enterprise%20Java/6.%20Code%20Quality%20and%20Maintainability/5.%20Code%20review%20best%20practices.md)
  - [6. Technical debt management](3.%20Enterprise%20Java/6.%20Code%20Quality%20and%20Maintainability/6.%20Technical%20debt%20management.md)

### [4. Specialized Topics](4.%20Specialized%20Topics)

- **[1. Functional Programming in Java](4.%20Specialized%20Topics/1.%20Functional%20Programming%20in%20Java)**
  - [1. Pure functions and immutability](4.%20Specialized%20Topics/1.%20Functional%20Programming%20in%20Java/1.%20Pure%20functions%20and%20immutability.md)
  - [2. Higher-order functions](4.%20Specialized%20Topics/1.%20Functional%20Programming%20in%20Java/2.%20Higher-order%20functions.md)
  - [3. Monads in Java](4.%20Specialized%20Topics/1.%20Functional%20Programming%20in%20Java/3.%20Monads%20in%20Java.md)
  - [4. Functional error handling](4.%20Specialized%20Topics/1.%20Functional%20Programming%20in%20Java/4.%20Functional%20error%20handling.md)
  - [5. Lazy evaluation](4.%20Specialized%20Topics/1.%20Functional%20Programming%20in%20Java/5.%20Lazy%20evaluation.md)
  - [6. Functional libraries (Vavr, Guava)](4.%20Specialized%20Topics/1.%20Functional%20Programming%20in%20Java/6.%20Functional%20libraries%20%28Vavr%2C%20Guava%29.md)
- **[2. Reactive Programming](4.%20Specialized%20Topics/2.%20Reactive%20Programming)**
  - [1. Reactive Streams specification](4.%20Specialized%20Topics/2.%20Reactive%20Programming/1.%20Reactive%20Streams%20specification.md)
  - [2. Project Reactor fundamentals](4.%20Specialized%20Topics/2.%20Reactive%20Programming/2.%20Project%20Reactor%20fundamentals.md)
  - [3. RxJava patterns](4.%20Specialized%20Topics/2.%20Reactive%20Programming/3.%20RxJava%20patterns.md)
  - [4. Reactive design patterns](4.%20Specialized%20Topics/2.%20Reactive%20Programming/4.%20Reactive%20design%20patterns.md)
  - [5. Reactive vs imperative](4.%20Specialized%20Topics/2.%20Reactive%20Programming/5.%20Reactive%20vs%20imperative.md)
  - [6. Testing reactive code](4.%20Specialized%20Topics/2.%20Reactive%20Programming/6.%20Testing%20reactive%20code.md)
- **[3. Microservices Patterns](4.%20Specialized%20Topics/3.%20Microservices%20Patterns)**
  - [1. Service communication](4.%20Specialized%20Topics/3.%20Microservices%20Patterns/1.%20Service%20communication.md)
  - [2. Service discovery and load balancing](4.%20Specialized%20Topics/3.%20Microservices%20Patterns/2.%20Service%20discovery%20and%20load%20balancing.md)
  - [3. Resilience patterns](4.%20Specialized%20Topics/3.%20Microservices%20Patterns/3.%20Resilience%20patterns.md)
  - [4. Distributed transactions](4.%20Specialized%20Topics/3.%20Microservices%20Patterns/4.%20Distributed%20transactions.md)
  - [5. Configuration management](4.%20Specialized%20Topics/3.%20Microservices%20Patterns/5.%20Configuration%20management.md)
  - [6. Observability in microservices](4.%20Specialized%20Topics/3.%20Microservices%20Patterns/6.%20Observability%20in%20microservices.md)
- **[4. Data Structures & Algorithms](4.%20Specialized%20Topics/4.%20Data%20Structures%20%26%20Algorithms)**
  - [1. Tree structures](4.%20Specialized%20Topics/4.%20Data%20Structures%20%26%20Algorithms/1.%20Tree%20structures.md)
  - [2. Graph algorithms](4.%20Specialized%20Topics/4.%20Data%20Structures%20%26%20Algorithms/2.%20Graph%20algorithms.md)
  - [3. Sorting algorithms](4.%20Specialized%20Topics/4.%20Data%20Structures%20%26%20Algorithms/3.%20Sorting%20algorithms.md)
  - [4. Search algorithms](4.%20Specialized%20Topics/4.%20Data%20Structures%20%26%20Algorithms/4.%20Search%20algorithms.md)
  - [5. Dynamic programming patterns](4.%20Specialized%20Topics/4.%20Data%20Structures%20%26%20Algorithms/5.%20Dynamic%20programming%20patterns.md)
  - [6. Advanced data structures](4.%20Specialized%20Topics/4.%20Data%20Structures%20%26%20Algorithms/6.%20Advanced%20data%20structures.md)
  - [7. String algorithms](4.%20Specialized%20Topics/4.%20Data%20Structures%20%26%20Algorithms/7.%20String%20algorithms.md)
  - [8. Bit manipulation](4.%20Specialized%20Topics/4.%20Data%20Structures%20%26%20Algorithms/8.%20Bit%20manipulation.md)
- **[5. System Design](4.%20Specialized%20Topics/5.%20System%20Design)**
  - [1. Scalability fundamentals](4.%20Specialized%20Topics/5.%20System%20Design/1.%20Scalability%20fundamentals.md)
  - [2. Database design decisions](4.%20Specialized%20Topics/5.%20System%20Design/2.%20Database%20design%20decisions.md)
  - [3. Caching strategies](4.%20Specialized%20Topics/5.%20System%20Design/3.%20Caching%20strategies.md)
  - [4. Message queues and event streaming](4.%20Specialized%20Topics/5.%20System%20Design/4.%20Message%20queues%20and%20event%20streaming.md)
  - [5. Rate limiting and throttling](4.%20Specialized%20Topics/5.%20System%20Design/5.%20Rate%20limiting%20and%20throttling.md)
  - [6. High availability and disaster recovery](4.%20Specialized%20Topics/5.%20System%20Design/6.%20High%20availability%20and%20disaster%20recovery.md)

### [5. Interviews & Soft Skills](5.%20Interviews%20%26%20Soft%20Skills)

- **[1. Coding Interview Patterns](5.%20Interviews%20%26%20Soft%20Skills/1.%20Coding%20Interview%20Patterns)**
  - [1. Two pointers technique](5.%20Interviews%20%26%20Soft%20Skills/1.%20Coding%20Interview%20Patterns/1.%20Two%20pointers%20technique.md)
  - [2. Sliding window](5.%20Interviews%20%26%20Soft%20Skills/1.%20Coding%20Interview%20Patterns/2.%20Sliding%20window.md)
  - [3. Fast and slow pointers](5.%20Interviews%20%26%20Soft%20Skills/1.%20Coding%20Interview%20Patterns/3.%20Fast%20and%20slow%20pointers.md)
  - [4. Merge intervals](5.%20Interviews%20%26%20Soft%20Skills/1.%20Coding%20Interview%20Patterns/4.%20Merge%20intervals.md)
  - [5. Cyclic sort](5.%20Interviews%20%26%20Soft%20Skills/1.%20Coding%20Interview%20Patterns/5.%20Cyclic%20sort.md)
  - [6. In-place reversal of linked list](5.%20Interviews%20%26%20Soft%20Skills/1.%20Coding%20Interview%20Patterns/6.%20In-place%20reversal%20of%20linked%20list.md)
  - [7. Tree BFS and DFS](5.%20Interviews%20%26%20Soft%20Skills/1.%20Coding%20Interview%20Patterns/7.%20Tree%20BFS%20and%20DFS.md)
  - [8. Backtracking](5.%20Interviews%20%26%20Soft%20Skills/1.%20Coding%20Interview%20Patterns/8.%20Backtracking.md)
  - [9. Top K elements](5.%20Interviews%20%26%20Soft%20Skills/1.%20Coding%20Interview%20Patterns/9.%20Top%20K%20elements.md)
  - [10. Modified binary search](5.%20Interviews%20%26%20Soft%20Skills/1.%20Coding%20Interview%20Patterns/10.%20Modified%20binary%20search.md)
- **[2. System Design Interview Prep](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep)**
  - [1. URL shortener design](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep/1.%20URL%20shortener%20design.md)
  - [2. Twitter&social media feed design](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep/2.%20Twitter%26social%20media%20feed%20design.md)
  - [3. Rate limiter design](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep/3.%20Rate%20limiter%20design.md)
  - [4. Web crawler design](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep/4.%20Web%20crawler%20design.md)
  - [5. Chat system design](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep/5.%20Chat%20system%20design.md)
  - [6. File storage system](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep/6.%20File%20storage%20system.md)
  - [7. Video streaming platform](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep/7.%20Video%20streaming%20platform.md)
  - [8. Distributed cache design](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep/8.%20Distributed%20cache%20design.md)
  - [9. Distributed message queue design (Kafka)](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep/9.%20Distributed%20message%20queue%20design%20%28Kafka%29.md)
  - [10. Distributed task queue design (RabbitMQ)](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep/10.%20Distributed%20task%20queue%20design%20%28RabbitMQ%29.md)
  - [11. Real-time messaging system design (NATS)](5.%20Interviews%20%26%20Soft%20Skills/2.%20System%20Design%20Interview%20Prep/11.%20Real-time%20messaging%20system%20design%20%28NATS%29.md)
- **[3. Behavioral Interview Questions](5.%20Interviews%20%26%20Soft%20Skills/3.%20Behavioral%20Interview%20Questions)**
  - [1. Leadership and mentorship](5.%20Interviews%20%26%20Soft%20Skills/3.%20Behavioral%20Interview%20Questions/1.%20Leadership%20and%20mentorship.md)
  - [2. Problem-solving and debugging](5.%20Interviews%20%26%20Soft%20Skills/3.%20Behavioral%20Interview%20Questions/2.%20Problem-solving%20and%20debugging.md)
  - [3. Collaboration and communication](5.%20Interviews%20%26%20Soft%20Skills/3.%20Behavioral%20Interview%20Questions/3.%20Collaboration%20and%20communication.md)
  - [4. Project delivery and management](5.%20Interviews%20%26%20Soft%20Skills/3.%20Behavioral%20Interview%20Questions/4.%20Project%20delivery%20and%20management.md)
  - [5. Growth and learning](5.%20Interviews%20%26%20Soft%20Skills/3.%20Behavioral%20Interview%20Questions/5.%20Growth%20and%20learning.md)
  - [6. Handling pressure and failure](5.%20Interviews%20%26%20Soft%20Skills/3.%20Behavioral%20Interview%20Questions/6.%20Handling%20pressure%20and%20failure.md)
- **[4. Architecture and Design Interview](5.%20Interviews%20%26%20Soft%20Skills/4.%20Architecture%20and%20Design%20Interview)**
  - [1. Monolith to microservices migration](5.%20Interviews%20%26%20Soft%20Skills/4.%20Architecture%20and%20Design%20Interview/1.%20Monolith%20to%20microservices%20migration.md)
  - [2. Event-driven architecture design](5.%20Interviews%20%26%20Soft%20Skills/4.%20Architecture%20and%20Design%20Interview/2.%20Event-driven%20architecture%20design.md)
  - [3. API design principles](5.%20Interviews%20%26%20Soft%20Skills/4.%20Architecture%20and%20Design%20Interview/3.%20API%20design%20principles.md)
  - [4. Database architecture decisions](5.%20Interviews%20%26%20Soft%20Skills/4.%20Architecture%20and%20Design%20Interview/4.%20Database%20architecture%20decisions.md)
  - [5. Performance architecture](5.%20Interviews%20%26%20Soft%20Skills/4.%20Architecture%20and%20Design%20Interview/5.%20Performance%20architecture.md)
  - [6. Security architecture](5.%20Interviews%20%26%20Soft%20Skills/4.%20Architecture%20and%20Design%20Interview/6.%20Security%20architecture.md)

<!-- toc:end -->

---

## Topic Outline

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

### Part II: Modern Java Features

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
- String templates (preview in Java 21–22, withdrawn in Java 23 — not part of the language)

**Section 5: Java 22-25 Features**

- Unnamed variables and patterns (final in Java 22)
- Flexible constructor bodies / statements before super() (final in Java 25)
- Foreign Function & Memory API (final in Java 22)
- Structured concurrency (still preview in Java 25)
- Module import declarations (final in Java 25)
- Scoped values (final in Java 25)
- Class-file API (final in Java 24)
- Compact source files and instance main methods (final in Java 25)
- Stream gatherers (final in Java 24)
- Other notable Java 24–25 changes (virtual threads without pinning, AOT cache, compact object headers, …)

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

### Part III: Enterprise Java

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

### Part IV: Specialized Topics

**Section 1: Functional Programming in Java**

- Pure functions and immutability
- Higher-order functions
- Monads in Java
- Functional error handling
- Lazy evaluation
- Functional libraries (Vavr, Guava)

**Section 2: Reactive Programming**

- Reactive Streams specification
- Project Reactor fundamentals
- RxJava patterns
- Reactive design patterns
- Reactive vs imperative
- Testing reactive code

**Section 3: Microservices Patterns**

- Service communication
- Service discovery and load balancing
- Resilience patterns
- Distributed transactions
- Configuration management
- Observability in microservices

**Section 4: Data Structures & Algorithms**

- Tree structures
- Graph algorithms
- Sorting algorithms
- Search algorithms
- Dynamic programming patterns
- Advanced data structures
- String algorithms
- Bit manipulation

**Section 5: System Design**

- Scalability fundamentals
- Database design decisions
- Caching strategies
- Message queues and event streaming (Kafka, RabbitMQ, SQS, NATS)
- Rate limiting and throttling
- High availability and disaster recovery

Broker-specific guides for Apache Kafka, RabbitMQ and NATS (Spring Boot setup, consumers, error handling, reliability, testing) are in the [Message Brokers](../Message%20Brokers/README.md) section.

---

### Part V: Interviews & Soft Skills

**Section 1: Coding Interview Patterns**

- Two pointers technique
- Sliding window
- Fast and slow pointers
- Merge intervals
- Cyclic sort
- In-place reversal of linked list
- Tree BFS and DFS
- Backtracking
- Top K elements
- Modified binary search

**Section 2: System Design Interview Prep**

- URL shortener design
- Twitter/social media feed design
- Rate limiter design
- Web crawler design
- Chat system design
- File storage system (Dropbox/Google Drive)
- Video streaming platform (YouTube/Netflix)
- Distributed cache design
- Distributed message queue design (Kafka)
- Distributed task queue design (RabbitMQ)
- Real-time messaging system design (NATS)

**Section 3: Behavioral Interview Questions**

- Leadership and mentorship
- Problem-solving and debugging
- Collaboration and communication
- Project delivery and management
- Growth and learning
- Handling pressure and failure

**Section 4: Architecture & Design Interview**

- Monolith to microservices migration
- Event-driven architecture design
- API design principles
- Database architecture decisions
- Performance architecture
- Security architecture

---

## Contributing

Found an error, have a better example, or want to add a missing section? See the [Contributing Guide](../CONTRIBUTING.md).
