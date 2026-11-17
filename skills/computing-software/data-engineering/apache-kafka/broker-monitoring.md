---
id: computing-software.data-engineering.apache-kafka.broker-monitoring
name: broker-monitoring
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-operations, under-replicated-partitions, kafka-jmx-metrics, jmx-exporter, offline-partitions, request-latency, isr-shrink, prometheus, grafana, broker-monitoring]
level: advanced
status: docs-checked
description: "Monitor Kafka brokers: the JMX metrics that matter (URP, UnderMinIsr, offline partitions, ISR shrink, request latency, handler idle) and which ones to alert on."
sources:
  - https://kafka.apache.org/39/operations/monitoring/
  - https://github.com/prometheus/jmx_exporter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka broker monitoring

**Goal:** detect data-loss risk and client-visible slowness before users report it.

## Export metrics
Attach the Prometheus JMX exporter java agent to each broker (see the jmx_exporter documentation for the agent syntax) with a curated rules file; exporting every MBean creates huge cardinality.

## Page-worthy alerts
| Metric (MBean) | Alert |
|---|---|
| `kafka.controller:type=KafkaController,name=OfflinePartitionsCount` | > 0: partitions unavailable |
| `kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount` | > 0: `acks=all` producers failing |
| `kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions` | > 0 for a sustained period (outside planned maintenance) |
| `kafka.controller:type=KafkaController,name=ActiveControllerCount` | exactly one broker in the cluster should report 1 |
| Disk usage per log dir | your threshold |
| Broker down (scrape up == 0) | any |

## Warning / dashboard metrics
- `kafka.server:type=ReplicaManager,name=IsrShrinksPerSec` / `IsrExpandsPerSec`: flapping ISR = slow followers, network or GC.
- `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce|FetchConsumer|FetchFollower` broken into `RequestQueueTimeMs`, `LocalTimeMs`, `RemoteTimeMs` (the time the request waits for the follower; non-zero for produce requests with acks=-1), `ResponseQueueTimeMs`, `ResponseSendTimeMs`: tells you where latency comes from.
- `kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent` and `kafka.network:type=SocketServer,name=NetworkProcessorAvgIdlePercent`: between 0 and 1, ideally > 0.3 (the monitoring page); persistently lower means saturated threads.
- `BytesInPerSec`, `BytesOutPerSec`, `MessagesInPerSec` per broker and topic: balance and capacity.
- `kafka.log:type=LogFlushStats,name=LogFlushRateAndTimeMs`, plus JVM GC pause time.
- `kafka.server:type=ReplicaFetcherManager,name=MaxLag,clientId=Replica`.

## Consumer lag
Consumer lag is published by the consumer, not the broker: `kafka.consumer:type=consumer-fetch-manager-metrics,client-id={client-id}` attribute `records-lag-max` (the monitoring page). Alert on it per consumer group.

## Checked
2026-10-28. Confirmed on the Kafka 3.9 monitoring page: the MBean names for OfflinePartitionsCount, UnderMinIsrPartitionCount, UnderReplicatedPartitions, ActiveControllerCount, IsrShrinksPerSec, IsrExpandsPerSec, RequestMetrics TotalTimeMs and its components, RequestHandlerAvgIdlePercent and NetworkProcessorAvgIdlePercent (ideally > 0.3), ReplicaFetcherManager MaxLag, BytesIn/Out and MessagesIn. Removed: java agent command line, p99, specific disk and URP time thresholds and thread-tuning advice that the page does not state.
Also confirmed: `RemoteTimeMs`, `LogFlushRateAndTimeMs` and the consumer `records-lag-max` metric. Removed the third-party lag tool list.
Method: documentation only; no commands were run.

## Verify
- [ ] Stopping one broker in staging fires URP within minutes and clears after restart.
- [ ] Dashboard shows Produce TotalTimeMs with its component breakdown.
- [ ] Alert rules are in version control with runbook links.
