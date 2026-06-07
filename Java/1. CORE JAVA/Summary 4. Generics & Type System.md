
# 1. Generics Fundamentals and Type Erasure


---

## Summary

### Quick Reference

**Generic Syntax:**

```java
// Generic class
class Box<T> {
    private T value;
    public void set(T value) { this.value = value; }
    public T get() { return value; }
}

// Multiple type parameters
class Pair<K, V> {
    private K key;
    private V value;
}

// Bounded type parameter
class NumberBox<T extends Number> {
    private T number;
}

// Generic method
public static <T> T getFirst(List<T> list) {
    return list.get(0);
}
```

**Type Erasure:**

```java
// Before erasure
class Box<T> {
    private T value;
    public T get() { return value; }
}

// After erasure
class Box {
    private Object value;  // T → Object
    public Object get() { return value; }
}

// Usage with casts
Box<String> box = new Box<>();
String s = box.get();  // Compiler inserts: (String)box.get()
```

**Limitations:**

```
✗ new T()              → Pass Class<T> or factory
✗ new T[10]            → Use List<T> or Array.newInstance()
✗ instanceof T         → Pass Class<T>
✗ T.class              → Pass Class<T> as parameter
✗ static T field       → Not possible
✗ catch (T e)          → Not possible
✗ List<String>[]       → Use List<List<String>>
```

### Key Takeaways

**1. Type erasure is fundamental:**

```
Compile time: Full type information, type checking
Runtime: Type parameters erased, only raw types remain
```

**2. Bridge methods maintain compatibility:**

```java
class Node<T> {
    public T getData() { ... }
}

class IntNode extends Node<Integer> {
    public Integer getData() { ... }     // Your method
    public Object getData() { ... }      // Bridge (synthetic)
}
```

**3. Arrays vs Generics:**

```
Arrays: Reified (runtime type checking)
Generics: Erased (compile-time only)
→ Cannot create generic arrays
```

**4. Raw types break safety:**

```java
List rawList = new ArrayList();  // NO TYPE CHECKING
rawList.add("hello");
rawList.add(42);  // Compiles! Runtime error later
```

**5. Workarounds exist:**

```java
// Pass type information
public <T> T create(Class<T> type) throws Exception {
    return type.getDeclaredConstructor().newInstance();
}

// Type tokens
new TypeToken<List<String>>() {}
```

---

# 2. Bounded Type Parameters and Wildcards

---

## Summary

### Quick Reference

**Bounded Type Parameters vs Wildcards:**

```java
// Type parameter - can name and refer to type
<T extends Number> T max(List<T> list)
// ↑ T appears multiple times, can return T

// Wildcard - anonymous type
double sum(List<? extends Number> numbers)
// ↑ Type used once, only reading
```

**PECS Rule:**

```java
// Producer Extends - reading from it
<? extends T>  // Get values OUT (produce)

// Consumer Super - writing to it
<? super T>    // Put values IN (consume)

// Example: Collections.copy
public static <T> void copy(
    List<? super T> dest,      // Consumer - write to
    List<? extends T> src)     // Producer - read from
```

**Upper Bounds:**

```
<T extends Type>         // Type parameter
<? extends Type>         // Wildcard

Reading: ✅ Safe - get Type or subtype
Writing: ❌ Unsafe - don't know exact type
```

**Lower Bounds:**

```
<? super Type>           // Wildcard only!

Reading: ❌ Limited - only Object
Writing: ✅ Safe - can add Type
```

**Unbounded Wildcard:**

```
<?>                      // Unknown type

Reading: ✅ As Object
Writing: ❌ Only null
Use when: Don't care about type
```

**Multiple Bounds:**

```
<T extends Class & Interface1 & Interface2>

Rules:
- Class first (if present)
- At most one class
- Multiple interfaces OK
```

### Decision Tree

```
Need to work with collection?
  ↓
Only READING from it?
  YES → <? extends T>
  Example: sum(List<? extends Number>)
  ↓
Only WRITING to it?
  YES → <? super T>
  Example: addAll(List<? super Integer> dest)
  ↓
Both READ and WRITE?
  YES → <T> (no wildcard)
  Example: sort(List<T> list)
  ↓
Only metadata (size, isEmpty)?
  YES → <?>
  Example: printSize(List<?>)
```

### Best Practices

**1. Apply PECS:**

```java
// ✅ GOOD: PECS applied
public static <T> void copy(
    List<? super T> dest,
    List<? extends T> src)

// ❌ BAD: PECS reversed
public static <T> void copy(
    List<? extends T> dest,    // Can't write!
    List<? super T> src)       // Can't read specific type!
```

**2. Don't use wildcards in return types:**

```java
// ❌ BAD: Wildcard in return
public List<? extends Number> getNumbers()

// ✅ GOOD: Concrete type
public List<Number> getNumbers()
```

**3. Prefer wildcards for flexibility:**

```java
// ✅ GOOD: Accepts any Number list
public double sum(List<? extends Number> numbers)

// ❌ BAD: Only accepts List<Number>
public double sum(List<Number> numbers)
```

**4. Use type parameters when naming needed:**

```java
// ✅ GOOD: T named for return type
public <T extends Comparable<T>> T max(List<T> list)

// ❌ BAD: Can't return specific type
public Comparable<?> max(List<? extends Comparable<?>> list)
```

**5. Multiple bounds: class first:**

```java
// ✅ GOOD: Class first
<T extends Animal & Comparable<T>>

// ❌ BAD: Interface first
<T extends Comparable<T> & Animal>  // Compile error!
```

---

# 3. Generic Type Inference and Diamond Operator


---

## Summary

### Quick Reference

**Type Inference Evolution:**

```
Java 5-6:  Basic method call inference
Java 7:    Diamond operator <>
Java 8:    Target typing, lambda inference
Java 9:    Diamond with anonymous classes
Java 10:   var keyword
Java 11+:  Incremental improvements
```

**Diamond Operator:**

```java
// Before Java 7
List<String> list = new ArrayList<String>();

// Java 7+
List<String> list = new ArrayList<>();  ✅

// Nested generics
Map<String, List<Integer>> map = new HashMap<>();  ✅
```

**Target Typing (Java 8+):**

```java
// Method arguments
processMap(new HashMap<>());  // Infers from parameter type

// Return statements
return new ArrayList<>();  // Infers from return type

// Lambda parameters
Comparator<String> c = (s1, s2) -> s1.length() - s2.length();
// s1 and s2 inferred as String
```

**Type Witness:**

```java
// Syntax
ClassName.<TypeArgs>methodName(args)

// Example
List<String> list = Collections.<String>emptyList();

// Rarely needed - prefer target typing
List<String> list = Collections.emptyList();  ✅
```

**var (Java 10+):**

```java
// Type inferred from right side
var list = new ArrayList<String>();  // ArrayList<String>
var map = new HashMap<String, Integer>();  // HashMap<String, Integer>

// Still statically typed!
// list = "hello";  // ERROR
```

### When Inference Fails

```
1. No target type → Assign to variable
2. Ambiguous types → Use type witness
3. Overload ambiguity → Provide explicit type
4. Null literal → Cast or type witness
5. Complex hierarchies → Simplify or type witness
6. Array creation → Use List or Class token
```

### Best Practices

**1. Always use diamond operator:**

```java
// ✅ GOOD
List<String> list = new ArrayList<>();

// ❌ BAD
List<String> list = new ArrayList<String>();
```

**2. Let target typing work:**

```java
// ✅ GOOD
List<String> list = Collections.emptyList();

// ❌ BAD (unnecessary type witness)
List<String> list = Collections.<String>emptyList();
```

**3. Use var judiciously:**

```java
// ✅ GOOD: Type obvious
var list = new ArrayList<String>();
var count = 0;

// ❌ BAD: Type not obvious
var result = process();  // What type is this?
```

**4. Avoid explicit types when inference works:**

```java
// ✅ GOOD
Map<String, Integer> map = createMap("age", 30);

// ❌ BAD (redundant type witness)
Map<String, Integer> map = TypeWitness.<String, Integer>createMap("age", 30);
```

**5. Break complex expressions:**

```java
// ❌ BAD: Complex, inference may fail
process(transform(filter(source)));

// ✅ GOOD: Clear types
var filtered = filter(source);
var transformed = transform(filtered);
process(transformed);
```

---

# 4. Reified Generics Workarounds

---

## Summary

### Quick Reference

**Type Capture Patterns:**

```java
// 1. Class token
public <T> T create(Class<T> type) { }
create(String.class)

// 2. TypeReference (super type token)
TypeReference<List<String>> ref = new TypeReference<List<String>>() {};
                                                                     ^^
// Anonymous class required!

// 3. Guava TypeToken
TypeToken<List<String>> token = new TypeToken<List<String>>() {};

// 4. Jackson TypeReference
List<User> users = mapper.readValue(json, 
    new TypeReference<List<User>>() {});
```

**Generic Array Creation:**

```java
// 1. Array.newInstance
@SuppressWarnings("unchecked")
public <T> T[] create(Class<T> type, int size) {
    return (T[]) Array.newInstance(type, size);
}

// 2. Varargs
@SafeVarargs
public <T> T[] arrayOf(T... elements) {
    return elements;
}

// 3. Use List (recommended)
List<T> list = new ArrayList<>();
```

**Reflection Type Hierarchy:**

```
Type (interface)
  ├── Class<T>              // String.class
  ├── ParameterizedType     // List<String>
  ├── GenericArrayType      // T[]
  ├── TypeVariable<D>       // T, E, K, V
  └── WildcardType          // ?, ? extends Number
```

### Comparison Table

```
┌──────────────────┬─────────────┬─────────────┬──────────────┐
│ Approach         │ Captures    │ Use Case    │ Complexity   │
├──────────────────┼─────────────┼─────────────┼──────────────┤
│ Class<T>         │ Raw type    │ Simple      │ Low ✅       │
│ TypeReference    │ Full type   │ JSON        │ Medium       │
│ Guava TypeToken  │ Full type   │ Advanced    │ High         │
│ Reflection       │ Full type   │ Frameworks  │ Very High    │
└──────────────────┴─────────────┴─────────────┴──────────────┘
```

### Best Practices

**1. Choose the right tool:**

```java
// Non-generic types → Class token
create(String.class)

// Generic types → TypeReference or TypeToken
new TypeReference<List<String>>() {}

// JSON deserialization → Jackson TypeReference
mapper.readValue(json, new TypeReference<List<User>>() {})
```

**2. Avoid generic arrays:**

```java
// ❌ BAD: Generic array
public <T> T[] create() {
    return new T[10];  // ERROR
}

// ✅ GOOD: Use List
public <T> List<T> create() {
    return new ArrayList<>();
}
```

**3. Remember anonymous class:**

```java
// ❌ BAD: Forgets anonymous class
// TypeReference<List<String>> ref = new TypeReference<>();

// ✅ GOOD: Anonymous class captures type
TypeReference<List<String>> ref = new TypeReference<List<String>>() {};
//                                                                   ^^
```

**4. Cache TypeReferences:**

```java
// ✅ GOOD: Reusable constant
public static final TypeReference<List<User>> USER_LIST_TYPE = 
    new TypeReference<List<User>>() {};

// Use repeatedly
List<User> users1 = mapper.readValue(json1, USER_LIST_TYPE);
List<User> users2 = mapper.readValue(json2, USER_LIST_TYPE);
```

---

# 5. Covariance and Contravariance

---

## Summary

### Quick Reference

**Variance Types:**

```
Covariance (extends):
  Preserves subtyping for reading
  List<Dog> → List<? extends Animal> ✓
  Safe to read, unsafe to write

Contravariance (super):
  Reverses subtyping for writing
  List<Animal> → List<? super Dog> ✓
  Safe to write, can only read as Object

Invariance (no wildcard):
  No subtyping relationship
  List<Dog> ↛ List<Animal> ✗
  Exact type required
```

**Arrays vs Generics:**

```
Arrays:
✓ Covariant (Dog[] → Animal[])
✗ Runtime checking (ArrayStoreException)
✗ Performance cost
✗ Can fail at runtime

Generics:
✓ Invariant by default
✓ Compile-time safety
✓ No runtime overhead
✓ Use wildcards for flexibility
```

**PECS Principle:**

```
Producer Extends (Covariance):
  <? extends T>
  Read from collection
  List<Dog> → List<? extends Animal>

Consumer Super (Contravariance):
  <? super T>
  Write to collection
  List<Animal> → List<? super Dog>

Example:
  <T> void copy(
      List<? super T> dest,    // Consumer
      List<? extends T> src)   // Producer
```

**Return Type Covariance:**

```
Override with more specific return:

class Animal {
    Animal reproduce() { ... }
}

class Dog extends Animal {
    @Override
    Dog reproduce() { ... }  // ✓ Covariant return
}

Safe because Dog is Animal
```

### Variance Decision Tree

```
Need to work with parameterized type?
  ↓
Only READING values?
  YES → <? extends T> (Covariance)
  Example: double sum(List<? extends Number>)
  ↓
Only WRITING values?
  YES → <? super T> (Contravariance)
  Example: void addAll(List<? super Dog>)
  ↓
Both READING and WRITING?
  YES → <T> (Invariance)
  Example: <T> void sort(List<T>)
  ↓
Only metadata access?
  YES → <?> (Unbounded)
  Example: int size(List<?>)
```

### Key Patterns

**1. Collections.copy:**

```java
public static <T> void copy(
    List<? super T> dest,      // Write here
    List<? extends T> src)     // Read from here
```

**2. Comparator:**

```java
void sort(Comparator<? super E> c)
// General comparator for specific type
```

**3. Function:**

```java
<R> Stream<R> map(
    Function<? super T, ? extends R> mapper)
// Contravariant input, covariant output
```

**4. Repository:**

```java
void saveAll(Collection<? extends T> entities)
List<? extends T> findAll()
// Covariant for reading collections
```

### Best Practices

**1. Arrays - avoid covariance:**

```java
// ❌ BAD: Covariance risk
Object[] objects = new String[10];
objects[0] = 42;  // ArrayStoreException

// ✅ GOOD: Use generics
List<Object> objects = new ArrayList<>();
List<String> strings = new ArrayList<>();
// objects = strings;  // Compile error
```

**2. Use wildcards for flexibility:**

```java
// ❌ BAD: Too restrictive
public void process(List<Animal> animals)

// ✅ GOOD: Accepts any Animal subtype
public void process(List<? extends Animal> animals)
```

**3. Apply PECS consistently:**

```java
// ✅ GOOD: PECS applied
public <T> void copy(
    List<? super T> dest,
    List<? extends T> src)
```

**4. Return type covariance for builders:**

```java
class Builder {
    Builder setName(String name) {
        return this;
    }
}

class SpecificBuilder extends Builder {
    @Override
    SpecificBuilder setName(String name) {  // Covariant
        return (SpecificBuilder) super.setName(name);
    }
    
    SpecificBuilder setSpecific() {
        return this;
    }
}
```

---
# 6. Advanced Generic Patterns

---

## Summary

### Pattern Catalog

**1. Recursive Type Bounds:**

```java
// Enum pattern
public abstract class Enum<E extends Enum<E>>

// Usage
enum Color extends Enum<Color> { RED, GREEN, BLUE }

// Method signature
public static <T extends Comparable<T>> T max(T a, T b)

// Relaxed for inheritance
public static <T extends Comparable<? super T>> T max(T a, T b)
```

**2. Self-Referential Generics:**

```java
// CRTP (Curiously Recurring Template Pattern)
class Builder<T extends Builder<T>> {
    @SuppressWarnings("unchecked")
    protected T self() {
        return (T) this;
    }
    
    public T setName(String name) {
        this.name = name;
        return self();
    }
}

class SpecificBuilder extends Builder<SpecificBuilder> {
    public SpecificBuilder setValue(int value) {
        return self();  // Returns SpecificBuilder
    }
}
```

**3. Generic Builder Pattern:**

```java
// Type-safe builder with phantom types
class Builder<N, E> {
    public Builder<HasName, E> setName(String name) { }
    public Builder<N, HasEmail> setEmail(String email) { }
    public User build() { }  // Only on Builder<HasName, HasEmail>
}

// Step builder
interface CustomerStep {
    ProductStep customer(String customer);
}
interface ProductStep {
    BuildStep product(String product);
}
```

**4. Type-Safe Heterogeneous Containers:**

```java
// Favorites pattern (Effective Java)
class Favorites {
    private Map<Class<?>, Object> favorites = new HashMap<>();
    
    public <T> void putFavorite(Class<T> type, T instance) {
        favorites.put(type, type.cast(instance));
    }
    
    public <T> T getFavorite(Class<T> type) {
        return type.cast(favorites.get(type));
    }
}

// Different types in one container
favorites.putFavorite(String.class, "Java");
favorites.putFavorite(Integer.class, 42);
```

**5. Generic Singleton Pattern:**

```java
// Per-type singleton
class Cache<T> {
    private static Map<Class<?>, Cache<?>> instances = ...;
    
    public static <T> Cache<T> getInstance(Class<T> type) {
        return (Cache<T>) instances.computeIfAbsent(
            type, k -> new Cache<>());
    }
}

// Different singleton per type
Cache<String> stringCache = Cache.getInstance(String.class);
Cache<Integer> intCache = Cache.getInstance(Integer.class);
```

**6. Generic Factory Pattern:**

```java
// Abstract factory
interface Factory<T extends Animal> {
    T createAnimal();
}

class DogFactory implements Factory<Dog> {
    public Dog createAnimal() { return new Dog(); }
}

// Registry factory
class RegistryFactory<T> {
    private Map<String, Supplier<T>> registry = ...;
    
    public void register(String key, Supplier<T> factory) { }
    public T create(String key) { }
}
```

### When to Use Each Pattern

```
Recursive Type Bounds:
✓ Comparable/Enum-like interfaces
✓ Self-comparison operations
✓ Type-safe operations on same type

Self-Referential Generics:
✓ Fluent APIs
✓ Builder patterns with inheritance
✓ Method chaining across hierarchy

Generic Builder:
✓ Complex object construction
✓ Compile-time validation of required fields
✓ Progressive type narrowing

Type-Safe Heterogeneous Containers:
✓ Storing different types in one map
✓ Service registries
✓ Attribute maps with type safety

Generic Singleton:
✓ Different singleton per type
✓ Type-specific caches
✓ Per-type service instances

Generic Factory:
✓ Type-safe object creation
✓ Abstract factories
✓ Plugin systems
```

### Best Practices

**1. Use relaxed recursive bounds for inheritance:**

```java
// ❌ TOO STRICT
<T extends Comparable<T>>

// ✅ ALLOWS INHERITANCE
<T extends Comparable<? super T>>
```

**2. Provide self() helper in CRTP:**

```java
// ✅ GOOD
@SuppressWarnings("unchecked")
protected T self() {
    return (T) this;
}
```

**3. Runtime type check in heterogeneous containers:**

```java
// ✅ GOOD: Prevents raw type abuse
public <T> void put(Class<T> type, T instance) {
    favorites.put(type, type.cast(instance));
}
```

**4. Use enum for simple singletons:**

```java
// ✅ BEST SINGLETON
enum GenericService {
    INSTANCE;
    // Add type-safe map here
}
```

---
