# Kafka vs RabbitMQ vs NATS

> **Applies to:** Apache Kafka 3.x–4.x · RabbitMQ 3.13–4.x · NATS Server 2.10+ · Spring Boot 3.x · **Last updated:** 2026-11-21

## Overview

All three are mature and production-proven, and all three can be used from Spring Boot. They're built on different models, and that model — not raw speed — should drive the choice:

- **Kafka** is a distributed **log**. Records are retained, consumers track their own position, and many consumer groups can read (and re-read) the same data.
- **RabbitMQ** is a **message broker**. Exchanges route messages into queues, which are emptied as consumers acknowledge them; it's optimized for flexible routing and per-message handling.
- **NATS** is a lightweight **subject-based messaging system**. Core NATS is fast, in-memory pub/sub and request/reply with at-most-once delivery; **JetStream** adds persistent streams, consumers with acks, and a key-value store — in the same small server.

**Key Concept**: Ask what consumers need. The *history* of events, replayed by many independent readers → Kafka. The *next task*, routed by rules with per-message control → RabbitMQ. *Low-latency connectivity* between services (request/reply, fan-out), optionally with persistence, in a very small operational footprint → NATS.

---

## 1. Side-by-Side Comparison

| | Apache Kafka | RabbitMQ | NATS (core + JetStream) |
|---|---|---|---|
| Model | Partitioned, replicated append-only log | Exchanges route messages into queues | Subjects; JetStream streams + consumers for persistence |
| After consumption | Records stay until retention expires | Message deleted on ack (except streams) | Core: never stored. JetStream: per retention policy (limits, interest, work queue) |
| Replay | ✅ Reset offsets within retention | ❌ for queues; ✅ with RabbitMQ streams | ❌ core; ✅ JetStream (by sequence or time) |
| Default delivery | At-least-once | At-least-once (with confirms + acks) | Core: at-most-once. JetStream: at-least-once |
| Exactly-once options | Kafka → Kafka transactions | — | Publish de-dup (`Nats-Msg-Id`) + double ack |
| Multiple consumers of the same data | One consumer group per service | One queue per subscriber, bound to an exchange | Core: each subscription gets a copy. JetStream: one consumer per service |
| Load balancing within a service | Partitions split across group members | Competing consumers on a queue | Queue groups (core) or shared pull consumers (JetStream) |
| Ordering | Per partition (per key) | Per queue, with a single consumer | Per stream/consumer, with one message in flight |
| Routing | Topic + key; filtering in consumers | Rich: direct, topic patterns, fanout, headers | Subject hierarchy with `*` and `>` wildcards |
| Request/reply | Possible, awkward (`ReplyingKafkaTemplate`) | Supported (reply-to, direct reply-to) | **First-class**, with "no responders" detection |
| Per-message features | Few (headers, timestamps) | TTL, priorities, dead-lettering, delivery limits | Headers; JetStream: per-message nak delay, term, max deliver |
| Dead letters | Client-side (Spring Kafka DLT) | Broker-level DLX | Advisories on max deliveries → your DLQ stream |
| Built-in KV / object storage | — (compacted topics) | — | ✅ JetStream KV and object store |
| Stream processing ecosystem | Kafka Streams, Connect, ksqlDB, Flink | Not a focus | Limited |
| Throughput | Very high for sustained streams | High | Very high for core; high for JetStream |
| Latency | Low (ms) | Very low | Very low (sub-ms for core) |
| Footprint and operations | Brokers + KRaft controllers; partition and retention planning | Cluster of nodes; quorum queues | Single small binary; clusters, superclusters, leaf nodes |
| Multi-tenancy | ACLs, quotas | vhosts, permissions | Accounts with explicit subject exports/imports |
| Protocols | Kafka protocol | AMQP 0-9-1, AMQP 1.0, MQTT, STOMP | NATS protocol; MQTT and WebSocket gateways built in |
| Spring support | Spring for Apache Kafka (auto-configured) | Spring AMQP (auto-configured) | No Spring Boot auto-config; use the `jnats` client (plus community/NATS-maintained integrations) |

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
- **Protocol variety** — IoT devices over MQTT, web clients over STOMP/WebSockets, AMQP 1.0 interop.
- **Strong Spring integration** with minimal code (`@RabbitListener`, `RabbitTemplate`).

## 4. When to Choose NATS

- **Service-to-service request/reply** — load-balanced RPC through queue groups, no service discovery or load balancer needed.
- **Low-latency fan-out** — live updates, presence, telemetry, control-plane messages where the newest data matters most.
- **Edge, IoT and multi-region** — leaf nodes connect remote sites (factories, vehicles, stores) to a central cluster over one subject space, tolerating disconnections.
- **Small footprint** — one lightweight binary that's simple to run in Kubernetes, on edge devices or in tests.
- **Messaging plus simple state** — JetStream streams, work queues and KV buckets cover many needs without adding Redis or a separate broker.

---

## 5. Gray Areas

| Scenario | Notes |
|---|---|
| "We need events *and* task queues" | Many companies run two systems (e.g. Kafka for domain events, RabbitMQ for job queues). JetStream can cover both in one system for moderate scale — streams with `Limits` retention for events, `WorkQueue` retention for jobs. |
| "RabbitMQ streams make it Kafka-like" | Streams add retention, replay and high fan-out to RabbitMQ. Good if you already run RabbitMQ; the Kafka ecosystem (Connect, Streams, Schema Registry) is still far larger. |
| "Kafka can do queues" | Kafka 4.x adds *share groups* (KIP-932) as an early-access/preview feature: several consumers per partition with per-record acks. Check its status in your Kafka version first. |
| "Can NATS replace Kafka?" | JetStream gives replayable, replicated streams and is easier to run. Kafka remains stronger for very large retained data sets, long-term retention, and the data-integration / stream-processing ecosystem. |
| "Can NATS replace HTTP between services?" | For internal calls, often yes: request/reply over NATS gives load balancing, location transparency and no-responder detection. You lose some HTTP tooling (gateways, OpenAPI-first workflows, browser access). |
| Managed services | Kafka: Confluent Cloud, Amazon MSK, Aiven. RabbitMQ: Amazon MQ, CloudAMQP. NATS: Synadia Cloud. Managed offerings narrow the operational differences. |

---

## 6. The Same Problem in All Three

**Requirement:** when an order is created, invoicing and shipping must each process it; failures are retried, then parked.

| Step | Kafka | RabbitMQ | NATS JetStream |
|---|---|---|---|
| Publish | `kafkaTemplate.send("orders", orderId, event)` | `rabbitTemplate.convertAndSend("orders", "order.created.eu", event)` | `js.publish("orders.created.eu", bytes, PublishOptions.builder().messageId(id).build())` |
| Storage | Topic `orders` | Queues `invoicing.order-events`, `shipping.order-events` bound to exchange `orders` | Stream `ORDERS` capturing `orders.>` |
| Fan-out | Consumer groups `invoicing`, `shipping` | One queue per service | Durable consumers `invoicing`, `shipping` |
| Scale a service | Add instances (≤ partitions) | Add instances (any number) | Add instances pulling from the same durable consumer |
| Ordering per order | Key = order ID | Single active consumer or consistent-hash exchange | One in-flight message per consumer, or subject partitioning |
| Retry | `DefaultErrorHandler` with backoff, or `@RetryableTopic` | Spring Retry, TTL wait queues | `nakWithDelay`, consumer `backoff` |
| Dead letters | `orders-dlt` topic | DLX → `*.dlq` queue | Max-deliveries advisory → DLQ stream |
| Reprocess last week | Reset the group's offsets | Not possible unless stored elsewhere | New consumer with `DeliverPolicy.ByStartTime` |

And if durability isn't needed — say, pushing live order-status updates to connected UIs — core NATS pub/sub (or a RabbitMQ fanout exchange) is simpler than any of the above.

---

## 7. Interview Angle

- **"Kafka, RabbitMQ or NATS for X?"** — Start from requirements: replay, number of consumers, ordering, routing complexity, request/reply, latency, volume, footprint, team experience. "Kafka is faster" is not an argument on its own.
- **"How do you guarantee no message loss?"** — Kafka: `acks=all`, RF 3, `min.insync.replicas=2`, commit after processing. RabbitMQ: quorum queues, publisher confirms + returns, acks after processing, DLX. NATS: JetStream (core NATS is at-most-once), R3 streams, explicit acks, publish acks. All: transactional outbox for consistency with a database.
- **"How do you handle duplicates?"** — At-least-once is the norm everywhere; idempotent consumers with a dedup key. NATS and Kafka can also de-duplicate on the publish side.
- **"How do you keep order?"** — Kafka: same key → same partition. RabbitMQ: single active consumer or consistent hashing. NATS: one message in flight per consumer, or partitioned subjects.

---

## Summary

| Choose | When you need |
|---|---|
| **Kafka** | Durable event history, replay, many independent consumers, high-volume streams, stream processing and data integration |
| **RabbitMQ** | Task queues, rich routing, per-message TTL/priority/delays and dead-lettering, multiple protocols, tight Spring integration |
| **NATS** | Low-latency request/reply and fan-out, edge/multi-region connectivity, small footprint; JetStream when you also need persistence and KV |

---

## See also

- [Kafka fundamentals](1.%20Apache%20Kafka/1.%20Kafka%20fundamentals.md)
- [RabbitMQ fundamentals](2.%20RabbitMQ/1.%20RabbitMQ%20fundamentals.md)
- [NATS fundamentals](3.%20NATS/1.%20NATS%20fundamentals.md)
- [Message queues and event streaming — system design](../Java/4.%20Specialized%20Topics/5.%20System%20Design/4.%20Message%20queues%20and%20event%20streaming.md)
- [Event-driven architecture design — interview](../Java/5.%20Interviews%20%26%20Soft%20Skills/4.%20Architecture%20and%20Design%20Interview/2.%20Event-driven%20architecture%20design.md)
