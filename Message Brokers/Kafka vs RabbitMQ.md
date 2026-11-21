# Kafka vs RabbitMQ

> **Applies to:** Apache Kafka 3.x–4.x · RabbitMQ 3.13–4.x · Spring Boot 3.x · **Last updated:** 2026-11-21

## Overview

Both are mature, widely used and well supported by Spring. They're built on different models, and that model — not raw speed — should drive the choice:

- **Kafka** is a distributed **log**. Records are retained, consumers track their own position, and many consumer groups can read (and re-read) the same data.
- **RabbitMQ** is a **message broker**. The broker routes messages into queues and deletes them once consumed; it's optimized for flexible routing and per-message handling.

**Key Concept**: Ask "do consumers need the *history* of events, or just the *next task*?" History, replay and many independent readers point to Kafka. Task distribution, routing rules and per-message control point to RabbitMQ.

---

## 1. Side-by-Side Comparison

| | Apache Kafka | RabbitMQ |
|---|---|---|
| Model | Partitioned, replicated append-only log | Exchanges route messages into queues |
| After consumption | Records stay until retention expires | Message is deleted on ack (except streams) |
| Replay | ✅ Reset offsets to any point in retention | ❌ for queues; ✅ with RabbitMQ streams |
| Multiple consumers of the same data | Native: one consumer group per service | One queue per subscriber, bound to an exchange |
| Ordering | Per partition (per key) | Per queue, with a single consumer |
| Routing | By topic and key; filtering happens in consumers | Rich: direct, topic patterns, fanout, headers |
| Consumer scaling | Up to the number of partitions per group | Add consumers to a queue freely |
| Per-message features | Few (headers, timestamps) | TTL, priorities, dead-lettering, delivery limits |
| Delayed / scheduled delivery | Not built in | TTL + DLX patterns, delayed-message plugin |
| Retry and DLQ | Implemented by the client (Spring Kafka `DefaultErrorHandler`, retry topics) | Broker-level DLX + Spring Retry |
| Throughput | Very high; sequential disk I/O and batching | High; lower than Kafka for large sustained streams |
| Latency | Low (ms), tunable vs throughput | Very low for small messages |
| Stream processing | Kafka Streams, ksqlDB, Flink, Kafka Connect ecosystem | Not a focus |
| Delivery guarantee | At-least-once; exactly-once for Kafka → Kafka with transactions | At-least-once with confirms and acks |
| Protocol | Kafka binary protocol | AMQP 0-9-1, AMQP 1.0 (native in 4.x), MQTT, STOMP |
| Operations | Brokers + KRaft controllers; partitions and retention planning | Cluster of nodes; quorum queues; simpler for small setups |
| Spring support | Spring for Apache Kafka (`@KafkaListener`, `KafkaTemplate`) | Spring AMQP (`@RabbitListener`, `RabbitTemplate`) |

---

## 2. When to Choose Kafka

- **Event-driven architecture with many consumers** — several services react to the same domain events, each at its own pace.
- **Replay and reprocessing** — rebuild a read model, backfill a new service, recover from a consumer bug.
- **High-volume streams** — clickstreams, telemetry, logs, CDC from databases.
- **Stream processing** — aggregations, joins and materialized views with Kafka Streams or Flink.
- **Integration hub** — Kafka Connect moves data between databases, search, warehouses and object storage.

## 3. When to Choose RabbitMQ

- **Work queues / background jobs** — emails, PDF generation, image processing with a pool of workers.
- **Complex routing** — deliver messages by pattern, region, priority or header without consumer-side filtering.
- **Per-message control** — TTLs, priorities, delayed retries, dead-lettering per queue.
- **Request/reply** between services.
- **Smaller-scale systems** where operational simplicity matters more than retention and replay.
- **Protocol variety** — IoT devices over MQTT, web clients over STOMP/WebSockets.

## 4. Gray Areas

| Scenario | Notes |
|---|---|
| "We need both events and task queues" | Many companies run both: Kafka for domain events between services, RabbitMQ for internal job queues. |
| "RabbitMQ streams make it Kafka-like" | Streams add retention, replay and high fan-out to RabbitMQ. Good when you're already on RabbitMQ and need some log semantics — but the Kafka ecosystem (Connect, Streams, Schema Registry) is far larger. |
| "Kafka can do queues" | Kafka 4.x adds *share groups* (queues for Kafka, KIP-932) as an early-access/preview feature, allowing several consumers per partition with per-record acknowledgement. Check its status in your Kafka version before relying on it. |
| Managed services | Confluent Cloud, Amazon MSK, Aiven (Kafka); Amazon MQ, CloudAMQP (RabbitMQ). Managed offerings reduce the operational gap considerably. |

---

## 5. The Same Problem in Both

**Requirement:** when an order is created, invoicing and shipping must each process it once; failures are retried, then parked.

| Step | Kafka | RabbitMQ |
|---|---|---|
| Publish | `kafkaTemplate.send("orders", orderId, event)` | `rabbitTemplate.convertAndSend("orders", "order.created.eu", event)` |
| Fan-out | Separate consumer groups `invoicing`, `shipping` | Queues `invoicing.order-events`, `shipping.order-events` bound to exchange `orders` |
| Scale a service | Add instances (≤ partitions) | Add instances (any number) |
| Ordering per order | Key = order ID | Single active consumer or consistent-hash exchange |
| Retry | `DefaultErrorHandler` with backoff, or `@RetryableTopic` | Spring Retry with backoff, TTL wait queues |
| Dead letters | `orders-dlt` topic | DLX → `invoicing.order-events.dlq` |
| Reprocess last week | Reset the group's offsets | Not possible unless messages were kept elsewhere |

---

## 6. Interview Angle

Typical questions and the points worth making:

- **"Kafka or RabbitMQ for X?"** — Start from requirements: replay, number of consumers, ordering, routing complexity, volume, team experience. Avoid "Kafka is faster" as the only argument.
- **"How do you guarantee no message loss?"** — Kafka: `acks=all`, RF 3, `min.insync.replicas=2`, idempotent producer, commit after processing. RabbitMQ: quorum queues, publisher confirms + returns, manual/auto acks after processing, DLX. Both: transactional outbox for DB consistency.
- **"How do you handle duplicates?"** — At-least-once is the norm in both; idempotent consumers with a dedup key.
- **"How do you keep order?"** — Kafka: same key → same partition, one consumer per partition. RabbitMQ: one consumer per queue (single active consumer), or consistent hashing across queues.

---

## Summary

| Choose | When you need |
|---|---|
| **Kafka** | Durable event history, replay, many independent consumers, high-volume streams, stream processing |
| **RabbitMQ** | Task queues, rich routing, per-message TTL/priority/delays, request/reply, simpler operations at small scale |

---

## See also

- [Kafka fundamentals](1.%20Apache%20Kafka/1.%20Kafka%20fundamentals.md)
- [RabbitMQ fundamentals](2.%20RabbitMQ/1.%20RabbitMQ%20fundamentals.md)
- [Message queues and event streaming — system design](../Java/4.%20Specialized%20Topics/5.%20System%20Design/4.%20Message%20queues%20and%20event%20streaming.md)
- [Event-driven architecture design — interview](../Java/5.%20Interviews%20%26%20Soft%20Skills/4.%20Architecture%20and%20Design%20Interview/2.%20Event-driven%20architecture%20design.md)
