# 1. Exception Hierarchy and Best Practices
---

## Summary

### Exception Hierarchy Quick Reference

```
Throwable
├── Error (unchecked) - DON'T catch
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   ├── NoClassDefFoundError
│   └── AssertionError
│
└── Exception
    ├── Checked (must handle) - recoverable
    │   ├── IOException
    │   ├── SQLException
    │   ├── ClassNotFoundException
    │   └── InterruptedException
    │
    └── RuntimeException (unchecked) - programming errors
        ├── NullPointerException
        ├── IllegalArgumentException
        ├── IllegalStateException
        ├── IndexOutOfBoundsException
        └── ClassCastException
```

### Decision Trees

**Checked vs Unchecked:**

```
Is it recoverable?
  YES → Can caller do something useful?
    YES → CHECKED
    NO → UNCHECKED
  NO → UNCHECKED

Is it expected?
  YES → CHECKED
  NO → UNCHECKED (programming error)
```

**Exception Design:**

```
Creating custom exception?
  ├─ Checked or unchecked?
  ├─ Add context fields?
  ├─ Create hierarchy?
  └─ Provide 4 constructors
```

**Exception Translation:**

```
Database → Repository: SQLException → DataAccessException
Repository → Service: DataAccessException → BusinessException
Service → Controller: BusinessException → HttpException
```

### Best Practices Checklist

**✅ DO:**

- Use specific exception types
- Chain exceptions (preserve cause)
- Add business context
- Translate at layer boundaries
- Check suppressed exceptions
- Use try-with-resources
- Create domain hierarchies
- Document what can be thrown

**❌ DON'T:**

- Catch Error (generally)
- Catch Throwable
- Swallow exceptions silently
- Lose original exception
- Use exceptions for control flow
- Create too many custom exceptions
- Mix layer concerns
- Expose implementation details

---

# 2. Try-With-Resources and AutoCloseable

---

## Summary

### Quick Reference

**Basic Try-With-Resources:**

```java
// Single resource
try (Resource r = new Resource()) {
    r.use();
}

// Multiple resources
try (Resource1 r1 = new Resource1();
     Resource2 r2 = new Resource2()) {
    r1.use();
    r2.use();
}
// Closed in reverse order: r2, r1
```

**AutoCloseable vs Closeable:**

```java
// AutoCloseable (generic)
public interface AutoCloseable {
    void close() throws Exception;  // Any exception
}

// Closeable (I/O specific)
public interface Closeable extends AutoCloseable {
    void close() throws IOException;  // Only IOException
}

Use Closeable for I/O
Use AutoCloseable for other resources
```

**Suppressed Exceptions:**

```java
try (Resource r = new Resource()) {
    throw new Exception("Primary");
    // r.close() throws too
} catch (Exception e) {
    // Primary exception
    Throwable[] suppressed = e.getSuppressed();
    // Close exception in suppressed[0]
}
```

**Custom Implementation:**

```java
class MyResource implements AutoCloseable {
    private boolean closed = false;
    
    @Override
    public void close() {
        if (closed) return;  // Idempotent
        
        // Cleanup
        closed = true;
    }
}
```

### Comparison Tables

**Try-With-Resources vs Try-Finally:**

```
┌────────────────┬─────────────────┬──────────────────┐
│ Aspect         │ TWR (Java 7+)   │ Try-Finally      │
├────────────────┼─────────────────┼──────────────────┤
│ Lines of code  │ 1 line          │ 9+ lines         │
│ Suppression    │ Automatic       │ Manual/Complex   │
│ Idempotence    │ Guaranteed      │ Manual           │
│ Error-prone    │ No              │ Yes              │
│ Multiple       │ Easy            │ Duplicative      │
└────────────────┴─────────────────┴──────────────────┘
```

**AutoCloseable vs Closeable:**

```
┌──────────────┬─────────────────┬──────────────────┐
│ Aspect       │ AutoCloseable   │ Closeable        │
├──────────────┼─────────────────┼──────────────────┤
│ Exception    │ Exception       │ IOException      │
│ Scope        │ Generic         │ I/O specific     │
│ Idempotence  │ Recommended     │ Required         │
│ Use case     │ Any resource    │ I/O resources    │
└──────────────┴─────────────────┴──────────────────┘
```

### Best Practices Checklist

**✅ DO:**

- Use try-with-resources for all AutoCloseable resources
- Implement AutoCloseable for custom resources
- Make close() idempotent
- Check suppressed exceptions when debugging
- Close resources in reverse order (automatic with TWR)
- Track closed state
- Log close exceptions

**❌ DON'T:**

- Use try-finally unless absolutely necessary
- Forget null checks in old code
- Ignore suppressed exceptions
- Throw exceptions from close() unless critical
- Assume close order
- Create resources that aren't AutoCloseable

---

# 3. Exception Handling Anti-Patterns


---

## Summary

### Anti-Patterns Quick Reference

**❌ DON'T:**

```java
// 1. Catch Exception/Throwable
catch (Exception e) { }  // Too broad

// 2. Empty catch blocks
catch (IOException e) { }  // Silent failure

// 3. Exceptions for flow control
while (true) {
    try { array[i++]; }
    catch (ArrayIndexOutOfBoundsException e) { break; }
}

// 4. Lose stack traces
throw new RuntimeException("Failed");  // No cause

// 5. No context
throw new RuntimeException(e);  // What operation?

// 6. Swallow exceptions
catch (Exception e) { return null; }  // Silent error

// 7. Log and rethrow
e.printStackTrace();
throw new RuntimeException(e);  // Duplicate logs
```

**✅ DO:**

```java
// 1. Catch specific
catch (FileNotFoundException e) { }
catch (IOException e) { }

// 2. Always log or handle
catch (IOException e) {
    logger.error("File error", e);
    throw new RuntimeException("Failed", e);
}

// 3. Normal control flow
for (int i = 0; i < array.length; i++) { }

// 4. Chain exceptions
throw new RuntimeException("Failed", originalException);

// 5. Add context
throw new RuntimeException("Failed to process user: " + userId, e);

// 6. Propagate or handle fully
throw e;  // Or handle completely

// 7. Log once at top level
// Service: throw new RuntimeException("msg", e);
// Controller: logger.error("Request failed", e);
```

### Decision Trees

**Should I catch this exception?**

```
Can I handle it completely?
  YES → Handle it, don't rethrow
  NO → Continue...

Can I add useful context?
  YES → Add context, rethrow
  NO → Continue...

Is this top level?
  YES → Log and handle
  NO → Let it propagate
```

**What should I catch?**

```
Know specific exception type?
  YES → Catch specific
  NO → Continue...

Multiple types, same handling?
  YES → Multi-catch
  NO → Continue...

Top level or framework code?
  YES → Catch Exception
  NO → DON'T catch Exception
```

---

# 4. Error Handling in Async and Functional Code


---

## Summary

### Quick Reference

**CompletableFuture Exception Handling:**

```java
// Recovery
future.exceptionally(ex -> fallback)

// Transform both cases
future.handle((result, ex) -> {
    if (ex != null) return handleError(ex);
    return handleSuccess(result);
})

// Side effects only
future.whenComplete((result, ex) -> log(result, ex))

// Timeout
future.orTimeout(1, TimeUnit.SECONDS)
```

**Stream Exception Handling:**

```java
// Wrapper function
public static <T, R> Function<T, R> unchecked(
        ThrowingFunction<T, R, Exception> f) {
    return t -> {
        try { return f.apply(t); }
        catch (Exception e) { throw new RuntimeException(e); }
    };
}

// Usage
.map(unchecked(file -> new FileReader(file)))

// Optional pattern
.map(item -> {
    try { return Optional.of(parse(item)); }
    catch (Exception e) { return Optional.empty(); }
})
.filter(Optional::isPresent)
.map(Optional::get)
```

**Optional vs Exception:**

```java
// Use Optional for "might not exist"
Optional<User> findById(String id)

// Use Exception for "should exist"
User getById(String id) throws NotFoundException

// Combine
findById(id).orElseThrow(() -> new NotFoundException())
```

**Vavr Try/Either:**

```java
// Try monad
Try<String> result = Try.of(() -> readFile("data.txt"))
    .recover(ex -> "fallback")
    .map(String::toUpperCase);

// Either monad
Either<String, Integer> result = parseNumber("42")
    .mapLeft(error -> "Error: " + error)
    .map(num -> num * 2);
```

### Comparison Table

```
┌──────────────────┬───────────────────┬─────────────────┬──────────────────┐
│ Pattern          │ Use Case          │ Benefits        │ Drawbacks        │
├──────────────────┼───────────────────┼─────────────────┼──────────────────┤
│ exceptionally()  │ Async recovery    │ Clean syntax    │ Changes type     │
│ handle()         │ Both cases        │ Flexible        │ Must handle both │
│ whenComplete()   │ Side effects      │ No change       │ Can't recover    │
│ Try monad        │ Wrap exceptions   │ Functional      │ New dependency   │
│ Either           │ Typed errors      │ Type-safe       │ More complex     │
│ Optional         │ Nullable values   │ Standard Java   │ Limited errors   │
│ Unchecked wrap   │ Lambda exceptions │ Reusable        │ Lost checking    │
│ Sneaky throws    │ Bypass compiler   │ No wrapper      │ Dangerous        │
└──────────────────┴───────────────────┴─────────────────┴──────────────────┘
```

### Decision Trees

**Async Error Handling:**

```
CompletableFuture exception?
  ├─ Need recovery → exceptionally()
  ├─ Transform both → handle()
  └─ Log only → whenComplete()

Stream exception?
  ├─ Fail fast → Wrap in unchecked
  ├─ Continue processing → Optional/Result
  └─ Need error details → Result pattern

Checked in lambda?
  ├─ Simple case → Try-catch inside
  ├─ Reusable → Wrapper function
  ├─ Functional → Vavr Try
  └─ Clean → Extract method
```

---
