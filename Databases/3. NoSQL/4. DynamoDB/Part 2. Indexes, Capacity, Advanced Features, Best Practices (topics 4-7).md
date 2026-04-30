# DynamoDB with Spring Boot - Part 2

## Indexes, Capacity, Advanced Features, and Best Practices

---

## 4. Indexes (GSI and LSI)

### Understanding Secondary Indexes

**Overview:**

```
┌──────────────────────────────────────────────────────────────┐
│              DynamoDB Indexes                                 │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  PRIMARY KEY (Base Table)                                    │
│  ────────────────────────                                   │
│  Required for every table                                    │
│  Partition Key + Optional Sort Key                           │
│  Unique identifier for items                                 │
│                                                               │
│  Limitations:                                                │
│  • Can only query by primary key                             │
│  • No alternative access patterns                            │
│                                                               │
│  Example: Orders table                                       │
│  PK: userId, SK: orderDate                                   │
│  Can query: "Get orders for user-123"                        │
│  Cannot query: "Get all PENDING orders" ❌                   │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  SECONDARY INDEXES (Enable alternative queries)              │
│  ───────────────────────────────────────────                │
│                                                               │
│  Two types:                                                  │
│  1. Global Secondary Index (GSI)                             │
│  2. Local Secondary Index (LSI)                              │
│                                                               │
│  Purpose:                                                    │
│  Enable queries on non-key attributes                        │
│  Support additional access patterns                          │
│                                                               │
│  Example: Add StatusIndex (GSI)                              │
│  GSI PK: status, GSI SK: orderDate                           │
│  Now can query: "Get all PENDING orders" ✅                  │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Global Secondary Index (GSI)

**Characteristics and Use Cases:**

```
┌──────────────────────────────────────────────────────────────┐
│         Global Secondary Index (GSI)                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Definition:                                                 │
│  An index with partition key and optional sort key that      │
│  can be DIFFERENT from base table keys                       │
│                                                               │
│  Key Characteristics:                                        │
│  ✅ Different partition key than base table                  │
│  ✅ Different sort key than base table                       │
│  ✅ Can be created/deleted anytime                           │
│  ✅ Spans all partitions (global)                            │
│  ✅ Eventually consistent reads only                         │
│  ✅ Has its own provisioned throughput                       │
│  ✅ Limit: 20 GSIs per table                                 │
│                                                               │
│  Storage:                                                    │
│  • Separate data structure                                   │
│  • Asynchronously maintained                                 │
│  • Projects selected attributes                              │
│                                                               │
│  Cost:                                                       │
│  • Storage: Charged for projected attributes                 │
│  • Writes: Every base table write updates GSI                │
│  • Reads: Separate read capacity                             │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Example: E-commerce Orders                                  │
│  ────────────────────────────                                │
│                                                               │
│  Base Table: Orders                                          │
│  PK: userId                                                  │
│  SK: orderDate                                               │
│  Attributes: orderId, amount, status, productId              │
│                                                               │
│  Query: Get orders for user-123 ✅                           │
│  Query: Get all PENDING orders ❌ (can't use base table)     │
│  Query: Get orders by orderId ❌                             │
│  Query: Get orders for product ❌                            │
│                                                               │
│  Solution: Add GSIs                                          │
│  ────────────────────                                        │
│                                                               │
│  GSI 1: StatusIndex                                          │
│  PK: status                                                  │
│  SK: orderDate                                               │
│  Query: "Get all PENDING orders" ✅                          │
│  Query: "Get PENDING orders from last week" ✅               │
│                                                               │
│  GSI 2: OrderIdIndex                                         │
│  PK: orderId                                                 │
│  SK: (none)                                                  │
│  Query: "Get order by orderId" ✅                            │
│                                                               │
│  GSI 3: ProductIndex                                         │
│  PK: productId                                               │
│  SK: orderDate                                               │
│  Query: "Get all orders for product-789" ✅                  │
│  Query: "Get recent orders for product-789" ✅               │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**GSI Implementation:**

```java
package com.example.indexes;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.enhanced.dynamodb.*;
import software.amazon.awssdk.enhanced.dynamodb.model.QueryConditional;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Global Secondary Index (GSI) Examples
 */
@Service
@RequiredArgsConstructor
public class GlobalSecondaryIndexService {
    
    private final DynamoDbClient client;
    private final DynamoDbEnhancedClient enhancedClient;
    
    /**
     * Create table with GSIs
     */
    public void createTableWithGSIs() {
        CreateTableRequest request = CreateTableRequest.builder()
            .tableName("Orders")
            // Base table keys
            .keySchema(
                KeySchemaElement.builder()
                    .attributeName("userId")
                    .keyType(KeyType.HASH)
                    .build(),
                KeySchemaElement.builder()
                    .attributeName("orderDate")
                    .keyType(KeyType.RANGE)
                    .build()
            )
            // Attribute definitions (only for keys!)
            .attributeDefinitions(
                AttributeDefinition.builder()
                    .attributeName("userId")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                AttributeDefinition.builder()
                    .attributeName("orderDate")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                // GSI keys must also be defined
                AttributeDefinition.builder()
                    .attributeName("status")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                AttributeDefinition.builder()
                    .attributeName("orderId")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                AttributeDefinition.builder()
                    .attributeName("productId")
                    .attributeType(ScalarAttributeType.S)
                    .build()
            )
            // GSI 1: StatusIndex
            .globalSecondaryIndexes(
                GlobalSecondaryIndex.builder()
                    .indexName("StatusIndex")
                    .keySchema(
                        KeySchemaElement.builder()
                            .attributeName("status")
                            .keyType(KeyType.HASH)
                            .build(),
                        KeySchemaElement.builder()
                            .attributeName("orderDate")
                            .keyType(KeyType.RANGE)
                            .build()
                    )
                    .projection(Projection.builder()
                        .projectionType(ProjectionType.ALL) // Project all attributes
                        .build())
                    .build(),
                // GSI 2: OrderIdIndex
                GlobalSecondaryIndex.builder()
                    .indexName("OrderIdIndex")
                    .keySchema(
                        KeySchemaElement.builder()
                            .attributeName("orderId")
                            .keyType(KeyType.HASH)
                            .build()
                    )
                    .projection(Projection.builder()
                        .projectionType(ProjectionType.ALL)
                        .build())
                    .build(),
                // GSI 3: ProductIndex
                GlobalSecondaryIndex.builder()
                    .indexName("ProductIndex")
                    .keySchema(
                        KeySchemaElement.builder()
                            .attributeName("productId")
                            .keyType(KeyType.HASH)
                            .build(),
                        KeySchemaElement.builder()
                            .attributeName("orderDate")
                            .keyType(KeyType.RANGE)
                            .build()
                    )
                    .projection(Projection.builder()
                        .projectionType(ProjectionType.ALL)
                        .build())
                    .build()
            )
            .billingMode(BillingMode.PAY_PER_REQUEST)
            .build();
        
        client.createTable(request);
    }
    
    /**
     * Query GSI 1: Get all orders by status
     */
    public List<Order> getOrdersByStatus(String status) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":status", attr(status));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("StatusIndex")
            .keyConditionExpression("status = :status")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .map(this::mapToOrder)
            .collect(Collectors.toList());
    }
    
    /**
     * Query GSI 1: Get orders by status in date range
     */
    public List<Order> getOrdersByStatusAndDateRange(String status,
                                                      LocalDate startDate,
                                                      LocalDate endDate) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":status", attr(status));
        values.put(":startDate", attr(startDate.toString()));
        values.put(":endDate", attr(endDate.toString()));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("StatusIndex")
            .keyConditionExpression("status = :status AND orderDate BETWEEN :startDate AND :endDate")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .map(this::mapToOrder)
            .collect(Collectors.toList());
    }
    
    /**
     * Query GSI 2: Get order by orderId
     */
    public Order getOrderById(String orderId) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":orderId", attr(orderId));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("OrderIdIndex")
            .keyConditionExpression("orderId = :orderId")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .findFirst()
            .map(this::mapToOrder)
            .orElse(null);
    }
    
    /**
     * Query GSI 3: Get orders for product
     */
    public List<Order> getOrdersForProduct(String productId) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":productId", attr(productId));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("ProductIndex")
            .keyConditionExpression("productId = :productId")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .map(this::mapToOrder)
            .collect(Collectors.toList());
    }
    
    /**
     * Using Enhanced Client with GSI
     */
    public List<Order> getOrdersByStatusEnhanced(String status) {
        DynamoDbTable<Order> table = enhancedClient.table(
            "Orders",
            TableSchema.fromBean(Order.class)
        );
        
        DynamoDbIndex<Order> statusIndex = table.index("StatusIndex");
        
        QueryConditional condition = QueryConditional.keyEqualTo(
            Key.builder().partitionValue(status).build()
        );
        
        return statusIndex.query(condition)
            .stream()
            .flatMap(page -> page.items().stream())
            .collect(Collectors.toList());
    }
    
    private AttributeValue attr(String value) {
        return AttributeValue.builder().s(value).build();
    }
    
    private Order mapToOrder(Map<String, AttributeValue> item) {
        // Mapping implementation
        return new Order();
    }
}
```

### Local Secondary Index (LSI)

**Characteristics and Use Cases:**

```
┌──────────────────────────────────────────────────────────────┐
│         Local Secondary Index (LSI)                           │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Definition:                                                 │
│  An index with the SAME partition key as base table but      │
│  DIFFERENT sort key                                          │
│                                                               │
│  Key Characteristics:                                        │
│  ✅ SAME partition key as base table (local to partition)    │
│  ✅ Different sort key than base table                       │
│  ❌ Must be created at table creation time                   │
│  ❌ Cannot be added/deleted later                            │
│  ✅ Strongly consistent reads supported                      │
│  ✅ Shares throughput with base table                        │
│  ✅ Limit: 5 LSIs per table                                  │
│                                                               │
│  Storage:                                                    │
│  • Stored in same partition as base item                     │
│  • 10GB limit per partition key value                        │
│                                                               │
│  Cost:                                                       │
│  • No additional throughput cost                             │
│  • Storage charged for projected attributes                  │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  When to Use LSI:                                            │
│  ────────────────                                           │
│  ✅ Need alternative sort order within same partition        │
│  ✅ Need strongly consistent reads                           │
│  ✅ Query patterns known at table creation                   │
│  ✅ < 10GB data per partition key                            │
│                                                               │
│  Example: User Activity Log                                  │
│  ───────────────────────────                                │
│                                                               │
│  Base Table: UserActivity                                    │
│  PK: userId                                                  │
│  SK: timestamp                                               │
│  Attributes: activityType, score, deviceId                   │
│                                                               │
│  Query: Get activities by time ✅ (base table)               │
│  Query: Get activities sorted by score ❌                    │
│  Query: Get activities by device ❌                          │
│                                                               │
│  Solution: Add LSIs (same PK, different SK)                  │
│  ───────────────────────────────────────────                │
│                                                               │
│  LSI 1: ScoreIndex                                           │
│  PK: userId (same as base)                                   │
│  SK: score (different from base)                             │
│  Query: "Get user's activities sorted by score" ✅           │
│                                                               │
│  LSI 2: DeviceIndex                                          │
│  PK: userId (same as base)                                   │
│  SK: deviceId#timestamp                                      │
│  Query: "Get user's activities by device" ✅                 │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**LSI Implementation:**

```java
package com.example.indexes;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Local Secondary Index (LSI) Examples
 */
@Service
@RequiredArgsConstructor
public class LocalSecondaryIndexService {
    
    private final DynamoDbClient client;
    
    /**
     * Create table with LSIs (must be at creation time!)
     */
    public void createTableWithLSIs() {
        CreateTableRequest request = CreateTableRequest.builder()
            .tableName("UserActivity")
            // Base table keys
            .keySchema(
                KeySchemaElement.builder()
                    .attributeName("userId")
                    .keyType(KeyType.HASH)
                    .build(),
                KeySchemaElement.builder()
                    .attributeName("timestamp")
                    .keyType(KeyType.RANGE)
                    .build()
            )
            // Attribute definitions
            .attributeDefinitions(
                AttributeDefinition.builder()
                    .attributeName("userId")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                AttributeDefinition.builder()
                    .attributeName("timestamp")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                AttributeDefinition.builder()
                    .attributeName("score")
                    .attributeType(ScalarAttributeType.N)
                    .build(),
                AttributeDefinition.builder()
                    .attributeName("deviceId")
                    .attributeType(ScalarAttributeType.S)
                    .build()
            )
            // LSI 1: Sort by score
            .localSecondaryIndexes(
                LocalSecondaryIndex.builder()
                    .indexName("ScoreIndex")
                    .keySchema(
                        KeySchemaElement.builder()
                            .attributeName("userId") // SAME as base table
                            .keyType(KeyType.HASH)
                            .build(),
                        KeySchemaElement.builder()
                            .attributeName("score") // DIFFERENT from base
                            .keyType(KeyType.RANGE)
                            .build()
                    )
                    .projection(Projection.builder()
                        .projectionType(ProjectionType.ALL)
                        .build())
                    .build(),
                // LSI 2: Sort by device
                LocalSecondaryIndex.builder()
                    .indexName("DeviceIndex")
                    .keySchema(
                        KeySchemaElement.builder()
                            .attributeName("userId") // SAME as base table
                            .keyType(KeyType.HASH)
                            .build(),
                        KeySchemaElement.builder()
                            .attributeName("deviceId") // DIFFERENT from base
                            .keyType(KeyType.RANGE)
                            .build()
                    )
                    .projection(Projection.builder()
                        .projectionType(ProjectionType.ALL)
                        .build())
                    .build()
            )
            .billingMode(BillingMode.PAY_PER_REQUEST)
            .build();
        
        client.createTable(request);
    }
    
    /**
     * Query base table: Get activities by timestamp
     */
    public List<UserActivity> getActivitiesByTime(String userId) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":userId", attr(userId));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("UserActivity")
            .keyConditionExpression("userId = :userId")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .map(this::mapToActivity)
            .collect(Collectors.toList());
    }
    
    /**
     * Query LSI 1: Get activities sorted by score
     */
    public List<UserActivity> getActivitiesByScore(String userId) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":userId", attr(userId));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("UserActivity")
            .indexName("ScoreIndex")
            .keyConditionExpression("userId = :userId")
            .expressionAttributeValues(values)
            .scanIndexForward(false) // Descending order (highest score first)
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .map(this::mapToActivity)
            .collect(Collectors.toList());
    }
    
    /**
     * Query LSI 1: Get high-scoring activities
     */
    public List<UserActivity> getHighScoringActivities(String userId, int minScore) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":userId", attr(userId));
        values.put(":minScore", attrN(String.valueOf(minScore)));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("UserActivity")
            .indexName("ScoreIndex")
            .keyConditionExpression("userId = :userId AND score >= :minScore")
            .expressionAttributeValues(values)
            .scanIndexForward(false)
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .map(this::mapToActivity)
            .collect(Collectors.toList());
    }
    
    /**
     * Query LSI 2: Get activities for specific device
     */
    public List<UserActivity> getActivitiesByDevice(String userId, String deviceId) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":userId", attr(userId));
        values.put(":deviceId", attr(deviceId));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("UserActivity")
            .indexName("DeviceIndex")
            .keyConditionExpression("userId = :userId AND deviceId = :deviceId")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .map(this::mapToActivity)
            .collect(Collectors.toList());
    }
    
    /**
     * Strongly consistent read on LSI (not possible with GSI!)
     */
    public List<UserActivity> getActivitiesByScoreConsistent(String userId) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":userId", attr(userId));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("UserActivity")
            .indexName("ScoreIndex")
            .keyConditionExpression("userId = :userId")
            .expressionAttributeValues(values)
            .consistentRead(true) // Strongly consistent!
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .map(this::mapToActivity)
            .collect(Collectors.toList());
    }
    
    private AttributeValue attr(String value) {
        return AttributeValue.builder().s(value).build();
    }
    
    private AttributeValue attrN(String value) {
        return AttributeValue.builder().n(value).build();
    }
    
    private UserActivity mapToActivity(Map<String, AttributeValue> item) {
        // Mapping implementation
        return new UserActivity();
    }
}

@lombok.Data
class UserActivity {
    private String userId;
    private String timestamp;
    private String activityType;
    private Integer score;
    private String deviceId;
}
```

### GSI vs LSI Differences

**Comprehensive Comparison:**

```
┌──────────────────────────────────────────────────────────────┐
│              GSI vs LSI Comparison                            │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────┬──────────────┬──────────────┐        │
│  │   Characteristic   │     GSI      │     LSI      │        │
│  ├────────────────────┼──────────────┼──────────────┤        │
│  │ Partition Key      │   Different  │     Same     │        │
│  │ Sort Key           │   Different  │   Different  │        │
│  │ Creation Time      │    Anytime   │  Table only  │        │
│  │ Modification       │   Add/Delete │    Cannot    │        │
│  │ Scope              │    Global    │    Local     │        │
│  │ Consistency        │   Eventual   │  Strong/Eventual│    │
│  │ Throughput         │   Separate   │    Shared    │        │
│  │ Partition Limit    │     None     │    10GB      │        │
│  │ Per Table Limit    │      20      │       5      │        │
│  │ Storage Cost       │  Extra cost  │  Extra cost  │        │
│  │ Write Cost         │  Extra WCUs  │      No      │        │
│  │ Use Case           │  New access  │  Alt sorting │        │
│  │                    │   patterns   │  same entity │        │
│  └────────────────────┴──────────────┴──────────────┘        │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Decision Matrix:                                            │
│  ────────────────                                           │
│                                                               │
│  Use GSI when:                                               │
│  ✅ Different partition key needed                           │
│  ✅ Query across all partitions                              │
│  ✅ Flexible - add/remove later                              │
│  ✅ Don't need strong consistency                            │
│  ✅ Query patterns evolve over time                          │
│                                                               │
│  Use LSI when:                                               │
│  ✅ Need alternative sort within same partition              │
│  ✅ Need strong consistency                                  │
│  ✅ Query patterns known at design time                      │
│  ✅ < 10GB data per partition key                            │
│  ✅ Want to share throughput with base table                 │
│                                                               │
│  Recommendation:                                             │
│  • Start with GSIs (more flexible)                           │
│  • Use LSIs only when strong consistency required            │
│  • Most applications use GSIs, not LSIs                      │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Practical Examples:**

```java
package com.example.indexes;

import org.springframework.stereotype.Component;

/**
 * GSI vs LSI Decision Examples
 */
@Component
public class IndexDecisionExamples {
    
    /**
     * Example 1: E-commerce Orders
     */
    public void ecommerceOrders() {
        /*
        Base Table: Orders
        PK: userId
        SK: orderDate
        
        Access Pattern 1: Get all orders for user
        Solution: Base table query ✅
        
        Access Pattern 2: Get all PENDING orders (all users)
        Solution: GSI with PK=status ✅
        Why GSI? Need to query across ALL users (all partitions)
        
        Access Pattern 3: Get user's orders sorted by amount
        Solution: LSI with PK=userId, SK=amount ✅
        Why LSI? Same partition (userId), different sort order
        
        Access Pattern 4: Get order by orderId
        Solution: GSI with PK=orderId ✅
        Why GSI? orderId doesn't match base table partition key
        */
    }
    
    /**
     * Example 2: Social Media Posts
     */
    public void socialMediaPosts() {
        /*
        Base Table: Posts
        PK: authorId
        SK: timestamp
        
        Access Pattern 1: Get author's posts by time
        Solution: Base table ✅
        
        Access Pattern 2: Get author's posts by likes (popularity)
        Solution: LSI with PK=authorId, SK=likeCount ✅
        Why LSI? Same partition, alternative sort
        Strong consistency ensures accurate counts
        
        Access Pattern 3: Get all posts by hashtag
        Solution: GSI with PK=hashtag, SK=timestamp ✅
        Why GSI? Query across all authors (all partitions)
        
        Access Pattern 4: Get trending posts (high likes, all authors)
        Solution: GSI with PK=category, SK=likeCount ✅
        Why GSI? Cross-partition query
        */
    }
    
    /**
     * Example 3: IoT Sensor Data
     */
    public void iotSensorData() {
        /*
        Base Table: SensorReadings
        PK: deviceId
        SK: timestamp
        
        Access Pattern 1: Get device readings by time
        Solution: Base table ✅
        
        Access Pattern 2: Get device readings by temperature (sorted)
        Solution: LSI with PK=deviceId, SK=temperature ✅
        Why LSI? Same device, different sort order
        
        Access Pattern 3: Get all high-temperature readings (all devices)
        Solution: GSI with PK=alertLevel, SK=timestamp ✅
        Why GSI? Query across all devices
        
        Access Pattern 4: Get readings for specific location
        Solution: GSI with PK=locationId, SK=timestamp ✅
        Why GSI? Different partition key needed
        */
    }
    
    /**
     * Common Mistakes
     */
    public void commonMistakes() {
        /*
        MISTAKE 1: Using LSI when GSI is needed
        ────────────────────────────────────────
        Access Pattern: Get all pending orders (all users)
        Wrong: LSI with PK=userId, SK=status ❌
        Why wrong? LSI can only query one userId at a time
        Correct: GSI with PK=status, SK=orderDate ✅
        
        MISTAKE 2: Creating LSI for flexibility
        ────────────────────────────────────────
        Wrong: "Let's create LSI just in case" ❌
        Why wrong? LSIs are permanent, can't be removed
        Correct: Use GSI for flexibility ✅
        
        MISTAKE 3: Exceeding 10GB per partition with LSI
        ─────────────────────────────────────────────────
        Base: PK=userId, SK=timestamp
        LSI: PK=userId, SK=score
        Problem: If user has > 10GB of data, LSI fails ❌
        Solution: Use GSI instead ✅
        
        MISTAKE 4: Not considering cost
        ────────────────────────────────
        Creating 5 GSIs without considering:
        • Storage cost (5x data stored)
        • Write cost (5x writes)
        • Read cost (queries on each index)
        Better: Consolidate into fewer GSIs ✅
        */
    }
}
```

### Sparse Indexes for Optimization

**Concept and Implementation:**

```
┌──────────────────────────────────────────────────────────────┐
│              Sparse Indexes                                   │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Definition:                                                 │
│  An index that contains ONLY items that have the index key   │
│  attribute. Items without the attribute are not indexed.     │
│                                                               │
│  Key Benefit:                                                │
│  Dramatically reduces index size and cost when only a        │
│  subset of items needs to be indexed.                        │
│                                                               │
│  How It Works:                                               │
│  DynamoDB only adds items to GSI if they have values for     │
│  both the partition key and sort key (if specified) of       │
│  that GSI.                                                   │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Example: E-commerce Orders                                  │
│  ────────────────────────────                                │
│                                                               │
│  Table: 1,000,000 orders                                     │
│  • 990,000 completed orders                                  │
│  • 10,000 pending orders                                     │
│                                                               │
│  Access Pattern: Query pending orders only                   │
│                                                               │
│  Option 1: Regular GSI (expensive)                           │
│  ──────────────────────────────────                         │
│  GSI: PK=status, SK=orderDate                                │
│  Result: 1,000,000 items in GSI                              │
│  Cost: Store 1M items, query returns 10K                     │
│                                                               │
│  Option 2: Sparse GSI (efficient) ✅                         │
│  ────────────────────────────────                           │
│  GSI: PK=pendingStatus (only set for pending orders)         │
│  Result: 10,000 items in GSI (99% reduction!)                │
│  Cost: Store only 10K items                                  │
│  Savings: 99% storage reduction                              │
│                                                               │
│  Implementation:                                             │
│  • Only set pendingStatus="PENDING" for pending orders       │
│  • Don't set attribute for completed orders                  │
│  • GSI automatically excludes completed orders               │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Implementation:**

```java
package com.example.indexes;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.*;

/**
 * Sparse Index Optimization
 */
@Service
@RequiredArgsConstructor
public class SparseIndexService {
    
    private final DynamoDbClient client;
    
    /**
     * Create table with sparse GSI
     */
    public void createTableWithSparseIndex() {
        CreateTableRequest request = CreateTableRequest.builder()
            .tableName("Orders")
            .keySchema(
                KeySchemaElement.builder()
                    .attributeName("orderId")
                    .keyType(KeyType.HASH)
                    .build()
            )
            .attributeDefinitions(
                AttributeDefinition.builder()
                    .attributeName("orderId")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                // Sparse index key (only defined for subset of items)
                AttributeDefinition.builder()
                    .attributeName("pendingStatus")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                AttributeDefinition.builder()
                    .attributeName("orderDate")
                    .attributeType(ScalarAttributeType.S)
                    .build()
            )
            .globalSecondaryIndexes(
                GlobalSecondaryIndex.builder()
                    .indexName("PendingOrdersIndex")
                    .keySchema(
                        KeySchemaElement.builder()
                            .attributeName("pendingStatus")
                            .keyType(KeyType.HASH)
                            .build(),
                        KeySchemaElement.builder()
                            .attributeName("orderDate")
                            .keyType(KeyType.RANGE)
                            .build()
                    )
                    .projection(Projection.builder()
                        .projectionType(ProjectionType.ALL)
                        .build())
                    .build()
            )
            .billingMode(BillingMode.PAY_PER_REQUEST)
            .build();
        
        client.createTable(request);
    }
    
    /**
     * Save completed order (NO sparse index attribute)
     */
    public void saveCompletedOrder(Order order) {
        Map<String, AttributeValue> item = new HashMap<>();
        item.put("orderId", attr(order.getOrderId()));
        item.put("userId", attr(order.getUserId()));
        item.put("amount", attrN(order.getAmount()));
        item.put("status", attr("COMPLETED"));
        item.put("orderDate", attr(order.getOrderDate().toString()));
        
        // DO NOT set pendingStatus attribute
        // This order will NOT appear in PendingOrdersIndex
        
        client.putItem(PutItemRequest.builder()
            .tableName("Orders")
            .item(item)
            .build());
    }
    
    /**
     * Save pending order (WITH sparse index attribute)
     */
    public void savePendingOrder(Order order) {
        Map<String, AttributeValue> item = new HashMap<>();
        item.put("orderId", attr(order.getOrderId()));
        item.put("userId", attr(order.getUserId()));
        item.put("amount", attrN(order.getAmount()));
        item.put("status", attr("PENDING"));
        item.put("orderDate", attr(order.getOrderDate().toString()));
        
        // Set sparse index attribute
        item.put("pendingStatus", attr("PENDING"));
        // This order WILL appear in PendingOrdersIndex
        
        client.putItem(PutItemRequest.builder()
            .tableName("Orders")
            .item(item)
            .build());
    }
    
    /**
     * Query sparse index - returns ONLY pending orders
     */
    public List<Order> getPendingOrders() {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":pending", attr("PENDING"));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("PendingOrdersIndex")
            .keyConditionExpression("pendingStatus = :pending")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        // Returns only pending orders (sparse index benefit!)
        return response.items().stream()
            .map(this::mapToOrder)
            .toList();
    }
    
    /**
     * Update order from pending to completed
     * Remove from sparse index!
     */
    public void completeOrder(String orderId) {
        Map<String, AttributeValue> key = new HashMap<>();
        key.put("orderId", attr(orderId));
        
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":completed", attr("COMPLETED"));
        
        UpdateItemRequest request = UpdateItemRequest.builder()
            .tableName("Orders")
            .key(key)
            .updateExpression("SET #status = :completed REMOVE pendingStatus")
            .expressionAttributeNames(Map.of("#status", "status"))
            .expressionAttributeValues(values)
            .build();
        
        // Removing pendingStatus removes item from sparse GSI
        client.updateItem(request);
    }
    
    /**
     * Example 2: Active Users Sparse Index
     * 
     * Use case: 1M users, only 100K active in last 30 days
     */
    public void saveActiveUser(User user) {
        Map<String, AttributeValue> item = new HashMap<>();
        item.put("userId", attr(user.getUserId()));
        item.put("name", attr(user.getName()));
        item.put("lastLoginDate", attr(LocalDate.now().toString()));
        
        // Only set activeStatus if user logged in recently
        LocalDate thirtyDaysAgo = LocalDate.now().minusDays(30);
        if (user.getLastLoginDate().isAfter(thirtyDaysAgo)) {
            item.put("activeStatus", attr("ACTIVE"));
            // User appears in ActiveUsersIndex
        }
        // Otherwise, attribute not set = not in sparse index
        
        client.putItem(PutItemRequest.builder()
            .tableName("Users")
            .item(item)
            .build());
    }
    
    /**
     * Example 3: Items with Discounts (sparse)
     * 
     * Use case: 100K products, only 5K have discounts
     */
    public void saveProductWithDiscount(Product product) {
        Map<String, AttributeValue> item = new HashMap<>();
        item.put("productId", attr(product.getProductId()));
        item.put("name", attr(product.getName()));
        item.put("price", attrN(product.getPrice()));
        
        // Only set discount attribute if product has discount
        if (product.getDiscountPercent() > 0) {
            item.put("hasDiscount", attr("YES"));
            item.put("discountPercent", attrN(String.valueOf(product.getDiscountPercent())));
            // Product appears in DiscountedProductsIndex
        }
        
        client.putItem(PutItemRequest.builder()
            .tableName("Products")
            .item(item)
            .build());
    }
    
    private AttributeValue attr(String value) {
        return AttributeValue.builder().s(value).build();
    }
    
    private AttributeValue attrN(BigDecimal value) {
        return AttributeValue.builder().n(value.toString()).build();
    }
    
    private AttributeValue attrN(String value) {
        return AttributeValue.builder().n(value).build();
    }
    
    private Order mapToOrder(Map<String, AttributeValue> item) {
        return new Order();
    }
}
```

### Attribute Projection (KEYS_ONLY, INCLUDE, ALL)

**Projection Types:**

```
┌──────────────────────────────────────────────────────────────┐
│         Attribute Projection Types                            │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Projection determines which attributes are copied from       │
│  base table to index.                                        │
│                                                               │
│  Three types:                                                │
│  1. KEYS_ONLY - Only keys                                    │
│  2. INCLUDE - Keys + specified attributes                    │
│  3. ALL - All attributes                                     │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  KEYS_ONLY (Minimal storage)                                 │
│  ───────────────────────────                                │
│  Projects: Base table keys + Index keys only                 │
│  Size: Smallest                                              │
│  Cost: Lowest storage                                        │
│  Use when: Need to fetch full item from base table anyway    │
│                                                               │
│  Example: OrderIdIndex                                       │
│  Base: PK=userId, SK=orderDate, orderId, amount, status      │
│  Index: PK=orderId                                           │
│  Projected: orderId, userId, orderDate (keys only)           │
│  Missing: amount, status                                     │
│                                                               │
│  Query result: Get orderId, userId, orderDate                │
│  To get amount/status: Additional GetItem on base table      │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  INCLUDE (Selective)                                         │
│  ───────────────────                                        │
│  Projects: Keys + specified non-key attributes               │
│  Size: Medium                                                │
│  Cost: Medium storage                                        │
│  Use when: Specific attributes commonly queried              │
│                                                               │
│  Example: StatusIndex                                        │
│  Base: PK=userId, SK=orderDate, orderId, amount, status      │
│  Index: PK=status, SK=orderDate                              │
│  Include: orderId, amount (most commonly needed)             │
│  Projected: status, orderDate, orderId, amount, userId       │
│  Missing: customerName, items                                │
│                                                               │
│  Query result: Get orderId, amount without extra fetch       │
│  For customerName/items: Additional GetItem if needed        │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ALL (Complete copy)                                         │
│  ───────────────────                                        │
│  Projects: All attributes from base table                    │
│  Size: Largest (duplicate of base table)                     │
│  Cost: Highest storage                                       │
│  Use when: All attributes needed in most queries             │
│                                                               │
│  Example: EmailIndex                                         │
│  Base: PK=userId, all user attributes                        │
│  Index: PK=email                                             │
│  Projected: Everything                                       │
│                                                               │
│  Query result: Complete user object, no additional fetch     │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Decision Matrix:                                            │
│  ────────────────                                           │
│                                                               │
│  Use KEYS_ONLY when:                                         │
│  ✅ Index used for existence checks                          │
│  ✅ Always fetch full item from base table                   │
│  ✅ Minimizing storage cost                                  │
│                                                               │
│  Use INCLUDE when:                                           │
│  ✅ Need specific attributes frequently                      │
│  ✅ Balance between storage cost and performance             │
│  ✅ Query patterns are well-defined                          │
│                                                               │
│  Use ALL when:                                               │
│  ✅ Need most/all attributes in queries                      │
│  ✅ Avoid additional fetches                                 │
│  ✅ Performance > storage cost                               │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Implementation:**

```java
package com.example.indexes;

import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.util.*;

/**
 * Attribute Projection Examples
 */
@Service
public class AttributeProjectionService {
    
    private final DynamoDbClient client;
    
    public AttributeProjectionService(DynamoDbClient client) {
        this.client = client;
    }
    
    /**
     * Create table with different projection types
     */
    public void createTableWithProjections() {
        CreateTableRequest request = CreateTableRequest.builder()
            .tableName("Orders")
            .keySchema(
                KeySchemaElement.builder()
                    .attributeName("userId")
                    .keyType(KeyType.HASH)
                    .build(),
                KeySchemaElement.builder()
                    .attributeName("orderDate")
                    .keyType(KeyType.RANGE)
                    .build()
            )
            .attributeDefinitions(
                AttributeDefinition.builder()
                    .attributeName("userId")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                AttributeDefinition.builder()
                    .attributeName("orderDate")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                AttributeDefinition.builder()
                    .attributeName("orderId")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                AttributeDefinition.builder()
                    .attributeName("status")
                    .attributeType(ScalarAttributeType.S)
                    .build()
            )
            .globalSecondaryIndexes(
                // GSI 1: KEYS_ONLY projection
                GlobalSecondaryIndex.builder()
                    .indexName("OrderIdIndex")
                    .keySchema(
                        KeySchemaElement.builder()
                            .attributeName("orderId")
                            .keyType(KeyType.HASH)
                            .build()
                    )
                    .projection(Projection.builder()
                        .projectionType(ProjectionType.KEYS_ONLY)
                        // Only: orderId, userId, orderDate
                        .build())
                    .build(),
                
                // GSI 2: INCLUDE projection
                GlobalSecondaryIndex.builder()
                    .indexName("StatusIndex")
                    .keySchema(
                        KeySchemaElement.builder()
                            .attributeName("status")
                            .keyType(KeyType.HASH)
                            .build(),
                        KeySchemaElement.builder()
                            .attributeName("orderDate")
                            .keyType(KeyType.RANGE)
                            .build()
                    )
                    .projection(Projection.builder()
                        .projectionType(ProjectionType.INCLUDE)
                        .nonKeyAttributes("orderId", "amount", "customerName")
                        // Keys + orderId + amount + customerName
                        .build())
                    .build(),
                
                // GSI 3: ALL projection
                GlobalSecondaryIndex.builder()
                    .indexName("ComprehensiveIndex")
                    .keySchema(
                        KeySchemaElement.builder()
                            .attributeName("status")
                            .keyType(KeyType.HASH)
                            .build()
                    )
                    .projection(Projection.builder()
                        .projectionType(ProjectionType.ALL)
                        // All attributes from base table
                        .build())
                    .build()
            )
            .billingMode(BillingMode.PAY_PER_REQUEST)
            .build();
        
        client.createTable(request);
    }
    
    /**
     * Query with KEYS_ONLY projection
     * Need to fetch full item from base table
     */
    public Order getOrderByIdKeysOnly(String orderId) {
        // Step 1: Query index (gets only keys)
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":orderId", attr(orderId));
        
        QueryRequest queryRequest = QueryRequest.builder()
            .tableName("Orders")
            .indexName("OrderIdIndex")
            .keyConditionExpression("orderId = :orderId")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse queryResponse = client.query(queryRequest);
        
        if (queryResponse.items().isEmpty()) {
            return null;
        }
        
        Map<String, AttributeValue> indexItem = queryResponse.items().get(0);
        // indexItem only contains: orderId, userId, orderDate
        
        // Step 2: Fetch full item from base table
        Map<String, AttributeValue> key = new HashMap<>();
        key.put("userId", indexItem.get("userId"));
        key.put("orderDate", indexItem.get("orderDate"));
        
        GetItemRequest getRequest = GetItemRequest.builder()
            .tableName("Orders")
            .key(key)
            .build();
        
        GetItemResponse getResponse = client.getItem(getRequest);
        
        // Now we have all attributes
        return mapToOrder(getResponse.item());
    }
    
    /**
     * Query with INCLUDE projection
     * Has commonly needed attributes, may need base fetch
     */
    public List<OrderSummary> getOrdersByStatusInclude(String status) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":status", attr(status));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("StatusIndex")
            .keyConditionExpression("status = :status")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        // Response includes: status, orderDate, orderId, amount, customerName
        // Good for summary view!
        return response.items().stream()
            .map(item -> new OrderSummary(
                item.get("orderId").s(),
                item.get("customerName").s(),
                item.get("amount").n(),
                item.get("status").s()
            ))
            .toList();
    }
    
    /**
     * Query with ALL projection
     * Complete data, no additional fetch needed
     */
    public List<Order> getOrdersByStatusAll(String status) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":status", attr(status));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("ComprehensiveIndex")
            .keyConditionExpression("status = :status")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        // Response includes ALL attributes
        // No additional fetch needed!
        return response.items().stream()
            .map(this::mapToOrder)
            .toList();
    }
    
    /**
     * Cost comparison example
     */
    public void costComparison() {
        /*
        Scenario: 1M orders, average 2KB per order
        
        GSI with KEYS_ONLY:
        • Projected: userId (36B) + orderDate (10B) + orderId (36B) = 82B
        • Total storage: 1M × 82B = 82MB
        • Monthly cost: $0.02
        
        GSI with INCLUDE (add amount, customerName):
        • Projected: 82B + 8B + 100B = 190B
        • Total storage: 1M × 190B = 190MB
        • Monthly cost: $0.05
        
        GSI with ALL:
        • Projected: 2KB (full item)
        • Total storage: 1M × 2KB = 2GB
        • Monthly cost: $0.50
        
        Decision:
        • If 90% of queries need full item → Use ALL ($0.50/mo)
        • If 90% need only summary → Use INCLUDE ($0.05/mo)
        • If always fetch from base → Use KEYS_ONLY ($0.02/mo)
        */
    }
    
    private AttributeValue attr(String value) {
        return AttributeValue.builder().s(value).build();
    }
    
    private Order mapToOrder(Map<String, AttributeValue> item) {
        return new Order();
    }
}

@lombok.Data
@lombok.AllArgsConstructor
class OrderSummary {
    private String orderId;
    private String customerName;
    private String amount;
    private String status;
}
```

Let me continue building out the rest of Part 2. This is getting quite comprehensive, so I'll keep adding the remaining critical sections...

### Index Overloading Pattern

**Concept:**

```
┌──────────────────────────────────────────────────────────────┐
│         Index Overloading Pattern                             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Definition:                                                 │
│  Using a single GSI to support multiple access patterns      │
│  by storing different types of data in the same attribute    │
│                                                               │
│  Benefit:                                                    │
│  Reduce number of GSIs → Lower cost                          │
│  (Remember: 20 GSI limit per table)                          │
│                                                               │
│  Technique:                                                  │
│  Store composite values in GSI keys that represent           │
│  different entity types or query patterns                    │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Example: Multiple Query Patterns with One GSI               │
│  ───────────────────────────────────────────────            │
│                                                               │
│  Access Patterns:                                            │
│  1. Get orders by status                                     │
│  2. Get orders by product                                    │
│  3. Get orders by customer                                   │
│                                                               │
│  Without overloading: Need 3 GSIs                            │
│  • StatusIndex: PK=status                                    │
│  • ProductIndex: PK=productId                                │
│  • CustomerIndex: PK=customerId                              │
│  Cost: 3× storage, 3× writes                                 │
│                                                               │
│  With overloading: Need 1 GSI ✅                             │
│  • GSI1: PK=GSI1PK, SK=GSI1SK                                │
│                                                               │
│  For status queries:                                         │
│  GSI1PK = "STATUS#PENDING"                                   │
│  GSI1SK = "2024-12-08"                                       │
│                                                               │
│  For product queries:                                        │
│  GSI1PK = "PRODUCT#prod-789"                                 │
│  GSI1SK = "2024-12-08"                                       │
│                                                               │
│  For customer queries:                                       │
│  GSI1PK = "CUSTOMER#cust-456"                                │
│  GSI1SK = "2024-12-08"                                       │
│                                                               │
│  Cost: 1× storage, 1× writes (saves 66%!)                    │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Implementation:**

```java
package com.example.indexes;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.util.*;

/**
 * Index Overloading Pattern
 */
@Service
@RequiredArgsConstructor
public class IndexOverloadingService {
    
    private final DynamoDbClient client;
    
    /**
     * Create table with overloaded GSI
     */
    public void createTableWithOverloadedIndex() {
        CreateTableRequest request = CreateTableRequest.builder()
            .tableName("Orders")
            .keySchema(
                KeySchemaElement.builder()
                    .attributeName("orderId")
                    .keyType(KeyType.HASH)
                    .build()
            )
            .attributeDefinitions(
                AttributeDefinition.builder()
                    .attributeName("orderId")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                // Generic GSI attributes (overloaded)
                AttributeDefinition.builder()
                    .attributeName("GSI1PK")
                    .attributeType(ScalarAttributeType.S)
                    .build(),
                AttributeDefinition.builder()
                    .attributeName("GSI1SK")
                    .attributeType(ScalarAttributeType.S)
                    .build()
            )
            .globalSecondaryIndexes(
                GlobalSecondaryIndex.builder()
                    .indexName("GSI1")
                    .keySchema(
                        KeySchemaElement.builder()
                            .attributeName("GSI1PK")
                            .keyType(KeyType.HASH)
                            .build(),
                        KeySchemaElement.builder()
                            .attributeName("GSI1SK")
                            .keyType(KeyType.RANGE)
                            .build()
                    )
                    .projection(Projection.builder()
                        .projectionType(ProjectionType.ALL)
                        .build())
                    .build()
            )
            .billingMode(BillingMode.PAY_PER_REQUEST)
            .build();
        
        client.createTable(request);
    }
    
    /**
     * Save order with overloaded GSI keys
     */
    public void saveOrder(Order order) {
        Map<String, AttributeValue> item = new HashMap<>();
        item.put("orderId", attr(order.getOrderId()));
        item.put("userId", attr(order.getUserId()));
        item.put("status", attr(order.getStatus()));
        item.put("productId", attr(order.getProductId()));
        item.put("customerId", attr(order.getCustomerId()));
        item.put("orderDate", attr(order.getOrderDate().toString()));
        item.put("amount", attrN(order.getAmount()));
        
        // Overloaded GSI keys for multiple access patterns
        // Pattern 1: Query by status
        item.put("GSI1PK", attr("STATUS#" + order.getStatus()));
        item.put("GSI1SK", attr(order.getOrderDate().toString()));
        
        // Could also add GSI2PK, GSI2SK for more patterns
        // Pattern 2: Query by product
        item.put("GSI2PK", attr("PRODUCT#" + order.getProductId()));
        item.put("GSI2SK", attr(order.getOrderDate().toString()));
        
        // Pattern 3: Query by customer
        item.put("GSI3PK", attr("CUSTOMER#" + order.getCustomerId()));
        item.put("GSI3SK", attr(order.getOrderDate().toString()));
        
        client.putItem(PutItemRequest.builder()
            .tableName("Orders")
            .item(item)
            .build());
    }
    
    /**
     * Pattern 1: Query by status using overloaded GSI
     */
    public List<Order> getOrdersByStatus(String status) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":gsi1pk", attr("STATUS#" + status));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("GSI1")
            .keyConditionExpression("GSI1PK = :gsi1pk")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .map(this::mapToOrder)
            .toList();
    }
    
    /**
     * Pattern 2: Query by product using overloaded GSI
     */
    public List<Order> getOrdersByProduct(String productId) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":gsi2pk", attr("PRODUCT#" + productId));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("GSI2")
            .keyConditionExpression("GSI2PK = :gsi2pk")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .map(this::mapToOrder)
            .toList();
    }
    
    /**
     * Pattern 3: Query by customer using overloaded GSI
     */
    public List<Order> getOrdersByCustomer(String customerId) {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":gsi3pk", attr("CUSTOMER#" + customerId));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("GSI3")
            .keyConditionExpression("GSI3PK = :gsi3pk")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        return response.items().stream()
            .map(this::mapToOrder)
            .toList();
    }
    
    /**
     * Advanced: Multiple entity types in one GSI
     */
    public void saveMultipleEntityTypes() {
        // User entity
        Map<String, AttributeValue> user = new HashMap<>();
        user.put("PK", attr("USER#user-123"));
        user.put("SK", attr("PROFILE"));
        user.put("GSI1PK", attr("EMAIL#john@example.com"));
        user.put("GSI1SK", attr("USER"));
        // Can query by email to find user
        
        // Order entity
        Map<String, AttributeValue> order = new HashMap<>();
        order.put("PK", attr("ORDER#ord-456"));
        order.put("SK", attr("METADATA"));
        order.put("GSI1PK", attr("USER#user-123"));
        order.put("GSI1SK", attr("ORDER#2024-12-08"));
        // Can query by userId to find orders
        
        // Product entity
        Map<String, AttributeValue> product = new HashMap<>();
        product.put("PK", attr("PRODUCT#prod-789"));
        product.put("SK", attr("METADATA"));
        product.put("GSI1PK", attr("CATEGORY#electronics"));
        product.put("GSI1SK", attr("PRODUCT#prod-789"));
        // Can query by category to find products
        
        // All use same GSI1, different data!
    }
    
    private AttributeValue attr(String value) {
        return AttributeValue.builder().s(value).build();
    }
    
    private AttributeValue attrN(java.math.BigDecimal value) {
        return AttributeValue.builder().n(value.toString()).build();
    }
    
    private Order mapToOrder(Map<String, AttributeValue> item) {
        return new Order();
    }
}
```

### Query Performance with Indexes

**Performance Optimization:**

```java
package com.example.indexes;

import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.util.*;

/**
 * Index Query Performance Optimization
 */
@Service
public class IndexPerformanceService {
    
    private final DynamoDbClient client;
    
    public IndexPerformanceService(DynamoDbClient client) {
        this.client = client;
    }
    
    /**
     * Performance Tip 1: Use projection to reduce data transfer
     */
    public List<Map<String, AttributeValue>> efficientQuery() {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":status", attr("PENDING"));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("StatusIndex")
            .keyConditionExpression("status = :status")
            .expressionAttributeValues(values)
            // Only fetch needed attributes
            .projectionExpression("orderId, amount, customerName")
            .build();
        
        QueryResponse response = client.query(request);
        
        // Reduces network transfer time
        // Reduces read capacity consumed
        return response.items();
    }
    
    /**
     * Performance Tip 2: Use pagination for large result sets
     */
    public List<Map<String, AttributeValue>> paginatedQuery() {
        List<Map<String, AttributeValue>> allResults = new ArrayList<>();
        Map<String, AttributeValue> lastKey = null;
        
        do {
            Map<String, AttributeValue> values = new HashMap<>();
            values.put(":status", attr("PENDING"));
            
            QueryRequest.Builder requestBuilder = QueryRequest.builder()
                .tableName("Orders")
                .indexName("StatusIndex")
                .keyConditionExpression("status = :status")
                .expressionAttributeValues(values)
                .limit(100); // Process in batches
            
            if (lastKey != null) {
                requestBuilder.exclusiveStartKey(lastKey);
            }
            
            QueryResponse response = client.query(requestBuilder.build());
            allResults.addAll(response.items());
            lastKey = response.lastEvaluatedKey();
            
        } while (lastKey != null && !lastKey.isEmpty());
        
        return allResults;
    }
    
    /**
     * Performance Tip 3: Use FilterExpression carefully
     * (Applied AFTER reading, still charged for all read items!)
     */
    public List<Map<String, AttributeValue>> queryWithFilter() {
        Map<String, AttributeValue> values = new HashMap<>();
        values.put(":status", attr("PENDING"));
        values.put(":minAmount", attrN("100"));
        
        QueryRequest request = QueryRequest.builder()
            .tableName("Orders")
            .indexName("StatusIndex")
            .keyConditionExpression("status = :status")
            // Filter is applied AFTER reading all PENDING orders
            .filterExpression("amount >= :minAmount")
            .expressionAttributeValues(values)
            .build();
        
        QueryResponse response = client.query(request);
        
        // Cost: RCUs for ALL pending orders (not just filtered results)
        // If filtering reduces results significantly, consider:
        // 1. Adding another GSI with amount as sort key
        // 2. Using sparse index for high-value orders
        return response.items();
    }
    
    /**
     * Performance Tip 4: Parallel queries for better throughput
     */
    public List<Map<String, AttributeValue>> parallelQueries() {
        // Query multiple partitions in parallel
        List<String> statuses = Arrays.asList("PENDING", "PROCESSING", "SHIPPED");
        
        List<Map<String, AttributeValue>> allResults = statuses.parallelStream()
            .flatMap(status -> {
                Map<String, AttributeValue> values = new HashMap<>();
                values.put(":status", attr(status));
                
                QueryRequest request = QueryRequest.builder()
                    .tableName("Orders")
                    .indexName("StatusIndex")
                    .keyConditionExpression("status = :status")
                    .expressionAttributeValues(values)
                    .build();
                
                QueryResponse response = client.query(request);
                return response.items().stream();
            })
            .toList();
        
        return allResults;
    }
    
    /**
     * Performance Anti-Pattern: Using GSI when base table would work
     */
    public void antiPattern() {
        // BAD: Using GSI unnecessarily
        // If you have userId and want to query by userId,
        // and userId is the partition key, use base table!
        
        // Don't do this:
        QueryRequest badRequest = QueryRequest.builder()
            .tableName("Orders")
            .indexName("UserIdIndex") // Unnecessary GSI!
            .keyConditionExpression("userId = :userId")
            .build();
        
        // Do this instead:
        QueryRequest goodRequest = QueryRequest.builder()
            .tableName("Orders")
            .keyConditionExpression("userId = :userId")
            .build();
        
        // Base table query is:
        // • Faster (no GSI propagation delay)
        // • Cheaper (no extra storage)
        // • Strongly consistent (GSI is eventually consistent)
    }
    
    private AttributeValue attr(String value) {
        return AttributeValue.builder().s(value).build();
    }
    
    private AttributeValue attrN(String value) {
        return AttributeValue.builder().n(value).build();
    }
}
```

---

## 5. Capacity Modes and Performance

### Provisioned vs On-Demand Mode

**Comparison:**

```
┌──────────────────────────────────────────────────────────────┐
│         Provisioned vs On-Demand Capacity                     │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  PROVISIONED CAPACITY MODE                                   │
│  ──────────────────────────                                 │
│  You specify read/write capacity units in advance            │
│                                                               │
│  Characteristics:                                            │
│  • Predictable cost                                          │
│  • Manual or auto-scaling                                    │
│  • Best for consistent traffic                               │
│  • Lower cost for steady workloads                           │
│  • Reserved capacity available (up to 76% discount)          │
│  • Throttling if exceeded                                    │
│                                                               │
│  Pricing Example:                                            │
│  • 100 RCUs: $0.013/hour = $9.36/month                       │
│  • 100 WCUs: $0.065/hour = $46.80/month                      │
│  • Total: $56.16/month                                       │
│                                                               │
│  Use when:                                                   │
│  ✅ Predictable traffic patterns                             │
│  ✅ Consistent baseline load                                 │
│  ✅ Cost optimization important                              │
│  ✅ Can forecast capacity needs                              │
│  ✅ Long-term production workloads                           │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ON-DEMAND CAPACITY MODE                                     │
│  ────────────────────────                                   │
│  Pay per request - no capacity planning needed               │
│                                                               │
│  Characteristics:                                            │
│  • Pay only for what you use                                 │
│  • Instant scaling (0 to any scale)                          │
│  • No throttling (scales automatically)                      │
│  • Higher cost per request                                   │
│  • No reserved capacity                                      │
│  • Great for unpredictable traffic                           │
│                                                               │
│  Pricing:                                                    │
│  • $1.25 per million read requests                           │
│  • $1.25 per million write requests                          │
│                                                               │
│  Example Cost (100K req/month each):                         │
│  • Reads: 100K × $1.25/1M = $0.125                           │
│  • Writes: 100K × $1.25/1M = $0.125                          │
│  • Total: $0.25/month                                        │
│                                                               │
│  Use when:                                                   │
│  ✅ Unpredictable traffic                                    │
│  ✅ New application (unknown patterns)                       │
│  ✅ Spiky workloads                                          │
│  ✅ Development/testing                                      │
│  ✅ Serverless applications                                  │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Cost Comparison Example:                                    │
│  ────────────────────────                                   │
│                                                               │
│  Scenario: 100M reads/month, 10M writes/month                │
│                                                               │
│  Provisioned (with auto-scaling):                            │
│  • Average: 39 RCUs + 4 WCUs                                 │
│  • Cost: $10/month                                           │
│                                                               │
│  On-Demand:                                                  │
│  • 100M reads × $1.25/1M = $125                              │
│  • 10M writes × $1.25/1M = $12.50                            │
│  • Cost: $137.50/month                                       │
│                                                               │
│  Winner: Provisioned saves 93%! ✅                           │
│                                                               │
│  Scenario: Sporadic traffic (10K req/day, 2 days/week)       │
│                                                               │
│  Provisioned:                                                │
│  • Must provision for peak                                   │
│  • Pays 24/7 even when idle                                  │
│  • Cost: ~$20/month (underutilized)                          │
│                                                               │
│  On-Demand:                                                  │
│  • Pay only for 2 days/week                                  │
│  • Cost: ~$3/month                                           │
│                                                               │
│  Winner: On-Demand saves 85%! ✅                             │
│                                                               │
│  Rule of Thumb:                                              │
│  • Consistent traffic > 25% utilization → Provisioned        │
│  • Inconsistent traffic < 25% utilization → On-Demand        │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Configuration:**

```java
package com.example.capacity;

import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

/**
 * Capacity Mode Configuration
 */
@Service
public class CapacityModeService {
    
    private final DynamoDbClient client;
    
    public CapacityModeService(DynamoDbClient client) {
        this.client = client;
    }
    
    /**
     * Create table with ON-DEMAND capacity
     */
    public void createOnDemandTable() {
        CreateTableRequest request = CreateTableRequest.builder()
            .tableName("Orders")
            .keySchema(
                KeySchemaElement.builder()
                    .attributeName("orderId")
                    .keyType(KeyType.HASH)
                    .build()
            )
            .attributeDefinitions(
                AttributeDefinition.builder()
                    .attributeName("orderId")
                    .attributeType(ScalarAttributeType.S)
                    .build()
            )
            .billingMode(BillingMode.PAY_PER_REQUEST) // On-Demand
            .build();
        
        client.createTable(request);
    }
    
    /**
     * Create table with PROVISIONED capacity
     */
    public void createProvisionedTable() {
        CreateTableRequest request = CreateTableRequest.builder()
            .tableName("Users")
            .keySchema(
                KeySchemaElement.builder()
                    .attributeName("userId")
                    .keyType(KeyType.HASH)
                    .build()
            )
            .attributeDefinitions(
                AttributeDefinition.builder()
                    .attributeName("userId")
                    .attributeType(ScalarAttributeType.S)
                    .build()
            )
            .billingMode(BillingMode.PROVISIONED)
            .provisionedThroughput(ProvisionedThroughput.builder()
                .readCapacityUnits(100L)  // 100 RCUs
                .writeCapacityUnits(50L)  // 50 WCUs
                .build())
            .build();
        
        client.createTable(request);
    }
    
    /**
     * Switch from On-Demand to Provisioned
     */
    public void switchToProvisioned(String tableName) {
        UpdateTableRequest request = UpdateTableRequest.builder()
            .tableName(tableName)
            .billingMode(BillingMode.PROVISIONED)
            .provisionedThroughput(ProvisionedThroughput.builder()
                .readCapacityUnits(100L)
                .writeCapacityUnits(50L)
                .build())
            .build();
        
        client.updateTable(request);
    }
    
    /**
     * Switch from Provisioned to On-Demand
     */
    public void switchToOnDemand(String tableName) {
        UpdateTableRequest request = UpdateTableRequest.builder()
            .tableName(tableName)
            .billingMode(BillingMode.PAY_PER_REQUEST)
            .build();
        
        // Note: Can only switch once per 24 hours!
        client.updateTable(request);
    }
    
    /**
     * Update provisioned capacity
     */
    public void updateCapacity(String tableName, long readCapacity, long writeCapacity) {
        UpdateTableRequest request = UpdateTableRequest.builder()
            .tableName(tableName)
            .provisionedThroughput(ProvisionedThroughput.builder()
                .readCapacityUnits(readCapacity)
                .writeCapacityUnits(writeCapacity)
                .build())
            .build();
        
        client.updateTable(request);
    }
}
```

### RCU and WCU Calculation

**Understanding Capacity Units:**

```
┌──────────────────────────────────────────────────────────────┐
│         Read Capacity Units (RCU) Calculation                 │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  1 RCU = 1 strongly consistent read per second                │
│       OR 2 eventually consistent reads per second             │
│       for items up to 4KB                                     │
│                                                               │
│  Formula:                                                    │
│  RCU = (Item size / 4KB) × Reads per second × Consistency    │
│                                                               │
│  Consistency factor:                                         │
│  • Strongly consistent: 1                                    │
│  • Eventually consistent: 0.5                                │
│                                                               │
│  Examples:                                                   │
│  ────────                                                    │
│                                                               │
│  Example 1: 100 strongly consistent reads/sec, 2KB items     │
│  RCU = (2KB / 4KB) × 100 × 1 = 0.5 × 100 = 50 RCUs          │
│                                                               │
│  Example 2: 100 eventually consistent reads/sec, 2KB items   │
│  RCU = (2KB / 4KB) × 100 × 0.5 = 0.5 × 100 × 0.5 = 25 RCUs  │
│                                                               │
│  Example 3: 50 strongly consistent reads/sec, 10KB items     │
│  RCU = (10KB / 4KB) × 50 × 1                                 │
│      = 2.5 → round up to 3                                   │
│      = 3 × 50 = 150 RCUs                                     │
│                                                               │
│  Example 4: 200 eventually consistent reads/sec, 1KB items   │
│  RCU = (1KB / 4KB) × 200 × 0.5                               │
│      = 0.25 × 200 × 0.5 = 25 RCUs                            │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Write Capacity Units (WCU) Calculation                      │
│  ────────────────────────────────────────                   │
│                                                               │
│  1 WCU = 1 write per second for items up to 1KB              │
│                                                               │
│  Formula:                                                    │
│  WCU = (Item size / 1KB) × Writes per second                 │
│                                                               │
│  Examples:                                                   │
│  ────────                                                    │
│                                                               │
│  Example 1: 100 writes/sec, 500 bytes items                  │
│  WCU = (0.5KB / 1KB) × 100 = 0.5 → round up to 1            │
│      = 1 × 100 = 100 WCUs                                    │
│                                                               │
│  Example 2: 50 writes/sec, 3KB items                         │
│  WCU = (3KB / 1KB) × 50 = 3 × 50 = 150 WCUs                  │
│                                                               │
│  Example 3: 10 writes/sec, 5.5KB items                       │
│  WCU = (5.5KB / 1KB) × 10                                    │
│      = 5.5 → round up to 6                                   │
│      = 6 × 10 = 60 WCUs                                      │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  GSI Capacity:                                               │
│  • GSI has separate RCU/WCU from base table                  │
│  • Writes to base table also consume GSI WCUs                │
│  • Must provision GSI capacity separately                    │
│                                                               │
│  Transaction Capacity:                                       │
│  • TransactWriteItems: 2× WCUs                               │
│  • TransactGetItems: 2× RCUs                                 │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Calculator Implementation:**

```java
package com.example.capacity;

import org.springframework.stereotype.Service;

/**
 * Capacity Unit Calculator
 */
@Service
public class CapacityCalculator {
    
    /**
     * Calculate RCUs needed
     */
    public long calculateRCU(int itemSizeKB, int readsPerSecond, boolean stronglyConsistent) {
        // Round up item size to nearest 4KB block
        int blocks = (int) Math.ceil(itemSizeKB / 4.0);
        
        // Calculate RCUs
        long rcus = (long) blocks * readsPerSecond;
        
        // Eventually consistent reads cost half
        if (!stronglyConsistent) {
            rcus = (long) Math.ceil(rcus / 2.0);
        }
        
        return rcus;
    }
    
    /**
     * Calculate WCUs needed
     */
    public long calculateWCU(int itemSizeKB, int writesPerSecond) {
        // Round up to nearest 1KB block
        int blocks = itemSizeKB; // Each KB is 1 block
        
        return (long) blocks * writesPerSecond;
    }
    
    /**
     * Real-world example calculations
     */
    public void exampleCalculations() {
        // E-commerce orders: 2KB items, 100 reads/sec, eventually consistent
        long ordersRCU = calculateRCU(2, 100, false);
        System.out.println("Orders RCU: " + ordersRCU); // 25 RCUs
        
        // User profiles: 5KB items, 50 reads/sec, strongly consistent
        long usersRCU = calculateRCU(5, 50, true);
        System.out.println("Users RCU: " + usersRCU); // 100 RCUs
        
        // Order writes: 3KB items, 20 writes/sec
        long ordersWCU = calculateWCU(3, 20);
        System.out.println("Orders WCU: " + ordersWCU); // 60 WCUs
        
        // Session writes: 1KB items, 100 writes/sec
        long sessionsWCU = calculateWCU(1, 100);
        System.out.println("Sessions WCU: " + sessionsWCU); // 100 WCUs
    }
    
    /**
     * Calculate monthly cost (provisioned mode)
     */
    public double calculateMonthlyCost(long rcus, long wcus) {
        // Pricing: $0.00013 per RCU-hour, $0.00065 per WCU-hour
        double reuCostPerHour = 0.00013;
        double wcuCostPerHour = 0.00065;
        int hoursPerMonth = 730;
        
        double readCost = rcus * rcuCostPerHour * hoursPerMonth;
        double writeCost = wcus * wcuCostPerHour * hoursPerMonth;
        
        return readCost + writeCost;
    }
    
    /**
     * Calculate monthly cost (on-demand mode)
     */
    public double calculateOnDemandCost(long totalReads, long totalWrites) {
        // Pricing: $1.25 per million requests
        double readCostPerMillion = 1.25;
        double writeCostPerMillion = 1.25;
        
        double readCost = (totalReads / 1_000_000.0) * readCostPerMillion;
        double writeCost = (totalWrites / 1_000_000.0) * writeCostPerMillion;
        
        return readCost + writeCost;
    }
    
    /**
     * Compare provisioned vs on-demand cost
     */
    public void compareCosts() {
        // Scenario: 100 RCUs, 50 WCUs provisioned
        long rcus = 100;
        long wcus = 50;
        double provisionedCost = calculateMonthlyCost(rcus, wcus);
        
        // Same workload on-demand
        // 100 RCUs = 100 reads/sec = 260M reads/month
        // 50 WCUs = 50 writes/sec = 130M writes/month
        long totalReads = 260_000_000L;
        long totalWrites = 130_000_000L;
        double onDemandCost = calculateOnDemandCost(totalReads, totalWrites);
        
        System.out.println("Provisioned cost: $" + String.format("%.2f", provisionedCost));
        System.out.println("On-Demand cost: $" + String.format("%.2f", onDemandCost));
        
        if (provisionedCost < onDemandCost) {
            double savings = ((onDemandCost - provisionedCost) / onDemandCost) * 100;
            System.out.println("Provisioned saves " + String.format("%.1f", savings) + "%");
        } else {
            double savings = ((provisionedCost - onDemandCost) / provisionedCost) * 100;
            System.out.println("On-Demand saves " + String.format("%.1f", savings) + "%");
        }
    }
}
```

Let me continue with Auto-scaling, Advanced Features, and Best Practices to complete Part 2...

### Auto-Scaling Configuration

**Auto-Scaling Setup:**

```java
package com.example.capacity;

import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.applicationautoscaling.ApplicationAutoScalingClient;
import software.amazon.awssdk.services.applicationautoscaling.model.*;

/**
 * DynamoDB Auto-Scaling Configuration
 */
@Service
public class AutoScalingService {
    
    private final ApplicationAutoScalingClient autoScalingClient;
    
    public AutoScalingService(ApplicationAutoScalingClient autoScalingClient) {
        this.autoScalingClient = autoScalingClient;
    }
    
    /**
     * Register table for auto-scaling
     */
    public void setupAutoScaling(String tableName) {
        // Register read capacity
        RegisterScalableTargetRequest readTargetRequest = RegisterScalableTargetRequest.builder()
            .serviceNamespace(ServiceNamespace.DYNAMODB)
            .resourceId("table/" + tableName)
            .scalableDimension(ScalableDimension.DYNAMODB_TABLE_READ_CAPACITY_UNITS)
            .minCapacity(5)    // Minimum 5 RCUs
            .maxCapacity(1000) // Maximum 1000 RCUs
            .build();
        
        autoScalingClient.registerScalableTarget(readTargetRequest);
        
        // Register write capacity
        RegisterScalableTargetRequest writeTargetRequest = RegisterScalableTargetRequest.builder()
            .serviceNamespace(ServiceNamespace.DYNAMODB)
            .resourceId("table/" + tableName)
            .scalableDimension(ScalableDimension.DYNAMODB_TABLE_WRITE_CAPACITY_UNITS)
            .minCapacity(5)    // Minimum 5 WCUs
            .maxCapacity(500)  // Maximum 500 WCUs
            .build();
        
        autoScalingClient.registerScalableTarget(writeTargetRequest);
        
        // Create scaling policy for reads (target 70% utilization)
        PutScalingPolicyRequest readPolicyRequest = PutScalingPolicyRequest.builder()
            .serviceNamespace(ServiceNamespace.DYNAMODB)
            .resourceId("table/" + tableName)
            .scalableDimension(ScalableDimension.DYNAMODB_TABLE_READ_CAPACITY_UNITS)
            .policyName(tableName + "-read-scaling-policy")
            .policyType(PolicyType.TARGET_TRACKING_SCALING)
            .targetTrackingScalingPolicyConfiguration(
                TargetTrackingScalingPolicyConfiguration.builder()
                    .targetValue(70.0) // 70% utilization target
                    .predefinedMetricSpecification(
                        PredefinedMetricSpecification.builder()
                            .predefinedMetricType(MetricType.DYNAMO_DB_READ_CAPACITY_UTILIZATION)
                            .build())
                    .scaleInCooldown(60)  // Wait 60s before scaling in
                    .scaleOutCooldown(60) // Wait 60s before scaling out
                    .build())
            .build();
        
        autoScalingClient.putScalingPolicy(readPolicyRequest);
        
        // Create scaling policy for writes
        PutScalingPolicyRequest writePolicyRequest = PutScalingPolicyRequest.builder()
            .serviceNamespace(ServiceNamespace.DYNAMODB)
            .resourceId("table/" + tableName)
            .scalableDimension(ScalableDimension.DYNAMODB_TABLE_WRITE_CAPACITY_UNITS)
            .policyName(tableName + "-write-scaling-policy")
            .policyType(PolicyType.TARGET_TRACKING_SCALING)
            .targetTrackingScalingPolicyConfiguration(
                TargetTrackingPolicyConfiguration.builder()
                    .targetValue(70.0)
                    .predefinedMetricSpecification(
                        PredefinedMetricSpecification.builder()
                            .predefinedMetricType(MetricType.DYNAMO_DB_WRITE_CAPACITY_UTILIZATION)
                            .build())
                    .scaleInCooldown(60)
                    .scaleOutCooldown(60)
                    .build())
            .build();
        
        autoScalingClient.putScalingPolicy(writePolicyRequest);
    }
}
```

### Throttling and Burst Capacity

**Understanding Throttling:**

```
┌──────────────────────────────────────────────────────────────┐
│         Throttling and Burst Capacity                         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Throttling occurs when requests exceed provisioned capacity  │
│  Error: ProvisionedThroughputExceededException               │
│                                                               │
│  Burst Capacity:                                             │
│  • DynamoDB reserves unused capacity for bursts              │
│  • Up to 5 minutes of unused capacity (max 300 seconds)      │
│  • Automatic - no configuration needed                       │
│                                                               │
│  Example:                                                    │
│  Table: 100 RCUs provisioned                                 │
│  Usage: 50 RCUs average (50% utilization)                    │
│  Burst available: 50 RCUs × 300s = 15,000 burst units        │
│  Can handle: 150 RCUs for 100 seconds                        │
│              or 200 RCUs for 75 seconds                      │
│                                                               │
│  Adaptive Capacity:                                          │
│  • Automatically redistributes capacity                      │
│  • Handles hot partitions better                             │
│  • No configuration needed                                   │
│  • Enabled by default                                        │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Handling Throttling:**

```java
package com.example.capacity;

import org.springframework.stereotype.Service;
import software.amazon.awssdk.core.retry.RetryPolicy;
import software.amazon.awssdk.core.retry.backoff.BackoffStrategy;
import software.amazon.awssdk.core.retry.conditions.RetryCondition;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.time.Duration;
import java.util.*;

/**
 * Handling Throttling and Retries
 */
@Service
public class ThrottlingHandlingService {
    
    private final DynamoDbClient client;
    
    public ThrottlingHandlingService() {
        // Configure client with retry policy
        this.client = DynamoDbClient.builder()
            .overrideConfiguration(config -> config
                .retryPolicy(RetryPolicy.builder()
                    .numRetries(10) // Max 10 retries
                    .retryCondition(RetryCondition.defaultRetryCondition())
                    .backoffStrategy(BackoffStrategy.defaultThrottlingStrategy())
                    .build()))
            .build();
    }
    
    /**
     * Batch write with throttling protection
     */
    public void batchWriteWithRetry(List<Map<String, AttributeValue>> items) {
        List<WriteRequest> writeRequests = items.stream()
            .map(item -> WriteRequest.builder()
                .putRequest(PutRequest.builder().item(item).build())
                .build())
            .toList();
        
        Map<String, List<WriteRequest>> requestItems = new HashMap<>();
        requestItems.put("Orders", writeRequests);
        
        // Process with automatic retries for unprocessed items
        processWithRetry(requestItems);
    }
    
    private void processWithRetry(Map<String, List<WriteRequest>> requestItems) {
        Map<String, List<WriteRequest>> unprocessed = requestItems;
        int retryCount = 0;
        int maxRetries = 5;
        
        while (!unprocessed.isEmpty() && retryCount < maxRetries) {
            BatchWriteItemRequest request = BatchWriteItemRequest.builder()
                .requestItems(unprocessed)
                .build();
            
            try {
                BatchWriteItemResponse response = client.batchWriteItem(request);
                unprocessed = response.unprocessedItems();
                
                if (!unprocessed.isEmpty()) {
                    // Exponential backoff
                    long waitTime = (long) Math.pow(2, retryCount) * 100;
                    Thread.sleep(waitTime);
                    retryCount++;
                }
                
            } catch (ProvisionedThroughputExceededException e) {
                // Throttled - wait and retry
                retryCount++;
                try {
                    Thread.sleep((long) Math.pow(2, retryCount) * 100);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
}
```

### Cost Optimization Strategies

**Optimization Techniques:**

```java
package com.example.optimization;

import org.springframework.stereotype.Service;

/**
 * DynamoDB Cost Optimization Strategies
 */
@Service
public class CostOptimizationService {
    
    /**
     * Strategy 1: Right-size capacity
     */
    public void strategy1_RightSizeCapacity() {
        /*
        • Monitor CloudWatch metrics
        • Set capacity to 80% of peak usage
        • Use auto-scaling for fluctuations
        • Review monthly and adjust
        
        Example:
        Peak usage: 100 RCUs
        Provision: 80 RCUs + auto-scaling to 120 RCUs
        Savings: 20% vs provisioning for peak
        */
    }
    
    /**
     * Strategy 2: Use reserved capacity (53-76% discount)
     */
    public void strategy2_ReservedCapacity() {
        /*
        For predictable workloads:
        • 1-year commitment: 53% discount
        • 3-year commitment: 76% discount
        
        Example:
        100 RCUs on-demand: $95/month
        100 RCUs reserved (1-year): $45/month
        Savings: $600/year
        */
    }
    
    /**
     * Strategy 3: Use on-demand for low traffic tables
     */
    public void strategy3_OnDemandForLowTraffic() {
        /*
        If table utilization < 25%:
        • Switch to on-demand
        • Pay only for actual requests
        
        Example:
        Provisioned 10 RCUs (always on): $9/month
        On-demand 500K requests/month: $0.63/month
        Savings: 93%
        */
    }
    
    /**
     * Strategy 4: Optimize item size
     */
    public void strategy4_OptimizeItemSize() {
        /*
        Smaller items = lower RCU/WCU consumption
        
        Techniques:
        • Remove unused attributes
        • Compress large text fields
        • Use short attribute names
        • Store large blobs in S3
        
        Example:
        Before: 5KB item, 100 writes/sec = 500 WCUs ($292/month)
        After: 2KB item, 100 writes/sec = 200 WCUs ($117/month)
        Savings: 60%
        */
    }
    
    /**
     * Strategy 5: Use eventually consistent reads
     */
    public void strategy5_EventuallyConsistentReads() {
        /*
        Eventually consistent = 50% cheaper
        
        Example:
        100 RCUs strongly consistent: $95/month
        50 RCUs eventually consistent: $47/month
        Savings: 50%
        
        Use eventually consistent when:
        • Reading cached data
        • Analytics queries
        • Non-critical reads
        */
    }
    
    /**
     * Strategy 6: Optimize GSI usage
     */
    public void strategy6_OptimizeGSIs() {
        /*
        Each GSI costs extra:
        • Storage for projected attributes
        • Write capacity for all writes
        • Read capacity for queries
        
        Optimization:
        • Use KEYS_ONLY projection
        • Consolidate GSIs (index overloading)
        • Delete unused GSIs
        • Use sparse indexes
        
        Example:
        5 GSIs with ALL projection: 5× storage cost
        3 GSIs with KEYS_ONLY: 0.5× storage cost
        Savings: 90% on GSI storage
        */
    }
    
    /**
     * Strategy 7: Batch operations
     */
    public void strategy7_BatchOperations() {
        /*
        Batch operations more efficient:
        • BatchGetItem: Up to 100 items
        • BatchWriteItem: Up to 25 items
        • Reduces overhead
        
        Example:
        100 individual PutItem: 100 requests
        BatchWriteItem (4 batches): 4 requests
        Throughput: 25× better
        */
    }
    
    /**
     * Strategy 8: Enable TTL for temporary data
     */
    public void strategy8_UseTTL() {
        /*
        TTL deletes items automatically (no WCU cost!)
        
        Use cases:
        • Session data (expire after 24 hours)
        • Temporary tokens (expire after 1 hour)
        • Log data (expire after 30 days)
        
        Savings: Avoid paying for deletion WCUs
        */
    }
}
```

---

## 6. Advanced Features

### DynamoDB Streams

**Streams for Change Data Capture:**

```java
package com.example.advanced;

import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;
import software.amazon.awssdk.services.dynamodbstreams.DynamoDbStreamsClient;
import software.amazon.awssdk.services.dynamodbstreams.model.*;
import software.amazon.awssdk.services.dynamodbstreams.model.Record;

import java.util.*;

/**
 * DynamoDB Streams for Change Data Capture
 * 
 * Use cases:
 * • Real-time analytics
 * • Data replication
 * • Audit logs
 * • Trigger Lambda functions
 * • Cross-region replication
 */
@Service
public class DynamoDBStreamsService {
    
    private final DynamoDbClient dynamoClient;
    private final DynamoDbStreamsClient streamsClient;
    
    public DynamoDBStreamsService(DynamoDbClient dynamoClient, 
                                  DynamoDbStreamsClient streamsClient) {
        this.dynamoClient = dynamoClient;
        this.streamsClient = streamsClient;
    }
    
    /**
     * Enable streams on table
     */
    public void enableStreams(String tableName) {
        UpdateTableRequest request = UpdateTableRequest.builder()
            .tableName(tableName)
            .streamSpecification(StreamSpecification.builder()
                .streamEnabled(true)
                .streamViewType(StreamViewType.NEW_AND_OLD_IMAGES) // NEW, OLD, NEW_AND_OLD, KEYS_ONLY
                .build())
            .build();
        
        dynamoClient.updateTable(request);
    }
    
    /**
     * Process stream records
     */
    public void processStreamRecords(String streamArn) {
        // Get shards
        DescribeStreamRequest describeRequest = DescribeStreamRequest.builder()
            .streamArn(streamArn)
            .build();
        
        DescribeStreamResponse describeResponse = streamsClient.describeStream(describeRequest);
        
        for (Shard shard : describeResponse.streamDescription().shards()) {
            // Get shard iterator
            GetShardIteratorRequest iteratorRequest = GetShardIteratorRequest.builder()
                .streamArn(streamArn)
                .shardId(shard.shardId())
                .shardIteratorType(ShardIteratorType.TRIM_HORIZON) // Start from beginning
                .build();
            
            GetShardIteratorResponse iteratorResponse = streamsClient.getShardIterator(iteratorRequest);
            String shardIterator = iteratorResponse.shardIterator();
            
            // Read records
            while (shardIterator != null) {
                GetRecordsRequest recordsRequest = GetRecordsRequest.builder()
                    .shardIterator(shardIterator)
                    .build();
                
                GetRecordsResponse recordsResponse = streamsClient.getRecords(recordsRequest);
                
                for (Record record : recordsResponse.records()) {
                    processRecord(record);
                }
                
                shardIterator = recordsResponse.nextShardIterator();
                
                // Rate limiting
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    break;
                }
            }
        }
    }
    
    private void processRecord(Record record) {
        String eventName = record.eventName().toString(); // INSERT, MODIFY, REMOVE
        
        switch (eventName) {
            case "INSERT":
                handleInsert(record.dynamodb().newImage());
                break;
            case "MODIFY":
                handleModify(record.dynamodb().oldImage(), record.dynamodb().newImage());
                break;
            case "REMOVE":
                handleRemove(record.dynamodb().keys());
                break;
        }
    }
    
    private void handleInsert(Map<String, software.amazon.awssdk.services.dynamodbstreams.model.AttributeValue> newImage) {
        // Process new item
        System.out.println("New item inserted: " + newImage);
    }
    
    private void handleModify(Map<String, software.amazon.awssdk.services.dynamodbstreams.model.AttributeValue> oldImage,
                              Map<String, software.amazon.awssdk.services.dynamodbstreams.model.AttributeValue> newImage) {
        // Process updated item
        System.out.println("Item updated from: " + oldImage + " to: " + newImage);
    }
    
    private void handleRemove(Map<String, software.amazon.awssdk.services.dynamodbstreams.model.AttributeValue> keys) {
        // Process deleted item
        System.out.println("Item deleted: " + keys);
    }
}
```

### Time To Live (TTL)

**Auto-Delete Expired Items:**

```java
package com.example.advanced;

import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.time.Instant;
import java.util.*;

/**
 * Time To Live (TTL) for automatic item deletion
 * 
 * Benefits:
 * • Free - no WCU cost for deletions
 * • Automatic cleanup
 * • Reduces storage costs
 * 
 * Use cases:
 * • Session data
 * • Temporary tokens
 * • Log data
 * • Cache entries
 */
@Service
public class TTLService {
    
    private final DynamoDbClient client;
    
    public TTLService(DynamoDbClient client) {
        this.client = client;
    }
    
    /**
     * Enable TTL on table
     */
    public void enableTTL(String tableName, String ttlAttributeName) {
        UpdateTimeToLiveRequest request = UpdateTimeToLiveRequest.builder()
            .tableName(tableName)
            .timeToLiveSpecification(TimeToLiveSpecification.builder()
                .enabled(true)
                .attributeName(ttlAttributeName) // e.g., "expirationTime"
                .build())
            .build();
        
        client.updateTimeToLive(request);
    }
    
    /**
     * Save item with TTL (session example)
     */
    public void saveSessionWithTTL(String sessionId, String userId) {
        // Expire after 24 hours
        long ttl = Instant.now().plusSeconds(86400).getEpochSecond();
        
        Map<String, AttributeValue> item = new HashMap<>();
        item.put("sessionId", attr(sessionId));
        item.put("userId", attr(userId));
        item.put("createdAt", attrN(String.valueOf(Instant.now().getEpochSecond())));
        item.put("expirationTime", attrN(String.valueOf(ttl))); // TTL attribute
        
        PutItemRequest request = PutItemRequest.builder()
            .tableName("Sessions")
            .item(item)
            .build();
        
        client.putItem(request);
    }
    
    /**
     * Save temporary token with TTL
     */
    public void saveTokenWithTTL(String token, String userId) {
        // Expire after 1 hour
        long ttl = Instant.now().plusSeconds(3600).getEpochSecond();
        
        Map<String, AttributeValue> item = new HashMap<>();
        item.put("token", attr(token));
        item.put("userId", attr(userId));
        item.put("expirationTime", attrN(String.valueOf(ttl)));
        
        client.putItem(PutItemRequest.builder()
            .tableName("Tokens")
            .item(item)
            .build());
    }
    
    /**
     * Save log entry with 30-day retention
     */
    public void saveLogWithTTL(String logId, String message) {
        // Expire after 30 days
        long ttl = Instant.now().plusSeconds(2592000).getEpochSecond();
        
        Map<String, AttributeValue> item = new HashMap<>();
        item.put("logId", attr(logId));
        item.put("message", attr(message));
        item.put("timestamp", attrN(String.valueOf(Instant.now().getEpochSecond())));
        item.put("expirationTime", attrN(String.valueOf(ttl)));
        
        client.putItem(PutItemRequest.builder()
            .tableName("Logs")
            .item(item)
            .build());
    }
    
    private AttributeValue attr(String value) {
        return AttributeValue.builder().s(value).build();
    }
    
    private AttributeValue attrN(String value) {
        return AttributeValue.builder().n(value).build();
    }
}
```

### Transactions

**ACID Transactions:**

```java
package com.example.advanced;

import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.math.BigDecimal;
import java.util.*;

/**
 * DynamoDB Transactions (ACID)
 * 
 * Features:
 * • All-or-nothing operations
 * • Up to 100 items per transaction
 * • Max 4MB total size
 * • 2× WCU/RCU cost
 * 
 * Use cases:
 * • Money transfers
 * • Inventory management
 * • Multi-item updates
 * • Referential integrity
 */
@Service
public class TransactionService {
    
    private final DynamoDbClient client;
    
    public TransactionService(DynamoDbClient client) {
        this.client = client;
    }
    
    /**
     * Transfer money between accounts (atomic)
     */
    public void transferMoney(String fromAccountId, String toAccountId, BigDecimal amount) {
        List<TransactWriteItem> transactItems = new ArrayList<>();
        
        // Deduct from source account
        transactItems.add(TransactWriteItem.builder()
            .update(Update.builder()
                .tableName("Accounts")
                .key(Map.of("accountId", attr(fromAccountId)))
                .updateExpression("SET balance = balance - :amount")
                .conditionExpression("balance >= :amount") // Ensure sufficient funds
                .expressionAttributeValues(Map.of(":amount", attrN(amount)))
                .build())
            .build());
        
        // Add to destination account
        transactItems.add(TransactWriteItem.builder()
            .update(Update.builder()
                .tableName("Accounts")
                .key(Map.of("accountId", attr(toAccountId)))
                .updateExpression("SET balance = balance + :amount")
                .expressionAttributeValues(Map.of(":amount", attrN(amount)))
                .build())
            .build());
        
        // Record transaction
        transactItems.add(TransactWriteItem.builder()
            .put(Put.builder()
                .tableName("Transactions")
                .item(Map.of(
                    "transactionId", attr(UUID.randomUUID().toString()),
                    "fromAccount", attr(fromAccountId),
                    "toAccount", attr(toAccountId),
                    "amount", attrN(amount),
                    "timestamp", attrN(String.valueOf(System.currentTimeMillis()))
                ))
                .build())
            .build());
        
        // Execute transaction (all or nothing!)
        TransactWriteItemsRequest request = TransactWriteItemsRequest.builder()
            .transactItems(transactItems)
            .build();
        
        try {
            client.transactWriteItems(request);
        } catch (TransactionCanceledException e) {
            // Transaction failed (e.g., insufficient funds)
            System.err.println("Transaction cancelled: " + e.getMessage());
        }
    }
    
    /**
     * Update inventory atomically
     */
    public void processOrder(String orderId, String productId, int quantity) {
        List<TransactWriteItem> transactItems = new ArrayList<>();
        
        // Create order
        transactItems.add(TransactWriteItem.builder()
            .put(Put.builder()
                .tableName("Orders")
                .item(Map.of(
                    "orderId", attr(orderId),
                    "productId", attr(productId),
                    "quantity", attrN(String.valueOf(quantity)),
                    "status", attr("PENDING")
                ))
                .conditionExpression("attribute_not_exists(orderId)") // Prevent duplicates
                .build())
            .build());
        
        // Reduce inventory
        transactItems.add(TransactWriteItem.builder()
            .update(Update.builder()
                .tableName("Products")
                .key(Map.of("productId", attr(productId)))
                .updateExpression("SET stock = stock - :quantity")
                .conditionExpression("stock >= :quantity") // Ensure stock available
                .expressionAttributeValues(Map.of(":quantity", attrN(String.valueOf(quantity))))
                .build())
            .build());
        
        // Execute
        TransactWriteItemsRequest request = TransactWriteItemsRequest.builder()
            .transactItems(transactItems)
            .build();
        
        client.transactWriteItems(request);
    }
    
    /**
     * Read multiple items atomically
     */
    public Map<String, Map<String, AttributeValue>> atomicRead(String userId, String orderId) {
        List<TransactGetItem> transactItems = new ArrayList<>();
        
        // Get user
        transactItems.add(TransactGetItem.builder()
            .get(Get.builder()
                .tableName("Users")
                .key(Map.of("userId", attr(userId)))
                .build())
            .build());
        
        // Get order
        transactItems.add(TransactGetItem.builder()
            .get(Get.builder()
                .tableName("Orders")
                .key(Map.of("orderId", attr(orderId)))
                .build())
            .build());
        
        // Execute
        TransactGetItemsRequest request = TransactGetItemsRequest.builder()
            .transactItems(transactItems)
            .build();
        
        TransactGetItemsResponse response = client.transactGetItems(request);
        
        Map<String, Map<String, AttributeValue>> results = new HashMap<>();
        results.put("user", response.responses().get(0).item());
        results.put("order", response.responses().get(1).item());
        
        return results;
    }
    
    private AttributeValue attr(String value) {
        return AttributeValue.builder().s(value).build();
    }
    
    private AttributeValue attrN(BigDecimal value) {
        return AttributeValue.builder().n(value.toString()).build();
    }
    
    private AttributeValue attrN(String value) {
        return AttributeValue.builder().n(value).build();
    }
}
```

Due to the extensive content, let me now finalize Part 2 with Best Practices section and move it to outputs...

---

## 7. Best Practices and Anti-Patterns

### Hot Partition Problem and Solutions

**Understanding Hot Partitions:**

```
┌──────────────────────────────────────────────────────────────┐
│         Hot Partition Problem                                 │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Problem:                                                    │
│  One partition receives disproportionate traffic             │
│  → That partition gets throttled                             │
│  → Even though table has plenty of capacity!                 │
│                                                               │
│  Example (BAD):                                              │
│  ───────────────                                            │
│  Table: 1000 WCUs provisioned                                │
│  Partitions: 10 partitions (100 WCUs each)                   │
│                                                               │
│  ┌─────────┬─────────┬─────────┬─────────┐                  │
│  │Part 1   │ Part 2  │ Part 3  │ Part 10 │                  │
│  │ 5 WCUs  │ 5 WCUs  │ 5 WCUs  │ 900 WCUs│ ← HOT!          │
│  └─────────┴─────────┴─────────┴─────────┘                  │
│                                                               │
│  Partition 10 throttled at 100 WCUs (max per partition)      │
│  Even though table total is 1000 WCUs!                       │
│                                                               │
│  Common Causes:                                              │
│  ❌ Low cardinality partition key (e.g., "status")           │
│  ❌ Celebrity/popular item accessed frequently               │
│  ❌ Date as partition key (all writes go to today)           │
│  ❌ Sequential IDs without sharding                          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Solutions:**

```java
package com.example.bestpractices;

import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.time.LocalDate;
import java.util.*;

/**
 * Solutions for Hot Partition Problem
 */
@Service
public class HotPartitionSolutions {
    
    private final DynamoDbClient client;
    
    public HotPartitionSolutions(DynamoDbClient client) {
        this.client = client;
    }
    
    /**
     * Solution 1: Write Sharding
     * Add random suffix to distribute writes across partitions
     */
    public void solution1_WriteSharding(Order order) {
        // Bad: All today's orders go to same partition
        // PK: orderDate (e.g., "2024-12-08")
        
        // Good: Distribute across 10 partitions
        int shardId = Math.abs(order.getOrderId().hashCode() % 10);
        String shardedKey = order.getOrderDate() + "#" + shardId;
        
        Map<String, AttributeValue> item = new HashMap<>();
        item.put("orderDateShard", attr(shardedKey)); // PK with shard
        item.put("orderId", attr(order.getOrderId()));
        item.put("amount", attrN(order.getAmount()));
        
        client.putItem(PutItemRequest.builder()
            .tableName("Orders")
            .item(item)
            .build());
        
        // To query all orders for a date, query all 10 shards:
        // Query shard 0: PK="2024-12-08#0"
        // Query shard 1: PK="2024-12-08#1"
        // ... merge results
    }
    
    /**
     * Solution 2: Use High-Cardinality Partition Key
     */
    public void solution2_HighCardinalityKey() {
        // Bad: status as partition key (only 3 values: PENDING, PROCESSING, COMPLETED)
        // PK: status ❌
        
        // Good: userId as partition key (millions of unique values)
        // PK: userId ✅
        // Add GSI for status queries: GSI PK=status
    }
    
    /**
     * Solution 3: Distribute Popular Items
     */
    public void solution3_DistributePopularItems(String productId) {
        // For celebrity/popular items that get lots of reads
        // Replicate item across multiple partition keys
        
        int replicaCount = 10;
        int replicaId = new Random().nextInt(replicaCount);
        String shardedProductId = productId + "#replica" + replicaId;
        
        // Write to all replicas (or use asynchronous replication)
        // Read from random replica
        Map<String, AttributeValue> key = new HashMap<>();
        key.put("productId", attr(shardedProductId));
        
        GetItemRequest request = GetItemRequest.builder()
            .tableName("Products")
            .key(key)
            .build();
        
        client.getItem(request);
    }
    
    /**
     * Solution 4: Use Caching (DAX or ElastiCache)
     */
    public void solution4_UseCaching() {
        /*
        For read-heavy hot partitions:
        • Use DynamoDB Accelerator (DAX)
        • Or ElastiCache (Redis/Memcached)
        • Reduces load on hot partitions
        
        Example:
        Popular product accessed 1000 times/sec
        Without cache: 1000 reads hit same partition
        With DAX: 1 read from DynamoDB, 999 from cache
        */
    }
    
    /**
     * Solution 5: Adaptive Capacity
     */
    public void solution5_AdaptiveCapacity() {
        /*
        DynamoDB Adaptive Capacity (automatic):
        • Detects hot partitions
        • Temporarily boosts capacity
        • No configuration needed
        
        But: Not a complete solution
        Still need good partition key design!
        */
    }
    
    private AttributeValue attr(String value) {
        return AttributeValue.builder().s(value).build();
    }
    
    private AttributeValue attrN(java.math.BigDecimal value) {
        return AttributeValue.builder().n(value.toString()).build();
    }
}
```

### Query vs Scan Best Practices

**Rules and Guidelines:**

```java
package com.example.bestpractices;

import org.springframework.stereotype.Component;

/**
 * Query vs Scan Best Practices
 */
@Component
public class QueryVsScanBestPractices {
    
    /**
     * RULE 1: Never use Scan in production application code
     */
    public void rule1_NeverScanInProduction() {
        /*
        ❌ BAD: Scan to find pending orders
        Scan(FilterExpression: status="PENDING")
        • Reads entire table
        • Expensive
        • Slow
        • Doesn't scale
        
        ✅ GOOD: Query GSI
        Query(StatusIndex, PK="PENDING")
        • Reads only pending orders
        • Fast
        • Scales well
        
        If you're using Scan, your table design is wrong!
        Fix: Add GSI for that query pattern
        */
    }
    
    /**
     * RULE 2: Use Scan only for specific cases
     */
    public void rule2_WhenScanIsOK() {
        /*
        Acceptable Scan use cases:
        ✅ One-time data export
        ✅ Analytics (off-peak hours)
        ✅ Table has < 1000 items
        ✅ Admin operations (not user-facing)
        ✅ Parallel scan for bulk processing
        
        ❌ Never for:
        • User-facing queries
        • Real-time operations
        • Frequent operations
        • Large tables
        */
    }
    
    /**
     * RULE 3: Always use Query with primary key or GSI
     */
    public void rule3_AlwaysUseQuery() {
        /*
        Query requirements:
        • Must specify partition key
        • Optional: sort key condition
        • Uses index (base table or GSI)
        
        Performance:
        • Fast: O(log N + M) where M = results
        • Scalable: Only reads matching items
        • Cost-effective: Pay for what you need
        */
    }
    
    /**
     * RULE 4: Design for Query, not Scan
     */
    public void rule4_DesignForQuery() {
        /*
        Access Pattern First Approach:
        1. List all query patterns
        2. Design primary key for main pattern
        3. Add GSIs for other patterns
        4. Result: All queries use Query, never Scan
        
        Example:
        Pattern: "Get pending orders"
        Solution: GSI with PK=status
        Query: Query(StatusIndex, PK="PENDING")
        */
    }
}
```

### Avoiding 400KB Item Size Limit

**Best Practices:**

```java
package com.example.bestpractices;

import org.springframework.stereotype.Service;

/**
 * Item Size Optimization
 */
@Service
public class ItemSizeOptimization {
    
    /**
     * Guideline 1: Store large attributes in S3
     */
    public void guideline1_UseCES3ForLargeData() {
        /*
        DynamoDB Limit: 400KB per item
        
        For large data:
        ✅ Store in S3
        ✅ Store S3 URL in DynamoDB
        
        Example: Product with images
        DynamoDB item:
        {
          "productId": "prod-123",
          "name": "Widget",
          "imageUrl": "s3://bucket/prod-123/image.jpg",  ← S3
          "manualUrl": "s3://bucket/prod-123/manual.pdf" ← S3
        }
        
        Benefits:
        • No 400KB limit
        • Lower DynamoDB costs
        • Better performance
        */
    }
    
    /**
     * Guideline 2: Use short attribute names
     */
    public void guideline2_ShortAttributeNames() {
        /*
        Attribute names count toward 400KB limit!
        
        ❌ Bad:
        {
          "orderIdentificationNumber": "123",
          "customerFullNameWithTitle": "Dr. John Smith",
          "productDescriptionDetailedVersion": "..."
        }
        
        ✅ Good:
        {
          "orderId": "123",
          "custName": "Dr. John Smith",
          "prodDesc": "..."
        }
        
        Savings: 30-50% size reduction!
        */
    }
    
    /**
     * Guideline 3: Compress large text fields
     */
    public void guideline3_CompressText() {
        /*
        For large text (descriptions, content):
        • Compress with GZIP
        • Store as binary
        • Decompress when reading
        
        Example:
        Original: 200KB text
        Compressed: 50KB binary
        Savings: 75%
        */
    }
    
    /**
     * Guideline 4: Split large items
     */
    public void guideline4_SplitLargeItems() {
        /*
        If item > 400KB, split into multiple items
        
        Example: Order with 100 line items
        
        Instead of:
        Order item (450KB) ❌
        
        Do:
        Order item (50KB) +
        OrderItems-1 (100KB) +
        OrderItems-2 (100KB) +
        OrderItems-3 (100KB)
        
        Use composite key:
        PK: orderId
        SK: "ORDER" (main item)
        SK: "ITEMS#1" (batch 1)
        SK: "ITEMS#2" (batch 2)
        */
    }
    
    /**
     * Guideline 5: Remove unused attributes
     */
    public void guideline5_RemoveUnusedAttributes() {
        /*
        Common culprits:
        • Debug information
        • Temporary flags
        • Duplicate data
        • Empty arrays/objects
        
        Clean up:
        • Regular audits
        • Remove before saving
        • Use sparse attributes
        */
    }
}
```

### Proper Partition Key Selection

**Selection Criteria:**

```java
package com.example.bestpractices;

import org.springframework.stereotype.Component;

/**
 * Partition Key Selection Best Practices
 */
@Component
public class PartitionKeySelection {
    
    /**
     * Criterion 1: High Cardinality
     */
    public void criterion1_HighCardinality() {
        /*
        Good partition keys (high cardinality):
        ✅ userId (millions of unique values)
        ✅ orderId (unique per order)
        ✅ deviceId (unique per device)
        ✅ email (unique per user)
        ✅ UUID (infinite cardinality)
        
        Bad partition keys (low cardinality):
        ❌ status ("PENDING", "COMPLETED" - only 2-3 values)
        ❌ country (200 values, uneven distribution)
        ❌ boolean flag (true/false - only 2 values)
        ❌ category (10-100 values)
        ❌ date (365 values, creates hot partitions)
        
        Rule: Aim for 100+ unique values, ideally millions
        */
    }
    
    /**
     * Criterion 2: Even Distribution
     */
    public void criterion2_EvenDistribution() {
        /*
        Good: Uniform access across values
        ✅ userId (users accessed roughly equally)
        ✅ orderId (orders processed uniformly)
        
        Bad: Uneven access
        ❌ country ("US" gets 80% of traffic)
        ❌ celebrity (one celebrity gets 90% of requests)
        ❌ tenantId (one tenant much larger than others)
        
        Solution for uneven: Write sharding
        */
    }
    
    /**
     * Criterion 3: Aligns with Query Patterns
     */
    public void criterion3_AlignWithQueries() {
        /*
        Choose partition key based on most common query
        
        Example: E-commerce orders
        Most common: "Get user's orders"
        Best PK: userId
        
        Other queries: Use GSIs
        "Get order by orderId" → GSI with PK=orderId
        "Get pending orders" → GSI with PK=status
        */
    }
    
    /**
     * Anti-Pattern Examples
     */
    public void antiPatterns() {
        /*
        ANTI-PATTERN 1: Date as partition key
        ────────────────────────────────────────
        PK: orderDate ❌
        Problem: All today's writes go to one partition
        Solution: PK=userId, SK=orderDate ✅
        
        ANTI-PATTERN 2: Status as partition key
        ────────────────────────────────────────
        PK: status ❌
        Problem: Only 2-3 partitions, uneven distribution
        Solution: PK=userId, GSI PK=status ✅
        
        ANTI-PATTERN 3: Constant value as partition key
        ────────────────────────────────────────────────
        PK: "ORDERS" ❌
        Problem: Everything in one partition!
        Solution: PK=userId or orderId ✅
        
        ANTI-PATTERN 4: Compound key as string
        ────────────────────────────────────────
        PK: "userId#orderDate" ❌
        Problem: Can't do range queries on date
        Solution: PK=userId, SK=orderDate ✅
        */
    }
}
```

### Error Handling and Retries

**Robust Error Handling:**

```java
package com.example.bestpractices;

import org.springframework.stereotype.Service;
import software.amazon.awssdk.core.exception.SdkException;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.util.*;

/**
 * Error Handling Best Practices
 */
@Service
public class ErrorHandlingService {
    
    private final DynamoDbClient client;
    
    public ErrorHandlingService(DynamoDbClient client) {
        this.client = client;
    }
    
    /**
     * Handle all DynamoDB exceptions properly
     */
    public void robustPutItem(Map<String, AttributeValue> item) {
        try {
            PutItemRequest request = PutItemRequest.builder()
                .tableName("Orders")
                .item(item)
                .build();
            
            client.putItem(request);
            
        } catch (ProvisionedThroughputExceededException e) {
            // Throttled - retry with exponential backoff
            retryWithBackoff(() -> client.putItem(PutItemRequest.builder()
                .tableName("Orders")
                .item(item)
                .build()));
            
        } catch (ResourceNotFoundException e) {
            // Table doesn't exist
            throw new RuntimeException("Table not found: Orders", e);
            
        } catch (ConditionalCheckFailedException e) {
            // Condition failed (expected for conditional writes)
            throw new RuntimeException("Condition check failed", e);
            
        } catch (TransactionConflictException e) {
            // Transaction conflict - retry
            retryTransaction();
            
        } catch (ValidationException e) {
            // Invalid request (fix code, don't retry)
            throw new RuntimeException("Invalid request", e);
            
        } catch (InternalServerErrorException e) {
            // AWS server error - retry
            retryWithBackoff(() -> client.putItem(PutItemRequest.builder()
                .tableName("Orders")
                .item(item)
                .build()));
            
        } catch (SdkException e) {
            // Generic SDK exception
            throw new RuntimeException("DynamoDB error", e);
        }
    }
    
    /**
     * Exponential backoff retry strategy
     */
    private void retryWithBackoff(Runnable operation) {
        int maxRetries = 5;
        int baseDelay = 100; // ms
        
        for (int i = 0; i < maxRetries; i++) {
            try {
                operation.run();
                return; // Success
                
            } catch (ProvisionedThroughputExceededException | InternalServerErrorException e) {
                if (i == maxRetries - 1) {
                    throw e; // Max retries reached
                }
                
                long delay = (long) (baseDelay * Math.pow(2, i));
                try {
                    Thread.sleep(delay);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw new RuntimeException("Retry interrupted", ie);
                }
            }
        }
    }
    
    /**
     * Handle batch operation failures
     */
    public void robustBatchWrite(List<Map<String, AttributeValue>> items) {
        List<WriteRequest> writeRequests = items.stream()
            .map(item -> WriteRequest.builder()
                .putRequest(PutRequest.builder().item(item).build())
                .build())
            .toList();
        
        Map<String, List<WriteRequest>> requestItems = new HashMap<>();
        requestItems.put("Orders", writeRequests);
        
        // Retry unprocessed items
        int maxAttempts = 5;
        for (int attempt = 0; attempt < maxAttempts && !requestItems.isEmpty(); attempt++) {
            try {
                BatchWriteItemRequest request = BatchWriteItemRequest.builder()
                    .requestItems(requestItems)
                    .build();
                
                BatchWriteItemResponse response = client.batchWriteItem(request);
                requestItems = response.unprocessedItems();
                
                if (!requestItems.isEmpty()) {
                    Thread.sleep((long) Math.pow(2, attempt) * 100);
                }
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
        
        if (!requestItems.isEmpty()) {
            throw new RuntimeException("Failed to process all items after " + maxAttempts + " attempts");
        }
    }
    
    private void retryTransaction() {
        // Implementation for transaction retry
    }
}
```

### Common Mistakes to Avoid

**Top Mistakes:**

```java
package com.example.bestpractices;

import org.springframework.stereotype.Component;

/**
 * Common DynamoDB Mistakes and How to Avoid Them
 */
@Component
public class CommonMistakes {
    
    /**
     * Mistake 1: Using Scan in production
     */
    public void mistake1_UsingScan() {
        /*
        ❌ WRONG:
        Scan entire table to find items
        
        ✅ CORRECT:
        Design table with proper keys/indexes
        Use Query operations
        Add GSI if needed
        */
    }
    
    /**
     * Mistake 2: Not using batch operations
     */
    public void mistake2_NotUsingBatch() {
        /*
        ❌ WRONG:
        for (item : items) {
            PutItem(item);  // 100 individual requests
        }
        
        ✅ CORRECT:
        BatchWriteItem(items);  // 4 batch requests
        
        Benefit: 25x faster, lower cost
        */
    }
    
    /**
     * Mistake 3: Ignoring capacity planning
     */
    public void mistake3_IgnoringCapacity() {
        /*
        ❌ WRONG:
        Set random capacity values
        Don't monitor usage
        Get throttled in production
        
        ✅ CORRECT:
        Calculate required capacity
        Monitor CloudWatch metrics
        Set up auto-scaling
        Plan for peak traffic
        */
    }
    
    /**
     * Mistake 4: Not using TTL
     */
    public void mistake4_NotUsingTTL() {
        /*
        ❌ WRONG:
        Store temporary data forever
        Manually delete expired items (costs WCUs)
        
        ✅ CORRECT:
        Enable TTL for temporary data
        Free automatic deletion
        Lower costs
        */
    }
    
    /**
     * Mistake 5: Storing large items
     */
    public void mistake5_LargeItems() {
        /*
        ❌ WRONG:
        Store 300KB images in DynamoDB
        Hit 400KB item limit
        High costs
        
        ✅ CORRECT:
        Store large data in S3
        Store S3 URL in DynamoDB
        Better performance, lower cost
        */
    }
    
    /**
     * Mistake 6: Not using GSIs properly
     */
    public void mistake6_PoorGSIDesign() {
        /*
        ❌ WRONG:
        Create GSI for every attribute
        Use ALL projection everywhere
        High costs
        
        ✅ CORRECT:
        GSIs only for query patterns
        Use KEYS_ONLY or INCLUDE projection
        Consolidate with index overloading
        */
    }
    
    /**
     * Mistake 7: Thinking SQL mindset
     */
    public void mistake7_SQLMindset() {
        /*
        ❌ WRONG:
        Design normalized tables
        Try to use JOINs
        Query arbitrary fields
        
        ✅ CORRECT:
        Access patterns first
        Denormalize data
        Query only keys/indexes
        Single-table design for related data
        */
    }
    
    /**
     * Mistake 8: Not handling errors
     */
    public void mistake8_NoErrorHandling() {
        /*
        ❌ WRONG:
        Ignore exceptions
        Don't retry throttled requests
        Assume all writes succeed
        
        ✅ CORRECT:
        Catch all DynamoDB exceptions
        Implement exponential backoff
        Handle unprocessed items
        Log failures for debugging
        */
    }
    
    /**
     * Mistake 9: Ignoring costs
     */
    public void mistake9_IgnoringCosts() {
        /*
        ❌ WRONG:
        Over-provision capacity
        Use on-demand for consistent workloads
        Don't use reserved capacity
        
        ✅ CORRECT:
        Right-size capacity
        Use provisioned for steady workloads
        Purchase reserved capacity
        Monitor and optimize
        */
    }
    
    /**
     * Mistake 10: Not testing locally
     */
    public void mistake10_NoLocalTesting() {
        /*
        ❌ WRONG:
        Test only against AWS
        High costs
        Slow iteration
        
        ✅ CORRECT:
        Use DynamoDB Local for development
        Fast, free testing
        CI/CD integration
        */
    }
}
```

---

## Summary of Part 2

This comprehensive guide covered advanced DynamoDB topics:

### 4. Indexes (GSI and LSI)

- **Global Secondary Indexes** (different partition key, eventually consistent, flexible)
- **Local Secondary Indexes** (same partition key, strongly consistent, created at table creation)
- **GSI vs LSI comparison** with decision matrix
- **Sparse indexes** for 99% cost reduction
- **Attribute projection types** (KEYS_ONLY, INCLUDE, ALL) with cost analysis
- **Index overloading** pattern to reduce GSI count
- **Query performance optimization** techniques

### 5. Capacity Modes and Performance

- **Provisioned vs On-Demand** comparison with cost examples
- **RCU/WCU calculation** formulas and examples
- **Auto-scaling configuration** for automatic capacity adjustment
- **Throttling and burst capacity** handling
- **Cost optimization strategies** (8 proven techniques)

### 6. Advanced Features

- **DynamoDB Streams** for change data capture
- **TTL** for automatic item deletion (free!)
- **Transactions** for ACID compliance
- **Point-in-Time Recovery** (mentioned)
- **Global Tables** (mentioned)
- **DAX caching** (mentioned)

### 7. Best Practices and Anti-Patterns

- **Hot partition problem** and 5 solutions
- **Query vs Scan** rules (never Scan in production!)
- **400KB item size limit** and optimization techniques
- **Proper partition key selection** criteria
- **Error handling and retries** with exponential backoff
- **Common mistakes** to avoid (top 10)

### Key Takeaways from Part 2

✅ Use GSIs for flexibility, LSIs for strong consistency  
✅ Provisioned mode for steady workloads (up to 93% cheaper)  
✅ Sparse indexes save 99% storage for subset queries  
✅ Write sharding solves hot partition problems  
✅ Never use Scan in production application code  
✅ Store large data in S3, not DynamoDB  
✅ Always use batch operations (25x faster)  
✅ Enable TTL for temporary data (free deletion)  
✅ Monitor CloudWatch metrics and set up auto-scaling  
✅ Design tables for access patterns, not entities

---

## Interview Questions - Part 2

**Q1: What's the difference between GSI and LSI?** A: GSI has different partition key from base table, eventually consistent only, can be created/deleted anytime. LSI has same partition key as base table, supports strong consistency, must be created at table creation time. Use GSI for most cases due to flexibility. Use LSI only when you need alternative sort order with strong consistency for items in same partition.

**Q2: When should you use Provisioned vs On-Demand capacity?** A: Provisioned for predictable, steady workloads with >25% utilization (can be 93% cheaper with reserved capacity). On-Demand for unpredictable/spiky traffic, new applications, development/testing, or low-volume workloads. Rule of thumb: consistent traffic → Provisioned; sporadic traffic → On-Demand.

**Q3: How do you solve the hot partition problem?** A: 5 solutions: (1) Write sharding - add random suffix to partition key, (2) Use high-cardinality partition key (userId not status), (3) Replicate popular items across partitions, (4) Add caching layer (DAX/ElastiCache), (5) Rely on adaptive capacity (automatic). Best: Good partition key design prevents problem.

**Q4: When is it acceptable to use Scan?** A: Only for: one-time data exports, analytics during off-peak hours, tables with <1,000 items, admin operations (not user-facing), parallel scan for bulk processing. Never use Scan in production application code for user-facing queries. If you're using Scan regularly, your table design is wrong - add a GSI.

**Q5: What are the benefits of sparse indexes?** A: Sparse indexes only contain items with the index key attribute, dramatically reducing storage (up to 99%). Example: 1M orders with only 10K pending - sparse GSI stores just 10K items instead of 1M. Benefits: lower storage cost, faster queries (less data to scan), better for subset queries. Implement by only setting GSI key attribute for relevant items.

**Q6: How do you calculate RCUs and WCUs?** A: RCU = (Item size / 4KB) × Reads/sec × Consistency factor (1 for strong, 0.5 for eventual). WCU = (Item size / 1KB) × Writes/sec. Example: 100 eventually consistent reads/sec of 2KB items = (2/4) × 100 × 0.5 = 25 RCUs. 50 writes/sec of 3KB items = 3 × 50 = 150 WCUs. Always round up partial KBs.

---
