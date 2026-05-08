
# 1. Java Thread Creation and Lifecycle


## Summary

### Thread Creation Methods

|Method|Pros|Cons|Use When|
|---|---|---|---|
|Extend Thread|Simple|Single inheritance, tight coupling|Simple scripts, learning|
|Implement Runnable|Flexible, reusable|No return value|Most production code|
|Implement Callable|Returns result, throws exceptions|Needs ExecutorService|Tasks with results|
|Virtual Thread|Massively scalable, cheap|Java 19+, pinning issues|I/O-bound apps|

### Thread States

```
NEW → start() → RUNNABLE ⇄ BLOCKED (waiting for lock)
                   ↕
              WAITING (wait(), join(), park())
                   ↕
         TIMED_WAITING (sleep(), wait(timeout))
                   ↓
              TERMINATED
```

### Key Differences

**sleep() vs wait():**

- sleep(): Pauses thread, keeps lock, static method
- wait(): Releases lock, instance method, needs synchronized

**join() vs wait():**

- join(): Wait for thread completion
- wait(): Wait for notification

**Daemon vs User:**

- Daemon: Background, JVM can exit
- User: Foreground, JVM waits

**Platform vs Virtual:**

- Platform: OS thread, heavy (MB), thousands
- Virtual: JVM thread, light (KB), millions

### Best Practices

**Thread Creation:**

1. ✅ Prefer Runnable/Callable over extending Thread
2. ✅ Use ExecutorService for thread management
3. ✅ Use virtual threads for I/O-bound tasks (Java 19+)
4. ✅ Use lambdas for simple tasks
5. ❌ Don't create unlimited threads
6. ❌ Don't call run() directly

**Thread Coordination:**

1. ✅ Always handle InterruptedException
2. ✅ Use join() to wait for completion
3. ✅ Use wait()/notify() for communication
4. ✅ Consider CountDownLatch for multiple threads
5. ❌ Don't use Thread.yield() for coordination
6. ❌ Don't rely on thread priorities

**Virtual Threads:**

1. ✅ Use for I/O-bound workloads
2. ✅ Use ReentrantLock instead of synchronized
3. ✅ Create per-task (don't pool)
4. ✅ Keep synchronized blocks short
5. ❌ Don't use for CPU-bound work
6. ❌ Don't use ThreadLocal extensively

---

# 2. Java Executor Framework and Thread Pools


## Summary

### Quick Reference

**Executor Types:**

```java
// Fixed pool (bounded threads, unbounded queue)
Executors.newFixedThreadPool(10);

// Cached pool (unbounded threads, no queue)
Executors.newCachedThreadPool();

// Single thread (sequential execution)
Executors.newSingleThreadExecutor();

// Scheduled (delayed/periodic tasks)
Executors.newScheduledThreadPool(5);

// Work-stealing (divide-and-conquer)
new ForkJoinPool();
```

**ThreadPoolExecutor Parameters:**

- corePoolSize: Minimum threads
- maximumPoolSize: Maximum threads
- keepAliveTime: Idle thread timeout
- workQueue: Task queue
- threadFactory: Thread creation
- handler: Rejection policy

**Queue Types:**

- LinkedBlockingQueue: Optionally bounded, good concurrency
- ArrayBlockingQueue: Bounded, fixed memory, optional fairness
- SynchronousQueue: No capacity, direct handoff
- PriorityBlockingQueue: Priority ordering
- DelayQueue: Delayed execution

**Rejection Policies:**

- AbortPolicy: Throw exception (default)
- CallerRunsPolicy: Run in caller thread
- DiscardPolicy: Silent discard
- DiscardOldestPolicy: Discard oldest

**Thread Pool Sizing:**

- CPU-bound: cores + 1
- I/O-bound: cores × (1 + W/C)
- Web server: cores × 10
- Microservice: cores × 20

### Best Practices

1. ✅ Use ExecutorService over manual thread creation
2. ✅ Always shutdown executors (try-with-resources in Java 19+)
3. ✅ Set meaningful thread names (custom ThreadFactory)
4. ✅ Use bounded queues for production (prevent OOM)
5. ✅ Handle RejectedExecutionException
6. ✅ Monitor pool metrics (size, queue, rejections)
7. ✅ Separate pools for different workloads
8. ❌ Don't use CachedThreadPool for long-running tasks
9. ❌ Don't use unbounded queue with corePoolSize = maximumPoolSize
10. ❌ Don't forget to configure rejection policy

---

# 3. Java CompletableFuture and Async Programming


## Summary

### Quick Reference

**Creating CompletableFuture:**

```java
// Async with return value
CompletableFuture.supplyAsync(() -> compute());

// Async without return value
CompletableFuture.runAsync(() -> doWork());

// With custom executor
CompletableFuture.supplyAsync(() -> compute(), executor);

// Already completed
CompletableFuture.completedFuture(value);
```

**Chaining Operations:**

```java
// Transform (Function<T, R>)
.thenApply(result -> transform(result))

// Consume (Consumer<T>)
.thenAccept(result -> consume(result))

// Execute (Runnable)
.thenRun(() -> doSomething())

// Async variants
.thenApplyAsync(...)
.thenAcceptAsync(...)
.thenRunAsync(...)
```

**Combining Futures:**

```java
// Parallel combination
future1.thenCombine(future2, (r1, r2) -> combine(r1, r2))

// Sequential composition
future.thenCompose(result -> fetchMore(result))

// Wait for all
CompletableFuture.allOf(f1, f2, f3)

// First to complete
CompletableFuture.anyOf(f1, f2, f3)
```

**Exception Handling:**

```java
// Provide fallback
.exceptionally(ex -> fallbackValue)

// Handle both success and failure
.handle((result, ex) -> ...)

// Side effects only
.whenComplete((result, ex) -> ...)

// Timeout (Java 9+)
.orTimeout(2, TimeUnit.SECONDS)
.completeOnTimeout(defaultValue, 2, TimeUnit.SECONDS)
```

### Method Comparison

|Method|Input|Output|Use Case|
|---|---|---|---|
|thenApply|Function<T,R>|CompletableFuture<R>|Transform|
|thenAccept|Consumer<T>|CompletableFuture<Void>|Side effect|
|thenRun|Runnable|CompletableFuture<Void>|Just execute|
|thenCombine|BiFunction|CompletableFuture<R>|Parallel combine|
|thenCompose|Function returning CF|CompletableFuture<R>|Sequential chain|
|exceptionally|Function<Throwable,T>|CompletableFuture<T>|Error recovery|
|handle|BiFunction<T,Throwable,R>|CompletableFuture<R>|Handle both|

### Best Practices

1. ✅ Use async methods for I/O-bound operations
2. ✅ Chain operations instead of blocking with get()
3. ✅ Use custom executors for blocking I/O
4. ✅ Handle exceptions with exceptionally/handle
5. ✅ Use allOf/anyOf for multiple futures
6. ✅ Avoid blocking common pool (use dedicated executor)
7. ❌ Don't call get() in the middle of chain
8. ❌ Don't use blocking calls in async callbacks
9. ❌ Don't ignore exceptions
10. ❌ Don't join() in loops (start all, then wait for all)

### Performance Tips

**Parallel vs Sequential:**

- 3 independent 1-second operations:
    - Sequential: 3 seconds
    - Parallel (CompletableFuture): 1 second
    - **3x speedup!**

**Avoid Blocking:**

```java
// ❌ BAD: 5 seconds total
for (String id : ids) {
    CompletableFuture.supplyAsync(() -> fetch(id)).join();
}

// ✅ GOOD: 1 second total
List<CF<String>> futures = ids.stream()
    .map(id -> CompletableFuture.supplyAsync(() -> fetch(id)))
    .collect(toList());
CompletableFuture.allOf(futures.toArray(new CF[0])).join();
```

---

# 4. Java Lock Implementations


## Summary

### Lock Type Comparison

```
┌─────────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│ Lock Type       │ Complexity   │ Performance  │ Use Case     │ Features     │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ synchronized    │ Simple       │ Good         │ General      │ Automatic    │
│ ReentrantLock   │ Medium       │ Good-Better  │ Advanced     │ tryLock,     │
│                 │              │              │ needs        │ timeout      │
│ ReadWriteLock   │ Medium       │ Better       │ Read-heavy   │ Read/write   │
│                 │              │              │ (>80% read)  │ separation   │
│ StampedLock     │ Complex      │ Best         │ Very read-   │ Optimistic   │
│                 │              │              │ heavy (>95%) │ reads        │
│ Lock-free (CAS) │ Very Complex │ Best         │ High         │ Non-blocking │
│                 │              │              │ contention   │              │
└─────────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

### Quick Reference

**ReentrantLock:**

```java
Lock lock = new ReentrantLock();
lock.lock();
try {
    // Critical section
} finally {
    lock.unlock();  // Always in finally!
}

// Try lock with timeout
if (lock.tryLock(2, TimeUnit.SECONDS)) {
    try {
        // Got lock
    } finally {
        lock.unlock();
    }
}
```

**ReadWriteLock:**

```java
ReadWriteLock rwLock = new ReentrantReadWriteLock();

// Read
rwLock.readLock().lock();
try {
    // Read data (multiple readers OK)
} finally {
    rwLock.readLock().unlock();
}

// Write
rwLock.writeLock().lock();
try {
    // Write data (exclusive)
} finally {
    rwLock.writeLock().unlock();
}
```

**StampedLock:**

```java
StampedLock lock = new StampedLock();

// Optimistic read (fastest)
long stamp = lock.tryOptimisticRead();
// Read data
if (!lock.validate(stamp)) {
    // Validation failed, get real lock
    stamp = lock.readLock();
    try {
        // Re-read data
    } finally {
        lock.unlockRead(stamp);
    }
}
```

**Lock-Free:**

```java
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();  // Lock-free

AtomicReference<Node> head = new AtomicReference<>();
head.compareAndSet(expected, newValue);  // CAS
```

### Performance Summary

**Read-Heavy Workload (95% reads):**

- synchronized: Baseline
- ReadWriteLock: 4-5x faster
- StampedLock: 8-10x faster
- **Winner: StampedLock**

**Write-Heavy Workload (50% writes):**

- synchronized: Baseline
- ReadWriteLock: 1.1x faster
- ReentrantLock: 1.2x faster
- **Winner: synchronized (simplicity)**

**High Contention:**

- synchronized: Baseline
- Lock-free (CAS): 2-3x faster
- **Winner: Lock-free**

### Best Practices

1. ✅ Default to `synchronized` for simplicity
2. ✅ Use `ReentrantLock` when need tryLock, timeout, or fairness
3. ✅ Use `ReadWriteLock` for read-heavy (>80% reads)
4. ✅ Use `StampedLock` for very read-heavy (>95% reads)
5. ✅ Use lock-free (AtomicXxx) for simple counters/flags
6. ✅ Always unlock in `finally` block
7. ❌ Don't forget to unlock (use try-finally)
8. ❌ Don't use fair locks unless necessary (10x slower)
9. ❌ Don't use `StampedLock` with `Condition` (not supported)
10. ❌ Don't optimize prematurely - measure first!

---

# 5. Java Concurrent Collections Deep Dive


## Summary

### Quick Reference

**Maps:**

```java
// General purpose, best performance
ConcurrentHashMap<K, V> map = new ConcurrentHashMap<>();

// Sorted, range queries
ConcurrentSkipListMap<K, V> sorted = new ConcurrentSkipListMap<>();
```

**Lists:**

```java
// Read-heavy (>95% reads), small lists
CopyOnWriteArrayList<E> list = new CopyOnWriteArrayList<>();

// Write-heavy or large lists
List<E> list = Collections.synchronizedList(new ArrayList<>());
```

**Queues:**

```java
// Blocking, producer-consumer
BlockingQueue<E> queue = new LinkedBlockingQueue<>();

// Non-blocking, high throughput
ConcurrentLinkedQueue<E> queue = new ConcurrentLinkedQueue<>();

// Priority ordering
PriorityBlockingQueue<E> queue = new PriorityBlockingQueue<>();

// Delayed elements
DelayQueue<E> queue = new DelayQueue<>();
```

### Performance Summary

**ConcurrentHashMap:**

- 4-5x faster than Hashtable/SynchronizedMap
- O(1) operations
- Best general-purpose concurrent map

**CopyOnWriteArrayList:**

- 4x faster than SynchronizedList (read-heavy)
- Lock-free reads
- Expensive writes (copies entire array)

**LinkedBlockingQueue:**

- 1.6x faster than ArrayBlockingQueue
- Two locks (better concurrency)
- Good for producer-consumer

**ConcurrentLinkedQueue:**

- 1.5x faster than LinkedBlockingQueue
- Lock-free (CAS-based)
- Best for non-blocking scenarios

**ConcurrentSkipListMap:**

- 3x faster than synchronized TreeMap
- O(log n) operations
- Best for sorted concurrent access

### Best Practices

1. ✅ Use ConcurrentHashMap for general maps (not Hashtable)
2. ✅ Use CopyOnWriteArrayList for event listeners
3. ✅ Use LinkedBlockingQueue for producer-consumer
4. ✅ Use ConcurrentLinkedQueue for non-blocking queues
5. ✅ Use ConcurrentSkipListMap for sorted maps
6. ❌ Don't use Hashtable or Vector (legacy, slow)
7. ❌ Don't use CopyOnWriteArrayList for write-heavy
8. ❌ Don't synchronize HashMap manually (use ConcurrentHashMap)

---

# 6. Java Atomic Classes and CAS Operations


## Summary

### Quick Reference

**Basic Atomic Classes:**

```java
// Integer counter
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();  // Returns new value
counter.getAndIncrement();  // Returns old value
counter.addAndGet(5);

// Long counter
AtomicLong longCounter = new AtomicLong(0L);

// Object reference
AtomicReference<String> ref = new AtomicReference<>("initial");
ref.compareAndSet("initial", "updated");
```

**Compare-And-Swap:**

```java
AtomicInteger value = new AtomicInteger(10);

// CAS: if current == 10, set to 20
boolean success = value.compareAndSet(10, 20);

// CAS loop pattern
int current, next;
do {
    current = value.get();
    next = computeNewValue(current);
} while (!value.compareAndSet(current, next));
```

**ABA Problem Solutions:**

```java
// Version stamping
AtomicStampedReference<Node> ref = 
    new AtomicStampedReference<>(node, 0);

int[] stampHolder = new int[1];
Node value = ref.get(stampHolder);
int stamp = stampHolder[0];

ref.compareAndSet(value, newValue, stamp, stamp + 1);

// Boolean marking
AtomicMarkableReference<Node> markable = 
    new AtomicMarkableReference<>(node, false);
```

**High Contention:**

```java
// Use LongAdder instead of AtomicLong
LongAdder adder = new LongAdder();
adder.increment();
long sum = adder.sum();

// 10x faster under high contention!
```

**FieldUpdater:**

```java
// For existing classes
class User {
    private volatile int count;
}

AtomicIntegerFieldUpdater<User> updater =
    AtomicIntegerFieldUpdater.newUpdater(User.class, "count");

updater.incrementAndGet(user);
```

### Performance Summary

**Single Thread:**

```
AtomicInteger:   250ms
LongAdder:       250ms  (same)
synchronized:    250ms  (same)
```

**High Contention (20 threads):**

```
LongAdder:       900ms   (baseline)
AtomicInteger:   8500ms  (9.4x slower)
synchronized:    11000ms (12.2x slower)
```

**Ranking:**

1. **LongAdder** - Best for high contention
2. **AtomicInteger** - Good for low contention
3. **ReentrantLock** - Flexible but slower
4. **synchronized** - Simplest but slowest

### Decision Guide

**Choose AtomicInteger/Long:**

- Low contention (<5 threads)
- Need exact value frequently
- Simple counter/flag

**Choose LongAdder:**

- High contention (>10 threads)
- Update-heavy workload
- Statistics/metrics

**Choose AtomicReference:**

- Thread-safe object updates
- Immutable object swapping
- Lock-free algorithms

**Choose AtomicStampedReference:**

- Need ABA protection
- Version tracking important
- Complex state changes

**Choose FieldUpdater:**

- Large object arrays
- Retrofit existing classes
- Memory constrained

### Best Practices

1. ✅ Use LongAdder for high-contention counters
2. ✅ Use AtomicInteger for simple, low-contention cases
3. ✅ Cache local copies for multiple reads
4. ✅ Batch updates when possible (add(1000) vs 1000x increment())
5. ✅ Use FieldUpdater for large object collections
6. ✅ Protect against ABA with stamped/markable references
7. ❌ Don't use synchronized for counters (use atomic)
8. ❌ Don't repeat expensive operations in CAS loop
9. ❌ Don't forget volatile for FieldUpdater fields
10. ❌ Don't use AtomicLong when LongAdder is better

---

# 7. Java Synchronizers


## Summary

### Quick Reference

**CountDownLatch:**

```java
CountDownLatch latch = new CountDownLatch(3);

// Workers
latch.countDown();  // Decrement count

// Main thread
latch.await();  // Wait until count = 0

// With timeout
boolean done = latch.await(5, TimeUnit.SECONDS);
```

**CyclicBarrier:**

```java
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("Barrier action");
});

// Each worker
barrier.await();  // Wait for all parties

// Reusable for multiple cycles
```

**Semaphore:**

```java
Semaphore semaphore = new Semaphore(5);  // 5 permits

semaphore.acquire();  // Get permit (blocks if none)
try {
    // Use resource
} finally {
    semaphore.release();  // Return permit
}

// Non-blocking
if (semaphore.tryAcquire(1, TimeUnit.SECONDS)) {
    // Got permit
}
```

**Phaser:**

```java
Phaser phaser = new Phaser(3);  // 3 parties

// Each party
phaser.arriveAndAwaitAdvance();  // Wait at phase boundary

// Dynamic
phaser.register();  // Add party
phaser.arriveAndDeregister();  // Remove party
```

**Exchanger:**

```java
Exchanger<Buffer> exchanger = new Exchanger<>();

// Thread 1
Buffer myBuffer = fullBuffer;
Buffer emptyBuffer = exchanger.exchange(myBuffer);

// Thread 2
Buffer myBuffer = emptyBuffer;
Buffer fullBuffer = exchanger.exchange(myBuffer);
```

### Best Practices

1. ✅ Use CountDownLatch for one-time coordination
2. ✅ Use CyclicBarrier for iterative algorithms
3. ✅ Use Semaphore for resource pools (always release in finally!)
4. ✅ Use Phaser for dynamic parties or complex multi-phase
5. ✅ Use Exchanger for efficient buffer swapping
6. ✅ Handle InterruptedException properly
7. ✅ Use timeout variants to prevent indefinite blocking
8. ❌ Don't reuse CountDownLatch (use CyclicBarrier instead)
9. ❌ Don't forget to release semaphore permits
10. ❌ Don't use Exchanger for >2 threads

### Common Patterns

**Application Startup:**

```java
CountDownLatch startupLatch = new CountDownLatch(3);
startDatabase().thenRun(startupLatch::countDown);
startCache().thenRun(startupLatch::countDown);
startWebServer().thenRun(startupLatch::countDown);
startupLatch.await();
```

**Connection Pool:**

```java
Semaphore available = new Semaphore(maxConnections);
Connection conn = getConnection() {
    available.acquire();
    return pool.get();
}
void release(Connection conn) {
    pool.put(conn);
    available.release();
}
```

**Parallel Computation:**

```java
CyclicBarrier barrier = new CyclicBarrier(workers);
for (phase = 0; phase < iterations; phase++) {
    doWork();
    barrier.await();  // Synchronize after each phase
}
```

---

# 8. Java ThreadLocal and Context Propagation


## Summary

### Quick Reference

**Basic ThreadLocal:**

```java
ThreadLocal<String> context = ThreadLocal.withInitial(() -> "default");

// Set value
context.set("my-value");

// Get value
String value = context.get();

// CRITICAL: Always clean up
context.remove();
```

**With try-finally:**

```java
try {
    threadLocal.set(value);
    // use value
} finally {
    threadLocal.remove();  // ALWAYS
}
```

**InheritableThreadLocal:**

```java
InheritableThreadLocal<String> context = new InheritableThreadLocal<>();
context.set("parent-value");

new Thread(() -> {
    System.out.println(context.get());  // Inherits parent-value
}).start();
```

**Context propagation:**

```java
// Capture before async
String captured = threadLocal.get();

CompletableFuture.runAsync(() -> {
    try {
        threadLocal.set(captured);  // Restore
        // work
    } finally {
        threadLocal.remove();  // Clean up
    }
});
```

**MDC pattern:**

```java
try {
    MDC.put("requestId", requestId);
    MDC.put("userId", userId);
    // logging will include context
} finally {
    MDC.clear();
}
```

### Memory Leak Prevention

**CRITICAL RULES:**

1. ✅ **ALWAYS call remove()** in finally block
2. ✅ **Use try-finally** pattern without exception
3. ✅ **Clean up in thread pools** (threads reused!)
4. ✅ **Propagate context** to async threads explicitly
5. ❌ **NEVER forget remove()** - leads to OutOfMemoryError
6. ❌ **Don't rely on GC** - strong reference keeps values alive
7. ❌ **Don't use InheritableThreadLocal** with thread pools

### Best Practices

**Pattern 1: Always clean up**

```java
// CORRECT
try {
    threadLocal.set(value);
    doWork();
} finally {
    threadLocal.remove();
}

// WRONG - Memory leak!
threadLocal.set(value);
doWork();
```

**Pattern 2: AutoCloseable**

```java
try (Context ctx = new Context(value)) {
    // work
}  // Auto cleanup
```

**Pattern 3: Wrapper**

```java
contextWrapper.runWithContext(value, () -> {
    // work
});  // Auto cleanup
```

**Pattern 4: Async propagation**

```java
Map<String, String> context = MDC.getCopyOfContextMap();

CompletableFuture.runAsync(() -> {
    try {
        MDC.setContextMap(context);
        work();
    } finally {
        MDC.clear();
    }
});
```

### Common Pitfalls

**❌ Pitfall 1: Forgetting remove()**

```java
// WRONG
public void handleRequest() {
    userContext.set(user);
    process();
    // Missing: userContext.remove();
}
// Result: Memory leak in thread pool
```

**❌ Pitfall 2: InheritableThreadLocal with thread pools**

```java
// WRONG
InheritableThreadLocal<String> ctx = new InheritableThreadLocal<>();
ctx.set("value");

executor.submit(() -> {
    // May see stale value from previous task!
});
```

**❌ Pitfall 3: Async without propagation**

```java
// WRONG
threadLocal.set("value");

CompletableFuture.runAsync(() -> {
    threadLocal.get();  // null!
});
```

---


# 9. Java Deadlock, Livelock, and Starvation


## Summary

### Quick Reference

**Deadlock Four Conditions:**

```
1. Mutual Exclusion - Resource held exclusively
2. Hold and Wait - Hold resource while waiting
3. No Preemption - Can't forcibly take resource
4. Circular Wait - Circular dependency chain

Break ANY ONE → No deadlock
```

**Detection:**

```bash
# Thread dump
jstack <pid>

# Or
kill -3 <pid>  # Unix
Ctrl+Break     # Windows

# Look for:
# "Found 1 deadlock"
# "waiting to lock"
# "which is held by"
```

**Prevention Strategies:**

```java
// 1. Lock ordering
synchronized (getLock(id1 < id2 ? id1 : id2)) {
    synchronized (getLock(id1 < id2 ? id2 : id1)) {
        // work
    }
}

// 2. tryLock with timeout
if (lock1.tryLock(1, TimeUnit.SECONDS)) {
    try {
        if (lock2.tryLock(1, TimeUnit.SECONDS)) {
            try {
                // work
            } finally { lock2.unlock(); }
        }
    } finally { lock1.unlock(); }
}

// 3. Single lock
synchronized (GLOBAL_LOCK) {
    // work
}
```

**Livelock Solution:**

```java
// Add random backoff
long backoff = 10 + random.nextInt(100);
Thread.sleep(backoff);
```

**Starvation Solutions:**

```java
// Fair locks
ReentrantLock lock = new ReentrantLock(true);

// Or limit priorities
// Or monitor thread progress
```

### Best Practices

1. ✅ **Always acquire locks in same order**
2. ✅ **Use tryLock() for dynamic lock order**
3. ✅ **Keep lock scope minimal**
4. ✅ **Don't call external code while holding locks**
5. ✅ **Monitor for deadlocks in production**
6. ✅ **Use fair locks when starvation possible**
7. ❌ **Don't hold multiple locks if avoidable**
8. ❌ **Don't nest synchronized blocks without ordering**
9. ❌ **Don't ignore thread priorities in critical sections**
10. ❌ **Don't hold locks during I/O or network calls**

---

# 10. Java Memory Model and Concurrent Programming Patterns

--

## Summary

### Quick Reference

**Java Memory Model:**

```
Happens-Before Rules:
1. Program order within thread
2. Monitor lock (synchronized)
3. Volatile write → read
4. Thread start → thread actions
5. Thread actions → thread join
6. Transitivity

Guarantees:
- volatile: visibility + ordering
- synchronized: visibility + atomicity + ordering
- final: safe publication (after constructor)
```

**Safe Publication:**

```java
// 1. Static initializer
private static final Object INSTANCE = new Object();

// 2. volatile
private volatile Object instance;

// 3. final field
private final Object instance;

// 4. Synchronized
private Object instance;
public synchronized Object getInstance() { return instance; }

// 5. Concurrent collection
map.put(key, value);  // Safe publication
```

**Singleton (Best):**

```java
// Holder pattern
class Singleton {
    private Singleton() {}
    
    private static class Holder {
        static final Singleton INSTANCE = new Singleton();
    }
    
    public static Singleton getInstance() {
        return Holder.INSTANCE;
    }
}

// Or enum
enum Singleton {
    INSTANCE;
}
```

**Producer-Consumer:**

```java
BlockingQueue<T> queue = new ArrayBlockingQueue<>(capacity);

// Producer
queue.put(item);

// Consumer
T item = queue.take();
```

**Immutability:**

```java
final class Immutable {
    private final int value;
    
    public Immutable(int value) {
        this.value = value;
    }
    
    public int getValue() { return value; }
    
    // Return new instance
    public Immutable withValue(int newValue) {
        return new Immutable(newValue);
    }
}
```

### Best Practices

1. ✅ **Minimize shared mutable state**
2. ✅ **Use volatile for flags and status**
3. ✅ **Use AtomicInteger for counters**
4. ✅ **Use synchronized for compound operations**
5. ✅ **Prefer immutable objects**
6. ✅ **Use thread-safe collections**
7. ✅ **Document synchronization policy**
8. ✅ **Keep lock scope minimal**
9. ❌ **Don't use volatile for compound operations**
10. ❌ **Don't hold locks during I/O**

---

# 11. Java Fork/Join Framework

## Summary

### Quick Reference

**RecursiveTask vs RecursiveAction:**

```java
// Returns result
class SumTask extends RecursiveTask<Long> {
    protected Long compute() {
        if (small) return computeDirectly();
        
        SumTask left = new SumTask(...);
        SumTask right = new SumTask(...);
        
        left.fork();
        long rightResult = right.compute();
        long leftResult = left.join();
        
        return leftResult + rightResult;
    }
}

// No result (void)
class IncrementAction extends RecursiveAction {
    protected void compute() {
        if (small) {
            incrementDirectly();
        } else {
            invokeAll(left, right);
        }
    }
}
```

**Threshold Selection:**

```
Too small (< 100): Too many tasks, overhead dominates
Optimal (1000-10000): Good balance
Too large (> 100000): Not enough parallelism
```

**Fork/Join vs ExecutorService:**

```
Fork/Join:
✓ Recursive decomposition
✓ CPU-intensive
✓ Dynamic task creation
✓ Work-stealing

ExecutorService:
✓ Independent tasks
✓ I/O-bound OK
✓ Fixed task count
✓ Blocking OK
```

**Parallel Streams:**

```java
// Uses ForkJoinPool.commonPool()
list.parallelStream()
    .filter(...)
    .map(...)
    .collect(Collectors.toList());

// Good: ArrayList, arrays, ranges
// Bad: LinkedList, Stream.iterate()
```

### Best Practices

1. ✅ **Threshold 1000-10000** for simple operations
2. ✅ **Compute one branch** in current thread (fork one, compute other)
3. ✅ **CPU-intensive only** (no blocking)
4. ✅ **Balanced subtasks**
5. ✅ **Immutable data** or careful synchronization
6. ✅ **Benchmark** sequential vs parallel
7. ❌ **Don't use for I/O** operations
8. ❌ **Don't share mutable state**
9. ❌ **Don't fork then immediately join both**
10. ❌ **Don't assume faster** (measure!)

---

# 12. Advanced Concurrency Patterns


## Summary

### Quick Reference

**Double-Checked Locking:**

```java
private volatile Singleton instance;

public Singleton getInstance() {
    Singleton result = instance;
    if (result == null) {
        synchronized (this) {
            result = instance;
            if (result == null) {
                instance = result = new Singleton();
            }
        }
    }
    return result;
}

// BUT: Prefer holder idiom instead!
```

**Lock Striping:**

```java
// Divide into N independent locks
Object[] locks = new Object[16];
long[] data = new long[16];

void increment() {
    int stripe = hash(Thread.currentThread()) % 16;
    synchronized (locks[stripe]) {
        data[stripe]++;
    }
}

// Up to 16 threads can work in parallel!
```

**RCU Pattern:**

```java
private volatile Map<K, V> map;

V get(K key) {
    return map.get(key);  // Lock-free read
}

synchronized void put(K key, V value) {
    Map<K, V> newMap = new HashMap<>(map);  // Copy
    newMap.put(key, value);                  // Update
    map = newMap;                            // Replace
}
```

**Disruptor:**

```
Ring Buffer + Sequences + Wait Strategies
= Ultra-low latency (10-100x faster than queues)
```

**Actor Model:**

```
No shared state + Message passing + Supervision
= Fault-tolerant distributed systems
```

**Reactive:**

```
Observable → Operators → Observer
= Asynchronous data streams with backpressure
```

### Pattern Selection Guide

```
┌─────────────────────┬──────────────┬────────────────┬──────────────┐
│ Pattern             │ Best For     │ Complexity     │ Performance  │
├─────────────────────┼──────────────┼────────────────┼──────────────┤
│ DCL                 │ Lazy init    │ Medium         │ Good         │
│ Spin Lock           │ Short locks  │ Low            │ Excellent    │
│ Lock Striping       │ High write   │ Medium         │ Excellent    │
│ RCU                 │ Read-heavy   │ Low            │ Excellent    │
│ Disruptor           │ Ultra-low    │ High           │ Exceptional  │
│                     │ latency      │                │              │
│ Actor Model         │ Distributed  │ High           │ Good         │
│ Reactive            │ Event-driven │ High           │ Good         │
└─────────────────────┴──────────────┴────────────────┴──────────────┘
```

### Best Practices

1. ✅ **Use holder idiom** over DCL
2. ✅ **Spin locks only for** very short critical sections
3. ✅ **Lock striping** reduces contention
4. ✅ **RCU for read-heavy** workloads
5. ✅ **Disruptor for latency-critical** systems
6. ✅ **Actors for distributed** systems
7. ✅ **Reactive for event-driven** architectures
8. ❌ **Don't use DCL** without volatile
9. ❌ **Don't spin** with high contention
10. ❌ **Don't copy large** structures in RCU

---
