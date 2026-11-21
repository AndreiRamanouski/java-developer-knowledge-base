# Databases

PostgreSQL, MySQL and Oracle with Spring Boot, Liquibase and Flyway migrations, and NoSQL stores.

[← Back to the main README](../README.md)

## Contents

<!-- toc:start -->
### [1. SQL Databases](1.%20SQL%20Databases)

- **[1. PostgreSQL](1.%20SQL%20Databases/1.%20PostgreSQL)**
  - [1. PostgreSQL-specific features in Spring Data JPA](1.%20SQL%20Databases/1.%20PostgreSQL/1.%20PostgreSQL-specific%20features%20in%20Spring%20Data%20JPA.md)
  - [2. Connection pooling - HikariCP configuration](1.%20SQL%20Databases/1.%20PostgreSQL/2.%20Connection%20pooling%20-%20HikariCP%20configuration.md)
  - [3. Transaction isolation levels in PostgreSQL](1.%20SQL%20Databases/1.%20PostgreSQL/3.%20Transaction%20isolation%20levels%20in%20PostgreSQL.md)
  - [4. N+1 query problem and solutions](1.%20SQL%20Databases/1.%20PostgreSQL/4.%20N%2B1%20query%20problem%20and%20solutions.md)
  - [5. Database indexing strategies](1.%20SQL%20Databases/1.%20PostgreSQL/5.%20Database%20indexing%20strategies.md)
  - [6. Handling database schema evolution in production](1.%20SQL%20Databases/1.%20PostgreSQL/6.%20Handling%20database%20schema%20evolution%20in%20production.md)
  - **[Interview follow-ups](1.%20SQL%20Databases/1.%20PostgreSQL/Interview%20follow-ups)**
    - [1. PostgreSQL-specific features in Spring Data JPA](1.%20SQL%20Databases/1.%20PostgreSQL/Interview%20follow-ups/1.%20PostgreSQL-specific%20features%20in%20Spring%20Data%20JPA.md)
    - [2. Connection pooling - HikariCP configuration (Q1-Q4)](1.%20SQL%20Databases/1.%20PostgreSQL/Interview%20follow-ups/2.%20Connection%20pooling%20-%20HikariCP%20configuration%20%28Q1-Q4%29.md)
    - [2. Connection pooling - HikariCP configuration (Q5-Q8)](1.%20SQL%20Databases/1.%20PostgreSQL/Interview%20follow-ups/2.%20Connection%20pooling%20-%20HikariCP%20configuration%20%28Q5-Q8%29.md)
    - [3. Transaction isolation levels in PostgreSQL (Q1-Q4)](1.%20SQL%20Databases/1.%20PostgreSQL/Interview%20follow-ups/3.%20Transaction%20isolation%20levels%20in%20PostgreSQL%20%28Q1-Q4%29.md)
    - [3. Transaction isolation levels in PostgreSQL (Q5-Q8)](1.%20SQL%20Databases/1.%20PostgreSQL/Interview%20follow-ups/3.%20Transaction%20isolation%20levels%20in%20PostgreSQL%20%28Q5-Q8%29.md)
    - [4. N+1 query problem and solutions](1.%20SQL%20Databases/1.%20PostgreSQL/Interview%20follow-ups/4.%20N%2B1%20query%20problem%20and%20solutions.md)
- **[2. MySQL](1.%20SQL%20Databases/2.%20MySQL)**
  - [1. MySQL vs PostgreSQL](1.%20SQL%20Databases/2.%20MySQL/1.%20MySQL%20vs%20PostgreSQL.md)
  - [2. MySQL-specific optimizations](1.%20SQL%20Databases/2.%20MySQL/2.%20MySQL-specific%20optimizations.md)
  - [3. Replication and read replicas with Spring Boot](1.%20SQL%20Databases/2.%20MySQL/3.%20Replication%20and%20read%20replicas%20with%20Spring%20Boot.md)
  - [4. Character sets and collations](1.%20SQL%20Databases/2.%20MySQL/4.%20Character%20sets%20and%20collations.md)
  - [5. MySQL locking mechanisms](1.%20SQL%20Databases/2.%20MySQL/5.%20MySQL%20locking%20mechanisms.md)
- **[3. Oracle](1.%20SQL%20Databases/3.%20Oracle)**
  - [1. Oracle-specific configuration in Spring Boot](1.%20SQL%20Databases/3.%20Oracle/1.%20Oracle-specific%20configuration%20in%20Spring%20Boot.md)
  - [2. Sequences and identity columns](1.%20SQL%20Databases/3.%20Oracle/2.%20Sequences%20and%20identity%20columns.md)
  - [3. Oracle PL-SQL integration](1.%20SQL%20Databases/3.%20Oracle/3.%20Oracle%20PL-SQL%20integration.md)
  - [4. Partitioning strategies in Oracle](1.%20SQL%20Databases/3.%20Oracle/4.%20Partitioning%20strategies%20in%20Oracle.md)

### [2. Database Migrations](2.%20Database%20Migrations)

- **[1. Liquibase](2.%20Database%20Migrations/1.%20Liquibase)**
  - [1. Liquibase fundamentals and setup](2.%20Database%20Migrations/1.%20Liquibase/1.%20Liquibase%20fundamentals%20and%20setup.md)
  - [2. Liquibase changelog organization](2.%20Database%20Migrations/1.%20Liquibase/2.%20Liquibase%20changelog%20organization.md)
  - [3. Advanced Liquibase features](2.%20Database%20Migrations/1.%20Liquibase/3.%20Advanced%20Liquibase%20features.md)
  - [4. Liquibase in production environments](2.%20Database%20Migrations/1.%20Liquibase/4.%20Liquibase%20in%20production%20environments.md)
  - [5. Testing database migrations](2.%20Database%20Migrations/1.%20Liquibase/5.%20Testing%20database%20migrations.md)
  - [6. Liquibase vs code-first approaches](2.%20Database%20Migrations/1.%20Liquibase/6.%20Liquibase%20vs%20code-first%20approaches.md)
- **[2. Flyway](2.%20Database%20Migrations/2.%20Flyway)**
  - [1. Flyway fundamentals and setup](2.%20Database%20Migrations/2.%20Flyway/1.%20Flyway%20fundamentals%20and%20setup.md)
  - [2. Flyway migration patterns](2.%20Database%20Migrations/2.%20Flyway/2.%20Flyway%20migration%20patterns.md)
  - [3. Flyway in microservices architecture](2.%20Database%20Migrations/2.%20Flyway/3.%20Flyway%20in%20microservices%20architecture.md)
  - [4. Flyway production strategies](2.%20Database%20Migrations/2.%20Flyway/4.%20Flyway%20production%20strategies.md)
  - [5. Testing Flyway migrations](2.%20Database%20Migrations/2.%20Flyway/5.%20Testing%20Flyway%20migrations.md)
  - [6. Flyway vs Liquibase comparison](2.%20Database%20Migrations/2.%20Flyway/6.%20Flyway%20vs%20Liquibase%20comparison.md)

### [3. NoSQL](3.%20NoSQL)

- **[1. MongoDB](3.%20NoSQL/1.%20MongoDB)**
  - [1. Spring Data MongoDB setup and configuration](3.%20NoSQL/1.%20MongoDB/1.%20Spring%20Data%20MongoDB%20setup%20and%20configuration.md)
  - [2. Document modeling patterns](3.%20NoSQL/1.%20MongoDB/2.%20Document%20modeling%20patterns.md)
  - [3. Querying MongoDB in Spring](3.%20NoSQL/1.%20MongoDB/3.%20Querying%20MongoDB%20in%20Spring.md)
  - [4. MongoDB indexing and performance](3.%20NoSQL/1.%20MongoDB/4.%20MongoDB%20indexing%20and%20performance.md)
  - [5. Transactions in MongoDB](3.%20NoSQL/1.%20MongoDB/5.%20Transactions%20in%20MongoDB.md)
  - [6. MongoDB change streams](3.%20NoSQL/1.%20MongoDB/6.%20MongoDB%20change%20streams.md)
  - [7. MongoDB testing strategies](3.%20NoSQL/1.%20MongoDB/7.%20MongoDB%20testing%20strategies.md)
- **[2. Redis](3.%20NoSQL/2.%20Redis)**
  - [1. Spring Data Redis setup](3.%20NoSQL/2.%20Redis/1.%20Spring%20Data%20Redis%20setup.md)
  - [2. Redis as a cache](3.%20NoSQL/2.%20Redis/2.%20Redis%20as%20a%20cache.md)
  - [3. Redis data structures in Spring](3.%20NoSQL/2.%20Redis/3.%20Redis%20data%20structures%20in%20Spring.md)
  - [4. Redis as a session store](3.%20NoSQL/2.%20Redis/4.%20Redis%20as%20a%20session%20store.md)
  - [5. Redis pub-sub messaging](3.%20NoSQL/2.%20Redis/5.%20Redis%20pub-sub%20messaging.md)
  - [6. Redis persistence and high availability](3.%20NoSQL/2.%20Redis/6.%20Redis%20persistence%20and%20high%20availability.md)
  - [7. Redis performance optimization](3.%20NoSQL/2.%20Redis/7.%20Redis%20performance%20optimization.md)
- **[3. Hazelcast](3.%20NoSQL/3.%20Hazelcast)**
  - [Hazelcast](3.%20NoSQL/3.%20Hazelcast/Hazelcast.md)
- **[4. DynamoDB](3.%20NoSQL/4.%20DynamoDB)**
  - [1. DynamoDB setup with Spring Boot](3.%20NoSQL/4.%20DynamoDB/1.%20DynamoDB%20setup%20with%20Spring%20Boot.md)
  - [2. Data modeling fundamentals](3.%20NoSQL/4.%20DynamoDB/2.%20Data%20modeling%20fundamentals.md)
  - [3. CRUD operations and queries](3.%20NoSQL/4.%20DynamoDB/3.%20CRUD%20operations%20and%20queries.md)
  - [4. Indexes (GSI and LSI)](3.%20NoSQL/4.%20DynamoDB/4.%20Indexes%20%28GSI%20and%20LSI%29.md)
  - [5. Capacity modes and performance](3.%20NoSQL/4.%20DynamoDB/5.%20Capacity%20modes%20and%20performance.md)
  - [6. Advanced features](3.%20NoSQL/4.%20DynamoDB/6.%20Advanced%20features.md)
  - [7. Best practices and anti-patterns](3.%20NoSQL/4.%20DynamoDB/7.%20Best%20practices%20and%20anti-patterns.md)
<!-- toc:end -->
