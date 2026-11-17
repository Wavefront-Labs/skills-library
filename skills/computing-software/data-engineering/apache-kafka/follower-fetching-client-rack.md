---
id: computing-software.data-engineering.apache-kafka.follower-fetching-client-rack
name: follower-fetching-client-rack
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-consumer, follower-fetching, client-rack, replica-selector, cross-az-cost, kip-392]
level: advanced
status: docs-checked
description: "Cut cross-AZ traffic by letting Kafka consumers fetch from an in-zone follower: replica.selector.class, client.rack, and the latency and lag trade-offs."
sources:
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-392%3A+Allow+consumers+to+fetch+from+closest+replica
  - https://kafka.apache.org/40/configuration/broker-configs/
  - https://kafka.apache.org/40/configuration/consumer-configs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rack-aware follower fetching (client.rack)

By default consumers fetch from the partition **leader**, which is often in another AZ. On clouds, cross-AZ transfer is typically billed per GB (check your provider). KIP-392 lets a consumer read from a follower in its own rack.

## Configure
Brokers:
```properties
broker.rack=us-east-1a
replica.selector.class=org.apache.kafka.common.replica.RackAwareReplicaSelector
```
Consumers:
```properties
client.rack=us-east-1a        # must equal the broker.rack string of brokers in the same AZ
```
- `replica.selector.class` defaults to null, which means the leader is used. `client.rack` defaults to an empty string and "corresponds with the broker config `broker.rack`" (consumer configs page).
- On Kubernetes and managed services, work out how your platform exposes the zone to the client and set `client.rack` to the same string as `broker.rack`.

## Trade-offs
- **Latency**: followers only serve records up to the high watermark they know, and the leader always sees high watermark updates before any follower. KIP-392 says "some extra latency is expected when fetching from followers"; an idle partition can see the follower's high watermark delayed by as long as `replica.fetch.max.wait.ms`.
- A consumer whose broker does not support follower fetching reverts to fetching from the leader.
- Fetching an offset between a replica's high watermark and log end offset returns `OFFSET_NOT_AVAILABLE`, and the consumer retries.
- Producers still write to the leader (cross-AZ replication is unavoidable).
- Benefit is only real if partitions have a replica in each consumer AZ: set `broker.rack` and use rack-aware replica placement with enough replicas.
- Kafka Streams and Connect consumers need `client.rack` set through their consumer config prefix; check the Streams and Connect docs for the exact key.

## Verify
- [ ] The Java client exposes a `preferred-read-replica` attribute under `kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*,topic=*,partition=*`: the broker ID the consumer reads from; missing or -1 means it is reading from the leader.
- [ ] Cloud billing or VPC flow logs show cross-AZ bytes from brokers to consumers dropping.
- [ ] End-to-end latency still within SLO.

## Checked
2026-11-09. Confirmed against KIP-392, the Kafka 4.0 broker-configs page (`replica.selector.class`) and consumer-configs page (`client.rack`). Removed unconfirmed claims: version gate, Kubernetes downward API detail, Strimzi, MSK and Confluent Cloud support, the Streams/Connect key names and the Fetch request-rate metric.
Method: documentation only; no commands were run.
