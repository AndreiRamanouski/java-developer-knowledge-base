
# 1. HashMap Internal Implementation


---

## Summary

**Internal Structure:**

```
HashMap = Array + LinkedList/Tree
- Array of buckets (power of 2)
- Each bucket: List (< 8) or Tree (≥ 8)
- Hash function: hash(key) ^ (hash >>> 16)
- Bucket index: hash & (capacity - 1)
```

**Time Complexity:**

```
Average: O(1)
Worst (Java 7): O(n)
Worst (Java 8+): O(log n)
```

**Critical Numbers:**

```
Capacity: 16 (default), always power of 2
Load factor: 0.75 (default)
Treeify threshold: 8
Resize: size > capacity * loadFactor
```

**Best Practices:**

1. ✅ Override equals and hashCode together
2. ✅ Use immutable keys
3. ✅ Size appropriately
4. ✅ Use ConcurrentHashMap for threading
5. ❌ Don't modify keys after insertion
6. ❌ Don't use in multithreaded code
7. ❌ Don't ignore sizing

---

# 2. TreeMap, LinkedHashMap, and Specialized Maps

## Summary

### Quick Reference

**TreeMap:**

```java
// Red-Black tree, O(log n), sorted keys
TreeMap<Integer, String> map = new TreeMap<>();
map.put(5, "five");
map.put(2, "two");
// Iteration: 2, 5 (sorted)

// NavigableMap operations
map.floorKey(4);    // 2 (largest ≤ 4)
map.ceilingKey(3);  // 5 (smallest ≥ 3)
map.subMap(2, 6);   // {2=two, 5=five}
```

**LinkedHashMap:**

```java
// Maintains insertion order
Map<String, Integer> map = new LinkedHashMap<>();

// Or access order (LRU)
Map<String, Integer> lru = new LinkedHashMap<>(16, 0.75f, true);
```

**LRU Cache:**

```java
class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private int maxSize;
    
    public LRUCache(int maxSize) {
        super(maxSize, 0.75f, true);
        this.maxSize = maxSize;
    }
    
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > maxSize;
    }
}
```

**WeakHashMap:**

```java
// Keys can be GC'd
Map<Object, String> map = new WeakHashMap<>();
Object key = new Object();
map.put(key, "value");
key = null;  // Entry will be GC'd
```

**IdentityHashMap:**

```java
// Uses == instead of equals()
Map<String, Integer> map = new IdentityHashMap<>();
String s1 = new String("key");
String s2 = new String("key");
map.put(s1, 1);
map.put(s2, 2);  // Two entries! (s1 != s2)
```

**EnumMap:**

```java
// Array-based, 4x faster for enums
enum Day { MON, TUE, WED }
Map<Day, String> map = new EnumMap<>(Day.class);
map.put(Day.MON, "Monday");
```

### Selection Guide

```
HashMap:          General purpose, fastest
LinkedHashMap:    Need insertion/access order
TreeMap:          Need sorted keys/range queries
WeakHashMap:      Memory-sensitive cache
IdentityHashMap:  Reference equality
EnumMap:          Enum keys (always use!)
```

### Performance Summary

```
Speed: EnumMap > Identity > Hash > Linked > Tree
Memory: EnumMap < Hash < Identity < Linked < Tree
```

---

# 3. ArrayList vs LinkedList - When to Use Each

---

## Summary

### Quick Reference

**ArrayList:**

```java
List<String> list = new ArrayList<>();
// Best for:
// - Random access: get(index) - O(1)
// - Iteration
// - Adding at end
// - Memory efficiency
// - 99% of use cases
```

**LinkedList:**

```java
List<String> list = new LinkedList<>();
// Best for:
// - Iterator-based insertion/deletion - O(1)
// - Deque operations (but use ArrayDeque instead)
// - Rare: 1% of use cases
```

**Complexity Comparison:**

```
Operation           ArrayList    LinkedList
─────────────────────────────────────────────
get(index)          O(1) ⚡      O(n) 🐌
add() at end        O(1) ⚡      O(1) 🟢
add(0, e)           O(n) 🐌      O(1) ⚡
iterator.remove()   O(n) 🐌      O(1) ⚡
Memory per element  8 bytes      40 bytes
```

**Decision Tree:**

```
Need iterator-based insertion/deletion?
├─ YES → LinkedList (rare)
└─ NO → ArrayList (default)
```

**Real-World Performance:**

```
Random access:     ArrayList 7500x faster
Iterator removal:  LinkedList 50x faster
Sequential access: ArrayList 1.5-2x faster
Memory overhead:   ArrayList 3x less
```

### Best Practices

**ArrayList:**

```java
// ✅ Size appropriately
List<String> list = new ArrayList<>(expectedSize);

// ✅ Use for random access
String item = list.get(index);

// ✅ Iterate with for-each
for (String item : list) {
    process(item);
}

// ✅ Add at end
list.add(item);
```

**LinkedList:**

```java
// ✅ Use iterator for modifications
Iterator<String> iter = list.iterator();
while (iter.hasNext()) {
    String item = iter.next();
    if (shouldRemove(item)) {
        iter.remove();  // O(1)
    }
}

// ❌ Don't use for random access
String item = list.get(index);  // O(n) - SLOW!

// ❌ Don't use get(i) in loop
for (int i = 0; i < list.size(); i++) {
    String item = list.get(i);  // O(n²) - VERY SLOW!
}
```

### Key Takeaways

1. **ArrayList is the default** - Use for 99% of cases
2. **LinkedList only for iterator operations** - Rare use case
3. **ArrayDeque beats LinkedList** for queue/deque
4. **Memory matters** - LinkedList uses 3x more
5. **Cache locality matters** - ArrayList much faster in practice
6. **Measure performance** - Profile before optimizing

---

# 4. HashSet, TreeSet, and LinkedHashSet Internals

---

## Summary

### Quick Reference

**HashSet:**

```java
Set<String> set = new HashSet<>();
// O(1) operations
// No ordering
// Backed by HashMap
// Default choice
```

**TreeSet:**

```java
Set<Integer> set = new TreeSet<>();
// O(log n) operations
// Sorted order
// Backed by TreeMap
// Use when sorting needed
```

**LinkedHashSet:**

```java
Set<String> set = new LinkedHashSet<>();
// O(1) operations
// Insertion order
// Backed by LinkedHashMap
// Use when order matters
```

### Comparison Table

```
┌──────────────────┬──────────┬─────────┬──────────┬────────────────┐
│ Implementation   │ Add      │ Contains│ Order    │ Best For       │
├──────────────────┼──────────┼─────────┼──────────┼────────────────┤
│ HashSet          │ O(1) ⚡  │ O(1) ⚡ │ None     │ General use    │
│ LinkedHashSet    │ O(1) 🟢  │ O(1) 🟢 │ Insertion│ Ordered iter   │
│ TreeSet          │ O(log n) │O(log n) │ Sorted   │ Sorted data    │
│ EnumSet          │ O(1) ⚡⚡│ O(1) ⚡⚡│ Enum     │ Enum flags     │
└──────────────────┴──────────┴─────────┴──────────┴────────────────┘

⚡⚡ = Fastest  ⚡ = Very Fast  🟢 = Fast
```

### Performance Summary

```
100K elements benchmark:
Add:      HashSet: 25ms  LinkedHashSet: 35ms  TreeSet: 85ms
Contains: HashSet: 5ms   LinkedHashSet: 8ms   TreeSet: 45ms
Memory:   HashSet: 24KB  LinkedHashSet: 32KB  TreeSet: 48KB

Winner: HashSet (3x faster, 2x less memory)
```

### Decision Tree

```
Need sorted elements?
├─ YES → TreeSet
└─ NO ↓

Need insertion order?
├─ YES → LinkedHashSet
└─ NO ↓

Elements are enums?
├─ YES → EnumSet
└─ NO ↓

→ HashSet (default)
```

### Best Practices

```java
// ✅ Default to HashSet
Set<String> set = new HashSet<>();

// ✅ Use immutable for constants
Set<String> TYPES = Set.of("A", "B", "C");

// ✅ EnumSet for enums
Set<Day> days = EnumSet.of(Day.MON, Day.FRI);

// ✅ Size appropriately
Set<String> set = new HashSet<>(expectedSize * 4/3);

// ✅ Always override equals/hashCode
class Element {
    @Override
    public boolean equals(Object obj) { ... }
    
    @Override
    public int hashCode() {
        return Objects.hash(field1, field2);
    }
}

// ❌ Don't use mutable elements
MutablePoint p = new MutablePoint(1, 2);
set.add(p);
p.x = 10;  // BAD! Lost in set!
```

### Key Takeaways

1. **HashSet is the default** - Use for 95% of cases
2. **TreeSet for sorting** - When you need sorted iteration
3. **LinkedHashSet for order** - When insertion order matters
4. **EnumSet for enums** - Always use for enum elements
5. **Always override equals/hashCode** - Critical for correctness
6. **Use immutable elements** - Prevents bugs

---

# 5. Queue and Deque Implementations

---

## Summary

### Quick Reference

**ArrayDeque:**

```java
Deque<String> queue = new ArrayDeque<>();
// O(1) operations
// Best for: Stack, Queue, Deque
// 3x faster than LinkedList
```

**PriorityQueue:**

```java
Queue<Task> pq = new PriorityQueue<>();
// O(log n) operations
// Min-heap by default
// Best for: Priority ordering
```

**BlockingQueue:**

```java
BlockingQueue<Task> queue = new ArrayBlockingQueue<>(100);
queue.put(task);  // Blocks if full
Task t = queue.take();  // Blocks if empty
// Best for: Producer-consumer
```

**DelayQueue:**

```java
DelayQueue<DelayedTask> queue = new DelayQueue<>();
// Elements implement Delayed
// Best for: Scheduling, cache expiration
```

**LinkedTransferQueue:**

```java
TransferQueue<Data> queue = new LinkedTransferQueue<>();
queue.transfer(data);  // Direct handoff
// Best for: Request-response
```

### Comparison Table

```
┌───────────────────┬─────────┬──────────┬──────────┬──────────────┐
│ Queue             │ Order   │ Thread   │ Ops      │ Use Case     │
├───────────────────┼─────────┼──────────┼──────────┼──────────────┤
│ ArrayDeque        │ FIFO    │ No       │ O(1)     │ Default      │
│ PriorityQueue     │ Min-heap│ No       │ O(log n) │ Priority     │
│ ArrayBlocking     │ FIFO    │ Yes      │ O(1)     │ Bounded      │
│ LinkedBlocking    │ FIFO    │ Yes      │ O(1)     │ Throughput   │
│ DelayQueue        │ Delay   │ Yes      │ O(log n) │ Scheduling   │
│ LinkedTransfer    │ FIFO    │ Yes      │ O(1)     │ Handoff      │
└───────────────────┴─────────┴──────────┴──────────┴──────────────┘
```

### Decision Tree

```
Single-threaded?
├─ YES → ArrayDeque (default)
└─ NO ↓

Need priority?
├─ YES → PriorityBlockingQueue
└─ NO ↓

Need delays?
├─ YES → DelayQueue
└─ NO ↓

Need bounded?
├─ YES → ArrayBlockingQueue
└─ NO → LinkedBlockingQueue
```

### Key Takeaways

1. **ArrayDeque is the default** - Use for 90% of queue needs
2. **Always bound BlockingQueues** - Prevent OOM in production
3. **LinkedTransferQueue for performance** - Lock-free, very fast
4. **PriorityQueue for heap algorithms** - Dijkstra, top-K
5. **DelayQueue for scheduling** - Built-in time-based execution
6. **Never use LinkedList** - ArrayDeque is 3x faster

---

# 6. Comparable vs Comparator

---

## Summary

### Quick Reference

**Comparable (Natural Ordering):**

```java
class Person implements Comparable<Person> {
    String name;
    int age;
    
    @Override
    public int compareTo(Person other) {
        return this.name.compareTo(other.name);
    }
}

// Automatic sorting
Collections.sort(people);  // Uses compareTo
TreeSet<Person> set = new TreeSet<>(people);
```

**Comparator (Custom Ordering):**

```java
// Lambda
people.sort((p1, p2) -> Integer.compare(p1.age, p2.age));

// Method reference
people.sort(Comparator.comparing(Person::getName));

// Chaining
people.sort(
    Comparator.comparing(Person::getDept)
              .thenComparingInt(Person::getSalary)
              .thenComparing(Person::getName)
);

// Reversed
people.sort(Comparator.comparing(Person::getAge).reversed());

// Nulls
people.sort(Comparator.comparing(
    Person::getName,
    Comparator.nullsLast(Comparator.naturalOrder())
));
```

### Comparison Table

```
┌──────────────────┬────────────┬────────────────┬─────────────┐
│ Feature          │ Comparable │ Comparator     │ Notes       │
├──────────────────┼────────────┼────────────────┼─────────────┤
│ Orderings        │ One        │ Multiple       │             │
│ Class control    │ Need       │ Don't need     │             │
│ Method           │ compareTo()│ compare()      │             │
│ Location         │ In class   │ Separate       │             │
│ Used by          │ TreeSet    │ sort(), TreeSet│             │
│ Flexibility      │ Low        │ High           │             │
│ Chaining         │ No         │ Yes            │             │
└──────────────────┴────────────┴────────────────┴─────────────┘
```

### Key Takeaways

**1. When to use Comparable:**

```
✓ One obvious natural ordering
✓ Control class source code
✓ Want automatic TreeSet/TreeMap sorting
Example: String, Integer, Date
```

**2. When to use Comparator:**

```
✓ Multiple orderings
✓ Don't control class
✓ Context-specific sorting
✓ Override natural order
Example: Sort Person by name OR age OR dept
```

**3. Implementation rules:**

```java
// ✅ CORRECT compareTo
return Integer.compare(this.value, other.value);
return Double.compare(this.value, other.value);
return this.name.compareTo(other.name);

// ❌ WRONG compareTo
return this.value - other.value;  // Overflow risk!
```

**4. Modern patterns:**

```java
// Comparing with method reference
Comparator.comparing(Person::getName)

// Primitive specializations (faster)
Comparator.comparingInt(Person::getAge)
Comparator.comparingDouble(Person::getSalary)

// Chaining
Comparator.comparing(Person::getDept)
          .thenComparingInt(Person::getAge)
          .thenComparing(Person::getName)

// Null safety
Comparator.comparing(Person::getManager,
    Comparator.nullsLast(Comparator.naturalOrder()))
```

**5. Performance tips:**

```
- Use comparingInt/Long/Double (no boxing)
- Precompute expensive keys
- Use primitive arrays for large data
- Cache comparator instances
- Profile before optimizing
```

---

# 7. Collection Performance and Big O Analysis
---

## Summary

### Performance Cheat Sheet

**Time Complexity:**

```
┌──────────────┬──────────┬──────────┬───────────┬──────────┐
│ Collection   │ Add      │ Get      │ Contains  │ Remove   │
├──────────────┼──────────┼──────────┼───────────┼──────────┤
│ ArrayList    │ O(1)*    │ O(1)     │ O(n)      │ O(n)     │
│ LinkedList   │ O(1)     │ O(n)     │ O(n)      │ O(1)**   │
│ HashSet      │ O(1)     │ N/A      │ O(1)      │ O(1)     │
│ TreeSet      │ O(log n) │ N/A      │ O(log n)  │ O(log n) │
│ HashMap      │ O(1)     │ O(1)     │ O(1)      │ O(1)     │
│ TreeMap      │ O(log n) │ O(log n) │ O(log n)  │ O(log n) │
│ ArrayDeque   │ O(1)*    │ N/A      │ O(n)      │ O(1)     │
│ PriorityQueue│ O(log n) │ O(1)***  │ O(n)      │ O(log n) │
└──────────────┴──────────┴──────────┴───────────┴──────────┘

*   Amortized
**  At iterator position
*** Only peek/poll
```

**Space Complexity:**

```
┌──────────────┬──────────────┬──────────────┐
│ Collection   │ Overhead/Elem│ 1000 Elements│
├──────────────┼──────────────┼──────────────┤
│ ArrayList    │ 8 bytes      │ ~8 KB        │
│ LinkedList   │ 40 bytes     │ ~40 KB       │
│ HashMap      │ 40 bytes     │ ~64 KB*      │
│ TreeMap      │ 48 bytes     │ ~48 KB       │
│ ArrayDeque   │ 8 bytes      │ ~8 KB        │
└──────────────┴──────────────┴──────────────┘

* Includes load factor overhead
```

**Cache Locality:**

```
✅ Excellent:  ArrayList, ArrayDeque, primitive arrays
🟢 Good:       HashMap (moderate)
🟡 Fair:       TreeMap
❌ Poor:       LinkedList
```

### Key Takeaways

**1. Default choices (95% of cases):**

```java
List<E> list = new ArrayList<>();
Set<E> set = new HashSet<>();
Map<K,V> map = new HashMap<>();
Deque<E> queue = new ArrayDeque<>();
```

**2. Performance rules:**

```
- ArrayList beats LinkedList (99% of time)
- HashMap beats TreeMap (unless need sorted)
- ArrayDeque beats LinkedList (always)
- Cache locality matters (array > linked)
```

**3. Sizing matters:**

```java
// ❌ BAD
List<E> list = new ArrayList<>();  // Default capacity 10

// ✅ GOOD
List<E> list = new ArrayList<>(expectedSize);  // No resizes!
```

**4. Amortized analysis:**

```
ArrayList.add(): O(1) amortized
- Most adds: O(1)
- Rare resize: O(n)
- Average: O(1) ✅
```

**5. Use JMH for benchmarks:**

```
- Proper warmup
- Statistical analysis
- Dead code elimination prevention
- Production-realistic results
```

---

# 8. Immutable Collections and Defensive Copying
---

## Summary

### Quick Reference

**Immutability Options:**

```java
// JDK Unmodifiable (view)
List<String> unmod = Collections.unmodifiableList(list);
// ⚠️ View, not copy - changes visible!

// Java 9+ (truly immutable)
List<String> immutable = List.of("a", "b", "c");
Set<Integer> immutableSet = Set.of(1, 2, 3);
Map<String, Integer> immutableMap = Map.of("a", 1, "b", 2);
// ✅ Truly immutable, null-hostile, optimized

// Guava (most features)
ImmutableList<String> guava = ImmutableList.of("a", "b", "c");
ImmutableSet<String> guavaSet = ImmutableSet.copyOf(list);
ImmutableMap<String, Integer> guavaMap = 
    ImmutableMap.<String, Integer>builder()
        .put("a", 1)
        .put("b", 2)
        .build();
// ✅ Rich API, builder pattern, Java 8 compatible
```

**Comparison Table:**

```
┌────────────────────┬─────────┬────────────┬─────────┬─────────┐
│ Feature            │ Unmod   │ List.of()  │ Guava   │ Mutable │
├────────────────────┼─────────┼────────────┼─────────┼─────────┤
│ Truly immutable    │ No ❌   │ Yes ✅     │ Yes ✅  │ No      │
│ Null support       │ Yes     │ No         │ No      │ Yes     │
│ Memory efficient   │ Yes     │ Yes ✅     │ Yes ✅  │ No      │
│ Thread-safe        │ Read ✅ │ Yes ✅     │ Yes ✅  │ No ❌   │
│ Builder pattern    │ No      │ No         │ Yes ✅  │ N/A     │
│ Java version       │ 1.2+    │ 9+         │ Any     │ Any     │
│ Creation cost      │ O(1)    │ O(n)       │ O(n)    │ O(1)    │
└────────────────────┴─────────┴────────────┴─────────┴─────────┘
```

**Performance:**

```
Read operations: Identical (all O(1) for get/contains)
Memory: Immutable 20-40% less than ArrayList
Creation: Immutable +5-10% slower than mutable
```

### Key Takeaways

**1. Prefer immutability:**

```java
// ✅ GOOD - Immutable by default
private final List<String> items = List.of("a", "b", "c");

// ❌ BAD - Mutable by default
private List<String> items = new ArrayList<>();
```

**2. Defensive copying:**

```java
// Constructor
public MyClass(List<String> items) {
    this.items = List.copyOf(items);  // Defensive copy
}

// Getter
public List<String> getItems() {
    return items;  // Already immutable, safe!
}
```

**3. Thread safety:**

```java
// ✅ Thread-safe without locks
private volatile ImmutableMap<K, V> cache = ImmutableMap.of();

// Update atomically
cache = ImmutableMap.<K, V>builder()
    .putAll(cache)
    .putAll(updates)
    .build();
```

**4. Use builders for complexity:**

```java
ImmutableList<String> list = ImmutableList.<String>builder()
    .add("a")
    .add("b")
    .addAll(otherList)
    .build();
```

**5. When NOT to use:**

```
- Building large collections incrementally
- Frequent modifications in hot path
- Working with legacy mutable APIs
→ Use mutable, then convert to immutable
```

---
