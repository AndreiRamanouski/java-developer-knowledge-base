# Hazelcast with Spring Boot - Complete Guide

## Overview

Hazelcast is an in-memory distributed computing platform providing distributed data structures, caching, and computing capabilities. Unlike Redis (single-threaded, cache-focused), Hazelcast is multi-threaded and designed for distributed computing with built-in cluster management. It runs as embedded within your application (no separate server) or client-server mode. Perfect for distributed caching, session replication, distributed locks, and in-memory processing.

**Key Concept**: Hazelcast = Redis + distributed computing. Embedded mode runs IN your app (no external server). Data automatically partitioned and replicated across cluster. Use IMap for distributed cache (like Redis but with backups), IQueue for distributed queues, ILock for distributed locking. Near cache for local caching. Supports both Spring Cache abstraction and native API. WAN replication for disaster recovery. Split-brain protection prevents data inconsistency.

---

## 1. Hazelcast Setup with Spring Boot

### spring-boot-starter-hazelcast

**Maven Dependencies:**

```xml
<dependencies>
    <!-- Hazelcast Spring Boot Starter -->
    <dependency>
        <groupId>com.hazelcast</groupId>
        <artifactId>hazelcast-spring</artifactId>
        <version>5.3.6</version>
    </dependency>
    
    <!-- Hazelcast Core -->
    <dependency>
        <groupId>com.hazelcast</groupId>
        <artifactId>hazelcast</artifactId>
        <version>5.3.6</version>
    </dependency>
    
    <!-- Spring Cache Support -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-cache</artifactId>
    </dependency>
    
    <!-- Optional: Hazelcast Kubernetes Discovery -->
    <dependency>
        <groupId>com.hazelcast</groupId>
        <artifactId>hazelcast-kubernetes</artifactId>
        <version>2.2.3</version>
    </dependency>
    
    <!-- Optional: Hazelcast Management Center Client -->
    <dependency>
        <groupId>com.hazelcast</groupId>
        <artifactId>hazelcast-enterprise</artifactId>
        <version>5.3.6</version>
    </dependency>
</dependencies>
```

**Gradle Dependencies:**

```gradle
dependencies {
    // Hazelcast Spring
    implementation 'com.hazelcast:hazelcast-spring:5.3.6'
    
    // Hazelcast Core
    implementation 'com.hazelcast:hazelcast:5.3.6'
    
    // Spring Cache
    implementation 'org.springframework.boot:spring-boot-starter-cache'
    
    // Optional: Kubernetes discovery
    implementation 'com.hazelcast:hazelcast-kubernetes:2.2.3'
}
```

### Embedded vs Client-Server Mode

**Mode Comparison:**

```
┌──────────────────────────────────────────────────────────────┐
│         Embedded Mode vs Client-Server Mode                   │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  EMBEDDED MODE (Default)                                      │
│  ──────────────────────────                                  │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   App 1     │  │   App 2     │  │   App 3     │          │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤          │
│  │  Hazelcast  │  │  Hazelcast  │  │  Hazelcast  │          │
│  │   Member    │  │   Member    │  │   Member    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│         │                 │                 │                │
│         └─────────────────┴─────────────────┘                │
│                    Cluster                                   │
│                                                               │
│  Characteristics:                                            │
│  ✅ No separate server needed                                │
│  ✅ Data stored in app JVM                                   │
│  ✅ Lower latency (local access)                             │
│  ✅ Simpler deployment                                       │
│  ❌ Couples data lifecycle to app                            │
│  ❌ Higher memory usage per app                              │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  CLIENT-SERVER MODE                                          │
│  ──────────────────────                                      │
│                                                               │
│  ┌────────┐  ┌────────┐  ┌────────┐                         │
│  │ App 1  │  │ App 2  │  │ App 3  │                         │
│  │(Client)│  │(Client)│  │(Client)│                         │
│  └───┬────┘  └───┬────┘  └───┬────┘                         │
│      │           │           │                              │
│      └───────────┼───────────┘                              │
│                  │                                          │
│  ┌──────────────┴──────────────┐                           │
│  │                              │                           │
│  ┌──────────┐  ┌──────────┐   ┌──────────┐                │
│  │Hazelcast │  │Hazelcast │   │Hazelcast │                │
│  │ Server 1 │  │ Server 2 │   │ Server 3 │                │
│  └──────────┘  └──────────┘   └──────────┘                │
│                 Data Cluster                                │
│                                                               │
│  Characteristics:                                            │
│  ✅ Separate data tier                                       │
│  ✅ Independent scaling                                      │
│  ✅ App restarts don't affect data                          │
│  ✅ Better resource isolation                                │
│  ❌ Network overhead                                         │
│  ❌ More complex deployment                                  │
│                                                               │
│  When to Use:                                                │
│  Embedded: Microservices, simple deployments, low latency   │
│  Client-Server: Production, large datasets, separate scaling │
└──────────────────────────────────────────────────────────────┘
```

**Embedded Mode Configuration:**

```java
@Configuration
@EnableCaching
public class HazelcastEmbeddedConfig {
    
    /**
     * Embedded Hazelcast instance
     * Runs inside application JVM
     */
    @Bean
    public Config hazelcastConfig() {
        Config config = new Config();
        config.setInstanceName("hazelcast-instance");
        
        // Cluster name (instances with same name form cluster)
        config.setClusterName("dev-cluster");
        
        // Network configuration
        NetworkConfig networkConfig = config.getNetworkConfig();
        networkConfig.setPort(5701);  // Default port
        networkConfig.setPortAutoIncrement(true);  // Try 5702, 5703 if 5701 used
        
        // Join configuration (multicast for local development)
        JoinConfig joinConfig = networkConfig.getJoin();
        joinConfig.getMulticastConfig()
            .setEnabled(true)
            .setMulticastGroup("224.2.2.3")
            .setMulticastPort(54327);
        
        // Disable other discovery methods
        joinConfig.getTcpIpConfig().setEnabled(false);
        joinConfig.getAwsConfig().setEnabled(false);
        
        return config;
    }
    
    /**
     * Hazelcast instance bean
     */
    @Bean
    public HazelcastInstance hazelcastInstance(Config config) {
        return Hazelcast.newHazelcastInstance(config);
    }
    
    /**
     * Spring Cache Manager using Hazelcast
     */
    @Bean
    public CacheManager cacheManager(HazelcastInstance hazelcastInstance) {
        return new HazelcastCacheManager(hazelcastInstance);
    }
}
```

**Client-Server Mode Configuration:**

Server:

```java
@Configuration
public class HazelcastServerConfig {
    
    @Bean
    public Config hazelcastServerConfig() {
        Config config = new Config();
        config.setClusterName("prod-cluster");
        
        // Network configuration
        NetworkConfig networkConfig = config.getNetworkConfig();
        networkConfig.setPort(5701);
        
        // TCP/IP discovery for production
        JoinConfig joinConfig = networkConfig.getJoin();
        joinConfig.getMulticastConfig().setEnabled(false);
        joinConfig.getTcpIpConfig()
            .setEnabled(true)
            .addMember("10.0.1.10")
            .addMember("10.0.1.11")
            .addMember("10.0.1.12");
        
        // Map configuration
        MapConfig mapConfig = new MapConfig("default");
        mapConfig.setBackupCount(1);  // 1 sync backup
        mapConfig.setAsyncBackupCount(1);  // 1 async backup
        mapConfig.setTimeToLiveSeconds(3600);  // 1 hour TTL
        
        config.addMapConfig(mapConfig);
        
        return config;
    }
    
    @Bean
    public HazelcastInstance hazelcastServerInstance(Config config) {
        return Hazelcast.newHazelcastInstance(config);
    }
}
```

Client:

```java
@Configuration
@EnableCaching
public class HazelcastClientConfig {
    
    @Bean
    public ClientConfig hazelcastClientConfig() {
        ClientConfig clientConfig = new ClientConfig();
        clientConfig.setClusterName("prod-cluster");
        
        // Network configuration - connect to cluster
        ClientNetworkConfig networkConfig = clientConfig.getNetworkConfig();
        networkConfig.addAddress("10.0.1.10:5701", "10.0.1.11:5701", "10.0.1.12:5701");
        
        // Connection retry
        networkConfig.setConnectionTimeout(5000);
        networkConfig.getConnectionPoolConfig()
            .setMaxSize(50);
        
        // Smart routing (client aware of data location)
        networkConfig.setSmartRouting(true);
        
        // Near cache configuration
        NearCacheConfig nearCacheConfig = new NearCacheConfig();
        nearCacheConfig.setName("default");
        nearCacheConfig.setInMemoryFormat(InMemoryFormat.OBJECT);
        nearCacheConfig.setTimeToLiveSeconds(300);  // 5 minutes
        nearCacheConfig.setMaxIdleSeconds(60);
        
        clientConfig.addNearCacheConfig(nearCacheConfig);
        
        return clientConfig;
    }
    
    @Bean
    public HazelcastInstance hazelcastClientInstance(ClientConfig clientConfig) {
        return HazelcastClient.newHazelcastClient(clientConfig);
    }
    
    @Bean
    public CacheManager cacheManager(HazelcastInstance hazelcastInstance) {
        return new HazelcastCacheManager(hazelcastInstance);
    }
}
```

### Cluster Discovery Mechanisms

**Multicast Discovery (Development):**

```java
public Config multicastDiscoveryConfig() {
    Config config = new Config();
    
    JoinConfig joinConfig = config.getNetworkConfig().getJoin();
    
    // Multicast for local development
    MulticastConfig multicastConfig = joinConfig.getMulticastConfig();
    multicastConfig.setEnabled(true);
    multicastConfig.setMulticastGroup("224.2.2.3");
    multicastConfig.setMulticastPort(54327);
    multicastConfig.setMulticastTimeToLive(32);
    
    // Disable other methods
    joinConfig.getTcpIpConfig().setEnabled(false);
    
    return config;
}
```

**TCP/IP Discovery (Production):**

```java
public Config tcpIpDiscoveryConfig() {
    Config config = new Config();
    
    JoinConfig joinConfig = config.getNetworkConfig().getJoin();
    
    // Disable multicast
    joinConfig.getMulticastConfig().setEnabled(false);
    
    // TCP/IP with known members
    TcpIpConfig tcpIpConfig = joinConfig.getTcpIpConfig();
    tcpIpConfig.setEnabled(true);
    tcpIpConfig.addMember("10.0.1.10");
    tcpIpConfig.addMember("10.0.1.11");
    tcpIpConfig.addMember("10.0.1.12");
    
    // Required member for cluster formation
    tcpIpConfig.setRequiredMember("10.0.1.10");
    
    return config;
}
```

**Kubernetes Discovery:**

```java
public Config kubernetesDiscoveryConfig() {
    Config config = new Config();
    
    JoinConfig joinConfig = config.getNetworkConfig().getJoin();
    
    // Disable other discovery
    joinConfig.getMulticastConfig().setEnabled(false);
    joinConfig.getTcpIpConfig().setEnabled(false);
    
    // Kubernetes discovery
    KubernetesConfig kubernetesConfig = joinConfig.getKubernetesConfig();
    kubernetesConfig.setEnabled(true);
    kubernetesConfig.setProperty("namespace", "default");
    kubernetesConfig.setProperty("service-name", "hazelcast-service");
    kubernetesConfig.setProperty("service-port", "5701");
    
    return config;
}
```

**AWS EC2 Discovery:**

```java
public Config awsDiscoveryConfig() {
    Config config = new Config();
    
    JoinConfig joinConfig = config.getNetworkConfig().getJoin();
    
    joinConfig.getMulticastConfig().setEnabled(false);
    joinConfig.getTcpIpConfig().setEnabled(false);
    
    // AWS discovery
    AwsConfig awsConfig = joinConfig.getAwsConfig();
    awsConfig.setEnabled(true);
    awsConfig.setProperty("access-key", "your-access-key");
    awsConfig.setProperty("secret-key", "your-secret-key");
    awsConfig.setProperty("region", "us-east-1");
    awsConfig.setProperty("tag-key", "hazelcast-cluster");
    awsConfig.setProperty("tag-value", "prod");
    
    return config;
}
```

### Hazelcast Configuration File vs Programmatic

**hazelcast.xml Configuration:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<hazelcast xmlns="http://www.hazelcast.com/schema/config"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.hazelcast.com/schema/config
           http://www.hazelcast.com/schema/config/hazelcast-config-5.3.xsd">
    
    <cluster-name>dev-cluster</cluster-name>
    <instance-name>dev-instance</instance-name>
    
    <network>
        <port auto-increment="true">5701</port>
        
        <join>
            <multicast enabled="true">
                <multicast-group>224.2.2.3</multicast-group>
                <multicast-port>54327</multicast-port>
            </multicast>
            
            <tcp-ip enabled="false"/>
            <aws enabled="false"/>
        </join>
    </network>
    
    <!-- Map configuration -->
    <map name="users">
        <backup-count>1</backup-count>
        <async-backup-count>1</async-backup-count>
        <time-to-live-seconds>3600</time-to-live-seconds>
        <max-idle-seconds>300</max-idle-seconds>
        
        <eviction eviction-policy="LRU" max-size-policy="PER_NODE" size="10000"/>
        
        <indexes>
            <index type="HASH">
                <attributes>
                    <attribute>userId</attribute>
                </attributes>
            </index>
        </indexes>
    </map>
    
    <!-- Near cache configuration -->
    <near-cache name="users">
        <in-memory-format>OBJECT</in-memory-format>
        <invalidate-on-change>true</invalidate-on-change>
        <time-to-live-seconds>300</time-to-live-seconds>
        <max-idle-seconds>60</max-idle-seconds>
        <eviction eviction-policy="LRU" max-size-policy="ENTRY_COUNT" size="1000"/>
    </near-cache>
</hazelcast>
```

**Load XML Configuration:**

```java
@Configuration
public class HazelcastXmlConfig {
    
    @Bean
    public HazelcastInstance hazelcastInstance() {
        // Load from classpath
        return Hazelcast.newHazelcastInstance(
            new ClasspathXmlConfig("hazelcast.xml")
        );
    }
    
    // Or load from file system
    @Bean
    public HazelcastInstance hazelcastInstanceFromFile() {
        return Hazelcast.newHazelcastInstance(
            new FileSystemXmlConfig("/etc/hazelcast/hazelcast.xml")
        );
    }
}
```

**Programmatic Configuration (Recommended for Spring Boot):**

```java
@Configuration
public class HazelcastProgrammaticConfig {
    
    @Bean
    public Config hazelcastConfig() {
        Config config = new Config();
        config.setClusterName("app-cluster");
        
        // Network
        NetworkConfig networkConfig = config.getNetworkConfig();
        networkConfig.setPort(5701);
        networkConfig.setPortAutoIncrement(true);
        
        // Discovery
        JoinConfig joinConfig = networkConfig.getJoin();
        joinConfig.getMulticastConfig()
            .setEnabled(true)
            .setMulticastGroup("224.2.2.3");
        
        // Map configuration
        MapConfig mapConfig = new MapConfig("users");
        mapConfig.setBackupCount(1);
        mapConfig.setAsyncBackupCount(1);
        mapConfig.setTimeToLiveSeconds(3600);
        mapConfig.setMaxIdleSeconds(300);
        
        // Eviction
        EvictionConfig evictionConfig = new EvictionConfig();
        evictionConfig.setEvictionPolicy(EvictionPolicy.LRU);
        evictionConfig.setMaxSizePolicy(MaxSizePolicy.PER_NODE);
        evictionConfig.setSize(10000);
        mapConfig.setEvictionConfig(evictionConfig);
        
        config.addMapConfig(mapConfig);
        
        return config;
    }
    
    @Bean
    public HazelcastInstance hazelcastInstance(Config config) {
        return Hazelcast.newHazelcastInstance(config);
    }
}
```

### Spring Boot Auto-Configuration

**application.yml:**

```yaml
spring:
  cache:
    type: hazelcast
  
  hazelcast:
    config: classpath:hazelcast.xml  # External config file

# Hazelcast configuration
hazelcast:
  cluster-name: spring-boot-cluster
  instance-name: spring-boot-instance
  
  network:
    port: 5701
    port-auto-increment: true
    join:
      multicast:
        enabled: true
        multicast-group: 224.2.2.3
        multicast-port: 54327
  
  # Map configurations
  map:
    default:
      backup-count: 1
      time-to-live-seconds: 0  # No TTL
      max-idle-seconds: 0
      eviction:
        eviction-policy: LRU
        max-size-policy: PER_NODE
        size: 10000
    
    users:
      backup-count: 1
      time-to-live-seconds: 3600  # 1 hour
      
    sessions:
      backup-count: 2
      time-to-live-seconds: 1800  # 30 minutes
```

**Auto-Configuration Bean:**

```java
@Configuration
@ConditionalOnClass(HazelcastInstance.class)
@ConditionalOnProperty(name = "spring.cache.type", havingValue = "hazelcast")
public class HazelcastAutoConfiguration {
    
    @Bean
    @ConditionalOnMissingBean
    public HazelcastInstance hazelcastInstance() {
        Config config = new Config();
        config.setClusterName("spring-boot-auto");
        
        // Auto-configuration with sensible defaults
        return Hazelcast.newHazelcastInstance(config);
    }
    
    @Bean
    @ConditionalOnMissingBean
    public CacheManager cacheManager(HazelcastInstance hazelcastInstance) {
        return new HazelcastCacheManager(hazelcastInstance);
    }
}
```

### Integration with Spring Cache

**Enable Caching:**

```java
@SpringBootApplication
@EnableCaching
public class Application {
    
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

**Using @Cacheable:**

```java
@Service
@Slf4j
public class UserService {
    
    private final UserRepository userRepository;
    
    /**
     * Cache user queries
     */
    @Cacheable(value = "users", key = "#userId")
    public User getUserById(String userId) {
        log.info("Fetching user from database: {}", userId);
        
        // Expensive database query
        return userRepository.findById(userId).orElse(null);
    }
    
    /**
     * Cache with condition
     */
    @Cacheable(value = "users", key = "#email", 
               condition = "#email != null && #email.length() > 0")
    public User getUserByEmail(String email) {
        log.info("Fetching user by email: {}", email);
        
        return userRepository.findByEmail(email).orElse(null);
    }
    
    /**
     * Update cache on modification
     */
    @CachePut(value = "users", key = "#user.userId")
    public User updateUser(User user) {
        log.info("Updating user: {}", user.getUserId());
        
        return userRepository.save(user);
    }
    
    /**
     * Evict cache entry
     */
    @CacheEvict(value = "users", key = "#userId")
    public void deleteUser(String userId) {
        log.info("Deleting user: {}", userId);
        
        userRepository.deleteById(userId);
    }
    
    /**
     * Evict entire cache
     */
    @CacheEvict(value = "users", allEntries = true)
    public void clearUserCache() {
        log.info("Clearing entire user cache");
    }
    
    /**
     * Multiple cache operations
     */
    @Caching(
        put = @CachePut(value = "users", key = "#user.userId"),
        evict = @CacheEvict(value = "usersByEmail", key = "#user.email")
    )
    public User updateUserWithEmailChange(User user) {
        return userRepository.save(user);
    }
}
```

**Programmatic Cache Access:**

```java
@Service
@RequiredArgsConstructor
public class CacheManagementService {
    
    private final CacheManager cacheManager;
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Direct cache access via Spring CacheManager
     */
    public void manageCache() {
        Cache usersCache = cacheManager.getCache("users");
        
        // Put
        usersCache.put("user-123", new User("123", "John"));
        
        // Get
        User user = usersCache.get("user-123", User.class);
        
        // Evict
        usersCache.evict("user-123");
        
        // Clear
        usersCache.clear();
    }
    
    /**
     * Direct Hazelcast IMap access
     */
    public void useIMapDirectly() {
        IMap<String, User> users = hazelcastInstance.getMap("users");
        
        // All IMap operations available
        users.put("user-456", new User("456", "Jane"));
        users.putIfAbsent("user-456", new User("456", "Jane Doe"));
        
        User user = users.get("user-456");
    }
    
    /**
     * Get cache statistics
     */
    public Map<String, Object> getCacheStats(String cacheName) {
        IMap<?, ?> map = hazelcastInstance.getMap(cacheName);
        LocalMapStats stats = map.getLocalMapStats();
        
        return Map.of(
            "size", stats.getOwnedEntryCount(),
            "backupSize", stats.getBackupEntryCount(),
            "hits", stats.getHits(),
            "getOperations", stats.getGetOperationCount(),
            "putOperations", stats.getPutOperationCount(),
            "memoryCost", stats.getOwnedEntryMemoryCost()
        );
    }
}
```

---

## 2. Distributed Data Structures

### IMap (Distributed Map)

**Basic IMap Operations:**

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class HazelcastMapService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Get distributed map
     */
    public IMap<String, User> getUserMap() {
        return hazelcastInstance.getMap("users");
    }
    
    /**
     * Basic operations
     */
    public void basicMapOperations() {
        IMap<String, User> users = getUserMap();
        
        // Put
        users.put("user-123", new User("123", "John", "john@example.com"));
        
        // Put with TTL (30 minutes)
        users.put("user-456", new User("456", "Jane", "jane@example.com"),
            30, TimeUnit.MINUTES);
        
        // Get
        User user = users.get("user-123");
        
        // Put if absent
        User previous = users.putIfAbsent("user-789", 
            new User("789", "Bob", "bob@example.com"));
        
        // Replace
        users.replace("user-123", new User("123", "John Doe", "john@example.com"));
        
        // Remove
        users.remove("user-456");
        
        // Check existence
        boolean exists = users.containsKey("user-123");
        
        // Size
        int size = users.size();
        
        // Clear all
        users.clear();
    }
    
    /**
     * Async operations (non-blocking)
     */
    public CompletableFuture<User> getAsync(String userId) {
        IMap<String, User> users = getUserMap();
        
        return users.getAsync(userId).toCompletableFuture();
    }
    
    public CompletableFuture<Void> putAsync(String userId, User user) {
        IMap<String, User> users = getUserMap();
        
        return users.putAsync(userId, user)
            .toCompletableFuture()
            .thenAccept(previous -> 
                log.info("User {} updated", userId));
    }
    
    /**
     * Batch operations
     */
    public void batchOperations() {
        IMap<String, User> users = getUserMap();
        
        // Put all
        Map<String, User> batch = Map.of(
            "user-1", new User("1", "User 1", "u1@ex.com"),
            "user-2", new User("2", "User 2", "u2@ex.com"),
            "user-3", new User("3", "User 3", "u3@ex.com")
        );
        users.putAll(batch);
        
        // Get all
        Set<String> keys = Set.of("user-1", "user-2", "user-3");
        Map<String, User> result = users.getAll(keys);
    }
    
    /**
     * Lock-based operations
     */
    public void lockedUpdate(String userId) {
        IMap<String, User> users = getUserMap();
        
        // Lock key
        users.lock(userId);
        
        try {
            User user = users.get(userId);
            // Modify user
            user.setEmail("new@example.com");
            users.put(userId, user);
            
        } finally {
            users.unlock(userId);
        }
    }
    
    /**
     * Try lock with timeout
     */
    public boolean tryLockedUpdate(String userId, long timeout, TimeUnit unit) {
        IMap<String, User> users = getUserMap();
        
        try {
            if (users.tryLock(userId, timeout, unit)) {
                try {
                    User user = users.get(userId);
                    user.setEmail("updated@example.com");
                    users.put(userId, user);
                    return true;
                    
                } finally {
                    users.unlock(userId);
                }
            }
            return false;
            
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        }
    }
}
```

### IQueue (Distributed Queue)

**Distributed Queue Operations:**

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class HazelcastQueueService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Get distributed queue
     */
    public IQueue<Task> getTaskQueue() {
        return hazelcastInstance.getQueue("tasks");
    }
    
    /**
     * Producer - add tasks to queue
     */
    public void produceTask(Task task) throws InterruptedException {
        IQueue<Task> queue = getTaskQueue();
        
        // Add to queue (blocks if full)
        queue.put(task);
        
        log.info("Task produced: {}", task.getId());
    }
    
    /**
     * Offer with timeout
     */
    public boolean offerTask(Task task, long timeout, TimeUnit unit) 
            throws InterruptedException {
        
        IQueue<Task> queue = getTaskQueue();
        
        // Try to add with timeout
        boolean added = queue.offer(task, timeout, unit);
        
        if (added) {
            log.info("Task offered: {}", task.getId());
        } else {
            log.warn("Task rejected (queue full): {}", task.getId());
        }
        
        return added;
    }
    
    /**
     * Consumer - process tasks from queue
     */
    public Task consumeTask() throws InterruptedException {
        IQueue<Task> queue = getTaskQueue();
        
        // Take from queue (blocks if empty)
        Task task = queue.take();
        
        log.info("Task consumed: {}", task.getId());
        
        return task;
    }
    
    /**
     * Poll with timeout
     */
    public Task pollTask(long timeout, TimeUnit unit) throws InterruptedException {
        IQueue<Task> queue = getTaskQueue();
        
        // Poll with timeout
        Task task = queue.poll(timeout, unit);
        
        if (task != null) {
            log.info("Task polled: {}", task.getId());
        }
        
        return task;
    }
    
    /**
     * Background worker processing queue
     */
    @Async
    public void startWorker() {
        IQueue<Task> queue = getTaskQueue();
        
        while (!Thread.currentThread().isInterrupted()) {
            try {
                Task task = queue.take();
                processTask(task);
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    private void processTask(Task task) {
        log.info("Processing task: {}", task.getId());
        // Task processing logic
    }
    
    /**
     * Queue statistics
     */
    public Map<String, Object> getQueueStats() {
        IQueue<Task> queue = getTaskQueue();
        
        return Map.of(
            "size", queue.size(),
            "remainingCapacity", queue.remainingCapacity(),
            "localSize", queue.getLocalQueueStats().getOwnedItemCount()
        );
    }
}
```

### ISet and IList (Distributed Collections)

**Distributed Set:**

```java
@Service
@RequiredArgsConstructor
public class HazelcastSetService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Distributed Set - unique elements
     */
    public void setOperations() {
        ISet<String> tags = hazelcastInstance.getSet("tags");
        
        // Add elements
        tags.add("java");
        tags.add("spring");
        tags.add("hazelcast");
        tags.add("java");  // Duplicate ignored
        
        // Size
        int size = tags.size();  // 3
        
        // Contains
        boolean hasJava = tags.contains("java");
        
        // Remove
        tags.remove("spring");
        
        // Iterate
        tags.forEach(tag -> System.out.println(tag));
        
        // Clear
        tags.clear();
    }
    
    /**
     * Use case: Track unique visitors
     */
    public void trackUniqueVisitor(String pageId, String visitorId) {
        ISet<String> visitors = hazelcastInstance.getSet("visitors:" + pageId);
        
        visitors.add(visitorId);
    }
    
    public int getUniqueVisitorCount(String pageId) {
        ISet<String> visitors = hazelcastInstance.getSet("visitors:" + pageId);
        
        return visitors.size();
    }
}
```

**Distributed List:**

```java
@Service
@RequiredArgsConstructor
public class HazelcastListService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Distributed List - ordered, allows duplicates
     */
    public void listOperations() {
        IList<String> logs = hazelcastInstance.getList("logs");
        
        // Add elements
        logs.add("Log entry 1");
        logs.add("Log entry 2");
        logs.add("Log entry 3");
        
        // Add at index
        logs.add(1, "Inserted log");
        
        // Get by index
        String log = logs.get(0);
        
        // Set at index
        logs.set(0, "Updated log");
        
        // Remove by index
        logs.remove(2);
        
        // Size
        int size = logs.size();
        
        // Sublist
        List<String> subset = logs.subList(0, 2);
    }
    
    /**
     * Use case: Recent activities
     */
    public void addActivity(String userId, String activity) {
        IList<String> activities = hazelcastInstance.getList("activities:" + userId);
        
        activities.add(activity);
        
        // Keep only last 100
        while (activities.size() > 100) {
            activities.remove(0);
        }
    }
    
    public List<String> getRecentActivities(String userId, int limit) {
        IList<String> activities = hazelcastInstance.getList("activities:" + userId);
        
        int size = activities.size();
        int start = Math.max(0, size - limit);
        
        return activities.subList(start, size);
    }
}
```

### ITopic for Pub/Sub

**Topic Operations:**

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class HazelcastTopicService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Publisher - send messages to topic
     */
    public void publishMessage(String topicName, String message) {
        ITopic<String> topic = hazelcastInstance.getTopic(topicName);
        
        topic.publish(message);
        
        log.info("Published to {}: {}", topicName, message);
    }
    
    /**
     * Subscriber - listen for messages
     */
    @PostConstruct
    public void subscribeToTopics() {
        ITopic<String> orderTopic = hazelcastInstance.getTopic("orders");
        
        orderTopic.addMessageListener(message -> {
            log.info("Received order: {}", message.getMessageObject());
            processOrder(message.getMessageObject());
        });
        
        ITopic<String> notificationTopic = hazelcastInstance.getTopic("notifications");
        
        notificationTopic.addMessageListener(message -> {
            log.info("Received notification: {}", message.getMessageObject());
            sendNotification(message.getMessageObject());
        });
    }
    
    /**
     * Reliable Topic (with message history)
     */
    public void reliableTopicOperations() {
        // Reliable topic stores messages in ringbuffer
        ITopic<String> reliableTopic = hazelcastInstance.getReliableTopic("reliable-orders");
        
        // Subscribe
        reliableTopic.addMessageListener(message -> {
            log.info("Reliable message: {}", message.getMessageObject());
        });
        
        // Publish
        reliableTopic.publish("Order #123");
    }
    
    private void processOrder(String order) {
        // Order processing logic
    }
    
    private void sendNotification(String notification) {
        // Notification logic
    }
}
```

### ILock for Distributed Locking

**Distributed Lock:**

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class HazelcastLockService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Basic distributed lock
     */
    public void withLock(String resourceId, Runnable task) {
        ILock lock = hazelcastInstance.getLock(resourceId);
        
        lock.lock();
        try {
            log.info("Lock acquired for: {}", resourceId);
            task.run();
            
        } finally {
            lock.unlock();
            log.info("Lock released for: {}", resourceId);
        }
    }
    
    /**
     * Try lock with timeout
     */
    public boolean tryWithLock(String resourceId, Runnable task, 
                                long timeout, TimeUnit unit) {
        ILock lock = hazelcastInstance.getLock(resourceId);
        
        try {
            if (lock.tryLock(timeout, unit)) {
                try {
                    log.info("Lock acquired for: {}", resourceId);
                    task.run();
                    return true;
                    
                } finally {
                    lock.unlock();
                    log.info("Lock released for: {}", resourceId);
                }
            } else {
                log.warn("Failed to acquire lock for: {}", resourceId);
                return false;
            }
            
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        }
    }
    
    /**
     * Use case: Prevent duplicate processing
     */
    public boolean processOnce(String taskId, Runnable processor) {
        return tryWithLock(
            "task:" + taskId,
            processor,
            5,
            TimeUnit.SECONDS
        );
    }
    
    /**
     * Use case: Leader election
     */
    public boolean tryBecomeLeader(String clusterId) {
        ILock leaderLock = hazelcastInstance.getLock("leader:" + clusterId);
        
        return leaderLock.tryLock();
    }
    
    public void resignLeadership(String clusterId) {
        ILock leaderLock = hazelcastInstance.getLock("leader:" + clusterId);
        
        if (leaderLock.isLockedByCurrentThread()) {
            leaderLock.unlock();
        }
    }
}
```

### Use Cases for Each Structure

**Use Case Examples:**

```java
@Service
@RequiredArgsConstructor
public class HazelcastUseCases {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * IMap: Distributed cache
     * Use: Fast access to frequently used data
     */
    public void cacheProductCatalog() {
        IMap<String, Product> products = hazelcastInstance.getMap("products");
        
        products.put("prod-123", new Product("123", "Laptop", 999.99));
        
        // Fast retrieval across all instances
        Product product = products.get("prod-123");
    }
    
    /**
     * IQueue: Task distribution
     * Use: Distribute work across multiple workers
     */
    public void distributeEmailTasks() {
        IQueue<EmailTask> emailQueue = hazelcastInstance.getQueue("emails");
        
        // Producer
        emailQueue.add(new EmailTask("user@example.com", "Welcome!"));
        
        // Consumer (runs on any instance)
        EmailTask task = emailQueue.poll();
        if (task != null) {
            sendEmail(task);
        }
    }
    
    /**
     * ISet: Track unique users online
     * Use: Real-time online user count
     */
    public void trackOnlineUsers(String userId) {
        ISet<String> onlineUsers = hazelcastInstance.getSet("online-users");
        
        onlineUsers.add(userId);
        
        int count = onlineUsers.size();  // Total online users
    }
    
    /**
     * IList: Activity feed
     * Use: Store ordered list of recent activities
     */
    public void recordActivity(String userId, String activity) {
        IList<Activity> activities = hazelcastInstance.getList("feed:" + userId);
        
        activities.add(new Activity(activity, Instant.now()));
        
        // Keep only last 50
        while (activities.size() > 50) {
            activities.remove(0);
        }
    }
    
    /**
     * ITopic: Real-time notifications
     * Use: Push notifications to all connected users
     */
    public void broadcastNotification(String message) {
        ITopic<String> topic = hazelcastInstance.getTopic("notifications");
        
        // All subscribers receive message
        topic.publish(message);
    }
    
    /**
     * ILock: Prevent duplicate scheduled job execution
     * Use: Ensure only one instance executes cron job
     */
    @Scheduled(fixedRate = 60000)
    public void scheduledJob() {
        ILock lock = hazelcastInstance.getLock("scheduled-job");
        
        if (lock.tryLock()) {
            try {
                // Only one instance executes
                performJobLogic();
                
            } finally {
                lock.unlock();
            }
        }
    }
    
    private void sendEmail(EmailTask task) {
        // Email sending logic
    }
    
    private void performJobLogic() {
        // Job execution logic
    }
}
```

---

## 3. Hazelcast as Distributed Cache

### @Cacheable with Hazelcast

**Spring Cache Integration:**

```java
@Service
@Slf4j
public class ProductService {
    
    private final ProductRepository productRepository;
    
    /**
     * Cache product queries
     */
    @Cacheable(value = "products", key = "#productId")
    public Product getProductById(String productId) {
        log.info("Fetching product from database: {}", productId);
        
        // Expensive database query
        return productRepository.findById(productId).orElse(null);
    }
    
    /**
     * Cache with condition
     */
    @Cacheable(value = "products", key = "#sku", 
               condition = "#sku != null && !#sku.isEmpty()")
    public Product getProductBySku(String sku) {
        log.info("Fetching product by SKU: {}", sku);
        
        return productRepository.findBySku(sku).orElse(null);
    }
    
    /**
     * Update cache on modification
     */
    @CachePut(value = "products", key = "#product.productId")
    public Product updateProduct(Product product) {
        log.info("Updating product: {}", product.getProductId());
        
        return productRepository.save(product);
    }
    
    /**
     * Evict cache entry
     */
    @CacheEvict(value = "products", key = "#productId")
    public void deleteProduct(String productId) {
        log.info("Deleting product: {}", productId);
        
        productRepository.deleteById(productId);
    }
    
    /**
     * Evict entire cache
     */
    @CacheEvict(value = "products", allEntries = true)
    public void clearProductCache() {
        log.info("Clearing entire product cache");
    }
    
    /**
     * Cache with custom key generator
     */
    @Cacheable(value = "products", keyGenerator = "customKeyGenerator")
    public List<Product> searchProducts(String query, int page, int size) {
        return productRepository.search(query, page, size);
    }
}

@Component
public class CustomKeyGenerator implements KeyGenerator {
    
    @Override
    public Object generate(Object target, Method method, Object... params) {
        return Arrays.stream(params)
            .map(String::valueOf)
            .collect(Collectors.joining("_"));
    }
}
```

### Near Cache Configuration

**Near Cache Setup:**

```java
@Configuration
public class HazelcastNearCacheConfig {
    
    @Bean
    public Config hazelcastConfig() {
        Config config = new Config();
        
        // Map configuration
        MapConfig mapConfig = new MapConfig("products");
        mapConfig.setBackupCount(1);
        
        // Near cache configuration
        NearCacheConfig nearCacheConfig = new NearCacheConfig();
        nearCacheConfig.setName("products");
        
        // In-memory format
        nearCacheConfig.setInMemoryFormat(InMemoryFormat.OBJECT);
        
        // Time to live (5 minutes)
        nearCacheConfig.setTimeToLiveSeconds(300);
        
        // Max idle time (1 minute)
        nearCacheConfig.setMaxIdleSeconds(60);
        
        // Invalidate when source map changes
        nearCacheConfig.setInvalidateOnChange(true);
        
        // Eviction configuration
        EvictionConfig evictionConfig = new EvictionConfig();
        evictionConfig.setEvictionPolicy(EvictionPolicy.LRU);
        evictionConfig.setMaxSizePolicy(MaxSizePolicy.ENTRY_COUNT);
        evictionConfig.setSize(1000);
        
        nearCacheConfig.setEvictionConfig(evictionConfig);
        
        mapConfig.setNearCacheConfig(nearCacheConfig);
        config.addMapConfig(mapConfig);
        
        return config;
    }
}
```

**Near Cache Benefits:**

```
┌──────────────────────────────────────────────────────────────┐
│                  Near Cache Benefits                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  WITHOUT Near Cache:                                         │
│  ┌─────────┐                         ┌──────────┐            │
│  │   App   │ ──── get(key) ────────> │ Cluster  │            │
│  │         │ <─── value ───────────  │ (remote) │            │
│  └─────────┘                         └──────────┘            │
│                                                               │
│  Latency: 1-5ms (network call)                              │
│                                                               │
│  WITH Near Cache:                                            │
│  ┌─────────┐                                                 │
│  │   App   │                                                 │
│  │ ┌─────┐ │ ──── get(key) ───> Local cache hit             │
│  │ │Near │ │ <─── value ────── (no network)                 │
│  │ │Cache│ │                                                 │
│  │ └─────┘ │                                                 │
│  └─────────┘                                                 │
│                                                               │
│  Latency: <0.1ms (local memory)                             │
│  Throughput: 10-100x improvement                             │
│                                                               │
│  Best For:                                                   │
│  ✅ Frequently read data                                     │
│  ✅ Read-heavy workloads                                     │
│  ✅ Data that doesn't change often                          │
│  ✅ Latency-sensitive operations                             │
│                                                               │
│  NOT For:                                                    │
│  ❌ Write-heavy workloads                                    │
│  ❌ Data that changes frequently                             │
│  ❌ Strong consistency required                              │
└──────────────────────────────────────────────────────────────┘
```

### Eviction Policies

**Eviction Configuration:**

```java
public class HazelcastEvictionConfig {
    
    /**
     * LRU (Least Recently Used) - Default
     */
    public MapConfig lruEviction() {
        MapConfig mapConfig = new MapConfig("cache");
        
        EvictionConfig evictionConfig = new EvictionConfig();
        evictionConfig.setEvictionPolicy(EvictionPolicy.LRU);
        evictionConfig.setMaxSizePolicy(MaxSizePolicy.PER_NODE);
        evictionConfig.setSize(10000);
        
        mapConfig.setEvictionConfig(evictionConfig);
        
        return mapConfig;
    }
    
    /**
     * LFU (Least Frequently Used)
     */
    public MapConfig lfuEviction() {
        MapConfig mapConfig = new MapConfig("cache");
        
        EvictionConfig evictionConfig = new EvictionConfig();
        evictionConfig.setEvictionPolicy(EvictionPolicy.LFU);
        evictionConfig.setMaxSizePolicy(MaxSizePolicy.PER_NODE);
        evictionConfig.setSize(10000);
        
        mapConfig.setEvictionConfig(evictionConfig);
        
        return mapConfig;
    }
    
    /**
     * RANDOM eviction
     */
    public MapConfig randomEviction() {
        MapConfig mapConfig = new MapConfig("cache");
        
        EvictionConfig evictionConfig = new EvictionConfig();
        evictionConfig.setEvictionPolicy(EvictionPolicy.RANDOM);
        evictionConfig.setMaxSizePolicy(MaxSizePolicy.PER_NODE);
        evictionConfig.setSize(10000);
        
        mapConfig.setEvictionConfig(evictionConfig);
        
        return mapConfig;
    }
    
    /**
     * NONE (no eviction)
     */
    public MapConfig noEviction() {
        MapConfig mapConfig = new MapConfig("cache");
        
        EvictionConfig evictionConfig = new EvictionConfig();
        evictionConfig.setEvictionPolicy(EvictionPolicy.NONE);
        
        mapConfig.setEvictionConfig(evictionConfig);
        
        return mapConfig;
    }
}
```

**Eviction Policies Comparison:**

```
┌──────────────────────────────────────────────────────────────┐
│                  Eviction Policies                            │
├─────────────┬────────────────────────────────────────────────┤
│ LRU         │ Least Recently Used                            │
│ (Default)   │ Evicts entries not accessed recently          │
│             │ Best for: General purpose caching              │
│             │ Example: Evict user profiles not accessed     │
│             │          for 1 hour                            │
├─────────────┼────────────────────────────────────────────────┤
│ LFU         │ Least Frequently Used                          │
│             │ Evicts entries accessed least often           │
│             │ Best for: Hot data identification              │
│             │ Example: Keep frequently requested products    │
├─────────────┼────────────────────────────────────────────────┤
│ RANDOM      │ Random eviction                                │
│             │ Fastest, no tracking needed                    │
│             │ Best for: High throughput, don't care which   │
│             │          gets evicted                          │
├─────────────┼────────────────────────────────────────────────┤
│ NONE        │ No eviction                                    │
│             │ Cache grows unbounded                          │
│             │ Best for: Explicit cache management            │
│             │ Warning: Can cause OOM if not careful         │
└─────────────┴────────────────────────────────────────────────┘
```

### In-Memory Format

**Format Comparison:**

```java
public class InMemoryFormatConfig {
    
    /**
     * BINARY format (default)
     * - Stores data as byte array
     * - Serialization on put/get
     * - Lower memory (shared strings, etc)
     * - Higher CPU (serialization overhead)
     */
    public MapConfig binaryFormat() {
        MapConfig config = new MapConfig("users");
        config.setInMemoryFormat(InMemoryFormat.BINARY);
        return config;
    }
    
    /**
     * OBJECT format
     * - Stores Java objects directly
     * - No serialization overhead
     * - Higher memory (object overhead)
     * - Faster access
     */
    public MapConfig objectFormat() {
        MapConfig config = new MapConfig("users");
        config.setInMemoryFormat(InMemoryFormat.OBJECT);
        return config;
    }
    
    /**
     * NATIVE format (Enterprise only)
     * - Off-heap memory
     * - No GC pressure
     * - Best performance
     * - Requires Hazelcast Enterprise
     */
    public MapConfig nativeFormat() {
        MapConfig config = new MapConfig("users");
        config.setInMemoryFormat(InMemoryFormat.NATIVE);
        return config;
    }
}
```

### Cache Partitioning

**Partition-Aware Keys:**

```java
public class PartitionAwareKey implements PartitionAware<String> {
    
    private final String userId;
    private final String orderId;
    
    public PartitionAwareKey(String userId, String orderId) {
        this.userId = userId;
        this.orderId = orderId;
    }
    
    @Override
    public String getPartitionKey() {
        // All orders for same user go to same partition
        return userId;
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        
        PartitionAwareKey that = (PartitionAwareKey) o;
        
        return userId.equals(that.userId) && orderId.equals(that.orderId);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(userId, orderId);
    }
}

@Service
public class OrderService {
    
    private final HazelcastInstance hazelcastInstance;
    
    public void storeOrder(String userId, String orderId, Order order) {
        IMap<PartitionAwareKey, Order> orders = hazelcastInstance.getMap("orders");
        
        // All orders for same user stored in same partition
        PartitionAwareKey key = new PartitionAwareKey(userId, orderId);
        orders.put(key, order);
    }
    
    public List<Order> getUserOrders(String userId) {
        IMap<PartitionAwareKey, Order> orders = hazelcastInstance.getMap("orders");
        
        // Query all orders for user (efficient - same partition)
        return orders.values(Predicates.equal("userId", userId))
            .stream()
            .collect(Collectors.toList());
    }
}
```

### Performance Tuning

**Performance Optimization:**

```java
@Configuration
public class HazelcastPerformanceConfig {
    
    @Bean
    public Config performanceTunedConfig() {
        Config config = new Config();
        
        // Partition count (default 271)
        config.setProperty("hazelcast.partition.count", "271");
        
        // Operation thread count (default: core count)
        config.setProperty("hazelcast.operation.thread.count", "16");
        
        // IO thread count
        config.setProperty("hazelcast.io.thread.count", "8");
        
        // Map configuration
        MapConfig mapConfig = new MapConfig("cache");
        
        // Backup count (1 = one synchronous backup)
        mapConfig.setBackupCount(1);
        mapConfig.setAsyncBackupCount(0);
        
        // Read backup data (load balancing)
        mapConfig.setReadBackupData(true);
        
        // Statistics
        mapConfig.setStatisticsEnabled(true);
        
        // Indexes for queries
        mapConfig.addIndexConfig(new IndexConfig(IndexType.HASH, "userId"));
        
        config.addMapConfig(mapConfig);
        
        return config;
    }
}
```

---

## 4. Hazelcast Distributed Computing

### Executor Service for Distributed Tasks

**Distributed Task Execution:**

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class HazelcastExecutorService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Execute task on any member
     */
    public <T> Future<T> executeTask(Callable<T> task) {
        IExecutorService executor = hazelcastInstance.getExecutorService("default");
        
        return executor.submit(task);
    }
    
    /**
     * Execute on specific member
     */
    public <T> Future<T> executeOnMember(Callable<T> task, Member member) {
        IExecutorService executor = hazelcastInstance.getExecutorService("default");
        
        return executor.submitToMember(task, member);
    }
    
    /**
     * Execute on all members
     */
    public <T> Map<Member, Future<T>> executeOnAllMembers(Callable<T> task) {
        IExecutorService executor = hazelcastInstance.getExecutorService("default");
        
        return executor.submitToAllMembers(task);
    }
    
    /**
     * Execute on key owner (partition-aware)
     */
    public <T> Future<T> executeOnKeyOwner(Callable<T> task, Object key) {
        IExecutorService executor = hazelcastInstance.getExecutorService("default");
        
        return executor.submitToKeyOwner(task, key);
    }
    
    /**
     * Real-world example: Distributed report generation
     */
    public CompletableFuture<Report> generateDistributedReport(String reportId) {
        IExecutorService executor = hazelcastInstance.getExecutorService("reports");
        
        // Task to run on each member
        Callable<PartialReport> reportTask = () -> {
            // Each member processes its local data
            IMap<String, Data> localData = hazelcastInstance.getMap("data");
            
            return processLocalData(localData.localKeySet());
        };
        
        // Execute on all members
        Map<Member, Future<PartialReport>> futures = 
            executor.submitToAllMembers(reportTask);
        
        // Aggregate results
        return CompletableFuture.supplyAsync(() -> {
            List<PartialReport> partialReports = futures.values().stream()
                .map(future -> {
                    try {
                        return future.get();
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                })
                .collect(Collectors.toList());
            
            return aggregateReports(partialReports);
        });
    }
    
    private PartialReport processLocalData(Set<String> keys) {
        // Process local partition data
        return new PartialReport();
    }
    
    private Report aggregateReports(List<PartialReport> partialReports) {
        // Aggregate partial reports into final report
        return new Report();
    }
}
```

### Aggregations API

**Distributed Aggregations:**

```java
@Service
@RequiredArgsConstructor
public class HazelcastAggregationService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Count aggregation
     */
    public long countActiveUsers() {
        IMap<String, User> users = hazelcastInstance.getMap("users");
        
        return users.aggregate(
            Aggregators.count(),
            Predicates.equal("status", "ACTIVE")
        );
    }
    
    /**
     * Sum aggregation
     */
    public BigDecimal getTotalSales() {
        IMap<String, Order> orders = hazelcastInstance.getMap("orders");
        
        return orders.aggregate(
            Aggregators.bigDecimalSum("amount")
        );
    }
    
    /**
     * Average aggregation
     */
    public Double getAverageOrderValue() {
        IMap<String, Order> orders = hazelcastInstance.getMap("orders");
        
        return orders.aggregate(
            Aggregators.doubleAvg("amount")
        );
    }
    
    /**
     * Min/Max aggregation
     */
    public Order getHighestValueOrder() {
        IMap<String, Order> orders = hazelcastInstance.getMap("orders");
        
        return orders.aggregate(
            Aggregators.maxBy("amount")
        );
    }
    
    /**
     * Custom aggregation
     */
    public Map<String, Long> getUserCountByStatus() {
        IMap<String, User> users = hazelcastInstance.getMap("users");
        
        // Group by status and count
        return users.aggregate(
            Aggregators.groupingBy(
                User::getStatus,
                Aggregators.count()
            )
        );
    }
    
    /**
     * Complex aggregation with predicates
     */
    public OrderStatistics getOrderStatistics(LocalDate startDate, LocalDate endDate) {
        IMap<String, Order> orders = hazelcastInstance.getMap("orders");
        
        Predicate<String, Order> datePredicate = Predicates.between(
            "orderDate",
            startDate,
            endDate
        );
        
        long count = orders.aggregate(Aggregators.count(), datePredicate);
        BigDecimal total = orders.aggregate(Aggregators.bigDecimalSum("amount"), datePredicate);
        Double average = orders.aggregate(Aggregators.doubleAvg("amount"), datePredicate);
        
        return new OrderStatistics(count, total, average);
    }
}
```

### Entry Processors for Atomic Updates

**Atomic Entry Updates:**

```java
@Service
@RequiredArgsConstructor
public class HazelcastEntryProcessorService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Entry processor for atomic updates
     */
    public void updateBalance(String accountId, BigDecimal amount) {
        IMap<String, Account> accounts = hazelcastInstance.getMap("accounts");
        
        accounts.executeOnKey(accountId, new AddBalanceProcessor(amount));
    }
    
    /**
     * Entry processor on all entries
     */
    public void applyInterest(BigDecimal rate) {
        IMap<String, Account> accounts = hazelcastInstance.getMap("accounts");
        
        accounts.executeOnEntries(new InterestProcessor(rate));
    }
    
    /**
     * Entry processor with predicate
     */
    public void deactivateInactiveAccounts(int inactiveDays) {
        IMap<String, Account> accounts = hazelcastInstance.getMap("accounts");
        
        LocalDate cutoffDate = LocalDate.now().minusDays(inactiveDays);
        Predicate<String, Account> predicate = 
            Predicates.lessThan("lastActivity", cutoffDate);
        
        accounts.executeOnEntries(
            new DeactivateAccountProcessor(),
            predicate
        );
    }
}

/**
 * Entry processor for adding balance
 */
public class AddBalanceProcessor implements EntryProcessor<String, Account, BigDecimal> {
    
    private final BigDecimal amount;
    
    public AddBalanceProcessor(BigDecimal amount) {
        this.amount = amount;
    }
    
    @Override
    public BigDecimal process(Map.Entry<String, Account> entry) {
        Account account = entry.getValue();
        
        if (account == null) {
            return BigDecimal.ZERO;
        }
        
        BigDecimal newBalance = account.getBalance().add(amount);
        account.setBalance(newBalance);
        
        entry.setValue(account);
        
        return newBalance;
    }
}

/**
 * Entry processor for applying interest
 */
public class InterestProcessor implements EntryProcessor<String, Account, Void> {
    
    private final BigDecimal rate;
    
    public InterestProcessor(BigDecimal rate) {
        this.rate = rate;
    }
    
    @Override
    public Void process(Map.Entry<String, Account> entry) {
        Account account = entry.getValue();
        
        if (account != null && "ACTIVE".equals(account.getStatus())) {
            BigDecimal interest = account.getBalance().multiply(rate);
            account.setBalance(account.getBalance().add(interest));
            
            entry.setValue(account);
        }
        
        return null;
    }
}
```

### Distributed Queries and Predicates

**Query with Predicates:**

```java
@Service
@RequiredArgsConstructor
public class HazelcastQueryService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Simple equality query
     */
    public Collection<User> findActiveUsers() {
        IMap<String, User> users = hazelcastInstance.getMap("users");
        
        return users.values(Predicates.equal("status", "ACTIVE"));
    }
    
    /**
     * Range query
     */
    public Collection<Order> findOrdersInRange(BigDecimal min, BigDecimal max) {
        IMap<String, Order> orders = hazelcastInstance.getMap("orders");
        
        return orders.values(Predicates.between("amount", min, max));
    }
    
    /**
     * Complex query with AND/OR
     */
    public Collection<User> findPremiumUsersInCity(String city) {
        IMap<String, User> users = hazelcastInstance.getMap("users");
        
        Predicate<String, User> predicate = Predicates.and(
            Predicates.equal("city", city),
            Predicates.equal("tier", "PREMIUM"),
            Predicates.equal("status", "ACTIVE")
        );
        
        return users.values(predicate);
    }
    
    /**
     * LIKE query
     */
    public Collection<User> findUsersByEmailDomain(String domain) {
        IMap<String, User> users = hazelcastInstance.getMap("users");
        
        return users.values(Predicates.like("email", "%" + domain));
    }
    
    /**
     * IN query
     */
    public Collection<Order> findOrdersByStatus(List<String> statuses) {
        IMap<String, Order> orders = hazelcastInstance.getMap("orders");
        
        return orders.values(Predicates.in("status", statuses.toArray(new String[0])));
    }
    
    /**
     * Paging query
     */
    public PagingResult<User> findUsersWithPaging(int page, int pageSize) {
        IMap<String, User> users = hazelcastInstance.getMap("users");
        
        PagingPredicate<String, User> pagingPredicate = 
            Predicates.pagingPredicate(pageSize);
        
        pagingPredicate.setPage(page);
        
        Collection<User> results = users.values(pagingPredicate);
        
        return new PagingResult<>(
            results,
            page,
            pageSize,
            users.size()
        );
    }
    
    /**
     * Sorted query
     */
    public Collection<Order> findRecentOrders(int limit) {
        IMap<String, Order> orders = hazelcastInstance.getMap("orders");
        
        // Sort by date descending
        Comparator<Map.Entry<String, Order>> comparator = 
            (e1, e2) -> e2.getValue().getOrderDate()
                .compareTo(e1.getValue().getOrderDate());
        
        PagingPredicate<String, Order> pagingPredicate = 
            Predicates.pagingPredicate(comparator, limit);
        
        return orders.values(pagingPredicate);
    }
}
```

### Real-World Use Cases

**Production Use Cases:**

```java
@Service
@RequiredArgsConstructor
public class HazelcastRealWorldUseCases {
    
    private final HazelcastInstance hazelcastInstance;
    private final IExecutorService executorService;
    
    /**
     * Use Case 1: Distributed batch processing
     * Process large dataset across cluster
     */
    public void processBatchRecords(List<Record> records) {
        IMap<String, Record> recordMap = hazelcastInstance.getMap("records");
        
        // Distribute records across cluster
        records.forEach(record -> 
            recordMap.put(record.getId(), record));
        
        // Process on each member (parallel)
        Map<Member, Future<Integer>> futures = executorService.submitToAllMembers(() -> {
            IMap<String, Record> localRecords = hazelcastInstance.getMap("records");
            int processed = 0;
            
            for (String key : localRecords.localKeySet()) {
                processRecord(localRecords.get(key));
                processed++;
            }
            
            return processed;
        });
        
        // Aggregate results
        int totalProcessed = futures.values().stream()
            .mapToInt(future -> {
                try {
                    return future.get();
                } catch (Exception e) {
                    return 0;
                }
            })
            .sum();
    }
    
    /**
     * Use Case 2: Real-time leaderboard
     */
    public void updateLeaderboard(String userId, int score) {
        IMap<String, Integer> leaderboard = hazelcastInstance.getMap("leaderboard");
        
        // Atomic update
        leaderboard.executeOnKey(userId, entry -> {
            Integer currentScore = entry.getValue();
            if (currentScore == null || score > currentScore) {
                entry.setValue(score);
            }
            return entry.getValue();
        });
    }
    
    public List<LeaderboardEntry> getTopPlayers(int limit) {
        IMap<String, Integer> leaderboard = hazelcastInstance.getMap("leaderboard");
        
        return leaderboard.entrySet().stream()
            .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
            .limit(limit)
            .map(entry -> new LeaderboardEntry(entry.getKey(), entry.getValue()))
            .collect(Collectors.toList());
    }
    
    /**
     * Use Case 3: Distributed rate limiting
     */
    public boolean checkRateLimit(String userId, int maxRequests, int windowSeconds) {
        String key = "rate_limit:" + userId;
        IMap<String, RateLimitData> rateLimits = hazelcastInstance.getMap("rate_limits");
        
        return rateLimits.executeOnKey(key, entry -> {
            RateLimitData data = entry.getValue();
            long now = System.currentTimeMillis();
            
            if (data == null) {
                data = new RateLimitData(1, now);
                entry.setValue(data);
                return true;
            }
            
            long windowStart = now - (windowSeconds * 1000L);
            if (data.getTimestamp() < windowStart) {
                // Reset window
                data = new RateLimitData(1, now);
                entry.setValue(data);
                return true;
            }
            
            if (data.getCount() < maxRequests) {
                data.incrementCount();
                entry.setValue(data);
                return true;
            }
            
            return false;
        });
    }
    
    private void processRecord(Record record) {
        // Processing logic
    }
}
```

---

## 5. Hazelcast Production Considerations

### WAN Replication for Disaster Recovery

**Cross-Datacenter Replication:**

```java
@Configuration
public class HazelcastWANConfig {
    
    @Bean
    public Config hazelcastConfigWithWAN() {
        Config config = new Config();
        
        // WAN replication configuration
        WanReplicationConfig wanConfig = new WanReplicationConfig();
        wanConfig.setName("my-wan-cluster");
        
        // Target cluster configuration
        WanBatchPublisherConfig publisherConfig = new WanBatchPublisherConfig();
        publisherConfig.setClusterName("backup-cluster");
        publisherConfig.setTargetEndpoints("backup-dc.example.com:5701,backup-dc.example.com:5702");
        
        // Batch configuration
        publisherConfig.setBatchSize(500);
        publisherConfig.setBatchMaxDelayMillis(1000);
        publisherConfig.setResponseTimeoutMillis(60000);
        publisherConfig.setAcknowledgeType(WanAcknowledgeType.ACK_ON_OPERATION_COMPLETE);
        
        wanConfig.addBatchReplicationPublisherConfig(publisherConfig);
        config.addWanReplicationConfig(wanConfig);
        
        // Map with WAN replication
        MapConfig mapConfig = new MapConfig("users");
        mapConfig.setWanReplicationRef(new WanReplicationRef(
            "my-wan-cluster",
            "com.hazelcast.enterprise.wan.replication.WanNoDelayReplication",
            Collections.emptyList(),
            false
        ));
        
        config.addMapConfig(mapConfig);
        
        return config;
    }
}
```

### Split-Brain Protection

**Split-Brain Configuration:**

```java
@Configuration
public class HazelcastSplitBrainConfig {
    
    @Bean
    public Config hazelcastConfigWithSplitBrainProtection() {
        Config config = new Config();
        
        // Split-brain protection (quorum)
        SplitBrainProtectionConfig splitBrainConfig = 
            new SplitBrainProtectionConfig();
        splitBrainConfig.setName("split-brain-protection");
        splitBrainConfig.setEnabled(true);
        splitBrainConfig.setMinimumClusterSize(3);  // Minimum 3 members
        splitBrainConfig.setProtectOn(SplitBrainProtectionOn.READ_WRITE);
        
        config.addSplitBrainProtectionConfig(splitBrainConfig);
        
        // Map with split-brain protection
        MapConfig mapConfig = new MapConfig("critical-data");
        mapConfig.setSplitBrainProtectionName("split-brain-protection");
        
        config.addMapConfig(mapConfig);
        
        return config;
    }
}
```

### Cluster Monitoring and Management

**Management Center & Metrics:**

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class HazelcastMonitoringService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Get cluster statistics
     */
    @Scheduled(fixedRate = 60000)  // Every minute
    public void monitorCluster() {
        Cluster cluster = hazelcastInstance.getCluster();
        
        log.info("Cluster size: {}", cluster.getMembers().size());
        log.info("Cluster state: {}", cluster.getClusterState());
        
        // Member info
        cluster.getMembers().forEach(member -> {
            log.info("Member: {} - {}", member.getUuid(), member.getAddress());
        });
    }
    
    /**
     * Monitor map statistics
     */
    public void monitorMapStats(String mapName) {
        IMap<?, ?> map = hazelcastInstance.getMap(mapName);
        
        LocalMapStats stats = map.getLocalMapStats();
        
        log.info("Map {} statistics:", mapName);
        log.info("  Size: {}", stats.getOwnedEntryCount());
        log.info("  Backup size: {}", stats.getBackupEntryCount());
        log.info("  Hits: {}", stats.getHits());
        log.info("  Get operations: {}", stats.getGetOperationCount());
        log.info("  Put operations: {}", stats.getPutOperationCount());
        log.info("  Memory cost: {} bytes", stats.getOwnedEntryMemoryCost());
    }
    
    /**
     * Health check
     */
    public boolean isHealthy() {
        try {
            Cluster cluster = hazelcastInstance.getCluster();
            
            // Check cluster size
            int memberCount = cluster.getMembers().size();
            if (memberCount < 2) {
                log.warn("Cluster size below minimum: {}", memberCount);
                return false;
            }
            
            // Check cluster state
            ClusterState state = cluster.getClusterState();
            if (state != ClusterState.ACTIVE) {
                log.warn("Cluster not active: {}", state);
                return false;
            }
            
            return true;
            
        } catch (Exception e) {
            log.error("Health check failed", e);
            return false;
        }
    }
}
```

### Persistence with MapStore/MapLoader

**MapStore Implementation:**

```java
@Component
public class UserMapStore implements MapStore<String, User> {
    
    private final UserRepository userRepository;
    
    public UserMapStore(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    @Override
    public void store(String key, User value) {
        // Write to database
        userRepository.save(value);
    }
    
    @Override
    public void storeAll(Map<String, User> map) {
        // Batch write
        userRepository.saveAll(map.values());
    }
    
    @Override
    public void delete(String key) {
        userRepository.deleteById(key);
    }
    
    @Override
    public void deleteAll(Collection<String> keys) {
        userRepository.deleteAllById(keys);
    }
    
    @Override
    public User load(String key) {
        // Read from database on cache miss
        return userRepository.findById(key).orElse(null);
    }
    
    @Override
    public Map<String, User> loadAll(Collection<String> keys) {
        return userRepository.findAllById(keys).stream()
            .collect(Collectors.toMap(User::getId, u -> u));
    }
    
    @Override
    public Iterable<String> loadAllKeys() {
        return userRepository.findAllIds();
    }
}

@Configuration
public class MapStoreConfig {
    
    @Bean
    public Config hazelcastConfigWithMapStore(UserMapStore userMapStore) {
        Config config = new Config();
        
        MapConfig mapConfig = new MapConfig("users");
        
        // MapStore configuration
        MapStoreConfig mapStoreConfig = new MapStoreConfig();
        mapStoreConfig.setImplementation(userMapStore);
        mapStoreConfig.setWriteDelaySeconds(5);  // Batch writes every 5 seconds
        mapStoreConfig.setWriteBatchSize(100);    // Max 100 per batch
        mapStoreConfig.setWriteCoalescing(true);  // Merge multiple updates
        
        // Write-through vs write-behind
        mapStoreConfig.setWriteThrough(false);  // Write-behind (async)
        
        mapConfig.setMapStoreConfig(mapStoreConfig);
        config.addMapConfig(mapConfig);
        
        return config;
    }
}
```

### Security Configuration

**Authentication & Authorization:**

```java
@Configuration
public class HazelcastSecurityConfig {
    
    @Bean
    public Config hazelcastSecureConfig() {
        Config config = new Config();
        
        // Security configuration
        SecurityConfig securityConfig = config.getSecurityConfig();
        securityConfig.setEnabled(true);
        
        // Member authentication
        RealmConfig memberRealmConfig = new RealmConfig()
            .setUsernamePasswordIdentityConfig(
                "admin",
                "admin-password"
            );
        
        securityConfig.setMemberRealmConfig("memberRealm", memberRealmConfig);
        
        // Client authentication
        RealmConfig clientRealmConfig = new RealmConfig()
            .setUsernamePasswordIdentityConfig(
                "client",
                "client-password"
            );
        
        securityConfig.setClientRealmConfig("clientRealm", clientRealmConfig);
        
        // SSL/TLS configuration
        SSLConfig sslConfig = new SSLConfig();
        sslConfig.setEnabled(true);
        sslConfig.setProperty("keyStore", "/path/to/keystore.jks");
        sslConfig.setProperty("keyStorePassword", "keystore-password");
        sslConfig.setProperty("trustStore", "/path/to/truststore.jks");
        sslConfig.setProperty("trustStorePassword", "truststore-password");
        
        config.getNetworkConfig().setSSLConfig(sslConfig);
        
        // Permissions
        PermissionConfig mapPermission = new PermissionConfig(
            PermissionType.MAP,
            "users",
            "admin"
        );
        mapPermission.addAction("create").addAction("destroy")
            .addAction("put").addAction("read");
        
        securityConfig.addClientPermissionConfig(mapPermission);
        
        return config;
    }
}
```

### Performance Benchmarking

**Benchmark Service:**

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class HazelcastBenchmarkService {
    
    private final HazelcastInstance hazelcastInstance;
    
    /**
     * Benchmark write performance
     */
    public void benchmarkWrites(int operationCount) {
        IMap<String, String> testMap = hazelcastInstance.getMap("benchmark");
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < operationCount; i++) {
            testMap.put("key-" + i, "value-" + i);
        }
        
        long duration = System.currentTimeMillis() - startTime;
        double opsPerSecond = (double) operationCount / duration * 1000;
        
        log.info("Write benchmark: {} ops in {}ms ({} ops/sec)",
            operationCount, duration, String.format("%.2f", opsPerSecond));
        
        testMap.clear();
    }
    
    /**
     * Benchmark read performance
     */
    public void benchmarkReads(int operationCount) {
        IMap<String, String> testMap = hazelcastInstance.getMap("benchmark");
        
        // Pre-populate
        for (int i = 0; i < operationCount; i++) {
            testMap.put("key-" + i, "value-" + i);
        }
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < operationCount; i++) {
            testMap.get("key-" + i);
        }
        
        long duration = System.currentTimeMillis() - startTime;
        double opsPerSecond = (double) operationCount / duration * 1000;
        
        log.info("Read benchmark: {} ops in {}ms ({} ops/sec)",
            operationCount, duration, String.format("%.2f", opsPerSecond));
        
        testMap.clear();
    }
    
    /**
     * Benchmark with near cache
     */
    public void benchmarkWithNearCache(int operationCount) {
        // Configure near cache
        Config config = new Config();
        MapConfig mapConfig = new MapConfig("benchmark-near");
        
        NearCacheConfig nearCacheConfig = new NearCacheConfig();
        nearCacheConfig.setInMemoryFormat(InMemoryFormat.OBJECT);
        
        mapConfig.setNearCacheConfig(nearCacheConfig);
        config.addMapConfig(mapConfig);
        
        IMap<String, String> testMap = hazelcastInstance.getMap("benchmark-near");
        
        // Pre-populate
        for (int i = 0; i < operationCount; i++) {
            testMap.put("key-" + i, "value-" + i);
        }
        
        // First read (populate near cache)
        for (int i = 0; i < operationCount; i++) {
            testMap.get("key-" + i);
        }
        
        // Second read (from near cache)
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < operationCount; i++) {
            testMap.get("key-" + i);
        }
        
        long duration = System.currentTimeMillis() - startTime;
        double opsPerSecond = (double) operationCount / duration * 1000;
        
        log.info("Near cache benchmark: {} ops in {}ms ({} ops/sec)",
            operationCount, duration, String.format("%.2f", opsPerSecond));
        
        testMap.clear();
    }
}
```

---

## Best Practices Summary

### ✅ DO:

1. **Use embedded mode** for microservices and simple deployments
2. **Configure backups** (minimum 1 sync backup for production)
3. **Enable near cache** for read-heavy workloads
4. **Use partition-aware keys** for related data locality
5. **Implement MapStore** for persistence and cache-aside pattern
6. **Monitor cluster** health and metrics continuously
7. **Use entry processors** for atomic multi-step updates
8. **Configure split-brain** protection (quorum) for critical data
9. **Enable WAN replication** for disaster recovery
10. **Use ILock** for distributed coordination

### ❌ DON'T:

1. **Don't store large objects** (>1MB) in maps
2. **Don't use default** serialization (configure efficiently)
3. **Don't skip backup** configuration (data loss risk)
4. **Don't ignore partition** distribution (hot partitions)
5. **Don't use blocking** operations in critical paths
6. **Don't forget TTL** for temporary data
7. **Don't mix concerns** in single map
8. **Don't skip security** configuration in production
9. **Don't ignore cluster** size requirements (min 3 for quorum)
10. **Don't use Hazelcast** as primary database (cache only)

---

## Interview Questions

**Q1: What is the difference between Hazelcast and Redis?**

Hazelcast: Multi-threaded, distributed computing platform, embedded in application (no separate server), automatic partitioning and replication, supports distributed data structures (IMap, IQueue, ILock), built-in cluster management, Java-native, supports distributed computing (executor service, aggregations). Redis: Single-threaded, cache-focused, separate server process, client-server architecture, simple data structures (strings, lists, sets), Lua scripts for atomic operations, faster for simple operations. Use Hazelcast for: distributed computing, embedded cache, Java apps, complex operations. Use Redis for: simple caching, high-throughput key-value, polyglot environments, pub/sub messaging.

**Q2: Explain embedded mode vs client-server mode in Hazelcast.**

Embedded mode: Hazelcast runs IN application JVM, data stored in app memory, no separate server, lower latency (local access), simpler deployment, couples data lifecycle to app, higher memory per app. Client-server mode: Separate Hazelcast cluster, apps connect as clients, independent data tier, app restarts don't affect data, better resource isolation, network overhead, more complex deployment. Use embedded for: microservices, small datasets, co-located data/compute. Use client-server for: production, large datasets, independent scaling, separate data layer. Embedded typical for 2-10 nodes, client-server for larger clusters.

**Q3: What is near cache and when should you use it?**

Near cache: Local cache on client/member storing frequently accessed data. Reads from local memory (no network), <0.1ms latency vs 1-5ms for remote, 10-100x throughput improvement. Configuration: in-memory format (BINARY, OBJECT), TTL (time to live), max idle time, eviction policy (LRU), invalidation (on change). Use for: frequently read data, read-heavy workloads, data that doesn't change often, latency-sensitive operations. Don't use for: write-heavy, frequently changing data, strong consistency needs. Example: user profiles, product catalogs, configuration data. Near cache hit rate >80% = effective. Monitor hit rate and adjust size/TTL.

**Q4: How do you implement distributed locking with Hazelcast?**

Use ILock for distributed locking across cluster. Basic: ILock lock = hazelcastInstance.getLock("resource"); lock.lock(); try { /* critical section */ } finally { lock.unlock(); }. With timeout: lock.tryLock(timeout, TimeUnit). Features: Reentrant (same thread can acquire multiple times), automatic unlock on member failure, fair ordering optional. Use cases: prevent duplicate processing, leader election, singleton tasks, coordinated updates. Example: Only one instance processes scheduled job - if (lock.tryLock()) { processJob(); lock.unlock(); }. Alternative: Entry processor for map-specific atomic operations. Important: Always unlock in finally block, use timeout to prevent deadlocks.

**Q5: What are the key production considerations for Hazelcast?**

Critical considerations: (1) Backup configuration - minimum 1 sync backup, avoid data loss. (2) Split-brain protection - quorum config, prevents inconsistency during network partition. (3) Cluster size - minimum 3 members for quorum, odd number preferred. (4) Partition distribution - monitor for hot partitions, use partition-aware keys. (5) WAN replication - cross-datacenter for DR, async replication. (6) Persistence - MapStore for write-through/write-behind to database. (7) Security - authentication, SSL/TLS, permissions. (8) Monitoring - Management Center, metrics, health checks. (9) Memory management - eviction policies, TTL, heap sizing. (10) Network configuration - discovery mechanism, timeouts, connection limits. Test failover scenarios regularly.

---

## Summary

Hazelcast with Spring Boot:

- ✅ **Setup** - Embedded (in-app) or client-server mode, multiple discovery mechanisms
- ✅ **Data Structures** - IMap (cache), IQueue (queue), ISet/IList, ITopic (pub/sub), ILock (locking)
- ✅ **Caching** - Spring Cache integration, near cache, eviction policies, in-memory formats
- ✅ **Computing** - Executor service, aggregations, entry processors, distributed queries
- ✅ **Production** - WAN replication, split-brain protection, MapStore persistence, security

**Key Takeaway**: Hazelcast = distributed in-memory data grid + computing platform. Unlike Redis (single-threaded cache), Hazelcast is multi-threaded and designed for embedded deployment with automatic clustering. Use embedded mode for microservices (data co-located with compute), client-server for separate data tier. Near cache provides local caching (<0.1ms reads). IMap for distributed cache with backups. IQueue for distributed queues. ILock for coordination. Entry processors for atomic updates. Configure backups (min 1), split-brain protection (quorum), and WAN replication (DR). MapStore for persistence. Ideal for: distributed caching, session replication, distributed locks, in-memory computing, real-time applications.