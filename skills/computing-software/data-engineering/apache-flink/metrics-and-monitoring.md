---
id: computing-software.data-engineering.apache-flink.metrics-and-monitoring
name: metrics-and-monitoring
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-deployment, flink-metrics, prometheus-reporter, checkpoint-metrics, kafka-consumer-lag, busy-time, watermark-lag, alerting]
level: practitioner
status: docs-checked
description: "Monitor Flink jobs: Prometheus reporter setup, the metrics that matter (throughput, busy/backpressure time, checkpoints, restarts, watermark and Kafka lag), custom metrics and alert rules."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/metrics/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/metric_reporters/
  - https://github.com/apache/flink-connector-kafka/blob/main/docs/content/docs/connectors/datastream/kafka.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flink metrics and monitoring

**Goal:** know within minutes when a job is down, falling behind, or about to fail checkpoints — before consumers notice stale data.

## 1. Export metrics
```yaml
metrics.reporter.prom.factory.class: org.apache.flink.metrics.prometheus.PrometheusReporterFactory
metrics.reporter.prom.port: 9249
```
Scrape JobManager and TaskManager pods (PodMonitor / annotations). The Prometheus reporter listens on port 9249 by default; a separate PrometheusPushGateway reporter exists for push-based setups. Other reporters (for example JMX) are configured the same way: each reporter needs `metrics.reporter.<name>.factory.class`, and some also take an `interval`.
Cardinality: per-operator, per-subtask metrics multiply fast; drop unneeded labels in Prometheus relabeling. Latency tracking is controlled by `metrics.latency.interval`; leave it off unless you need latency markers.

## 2. The metrics that matter
| Concern | Metric(s) | Alert idea |
|---|---|---|
| Job up | `runningTime` (`uptime` is deprecated), `numRestarts` (job, JobManager) | restarts increasing over 15 min |
| Throughput | `numRecordsInPerSecond` / `numRecordsOutPerSecond` (operator/task) | drop to 0 while source has data |
| Bottleneck | `busyTimeMsPerSecond`, `backPressuredTimeMsPerSecond`, `idleTimeMsPerSecond` | busy ~1000 on one operator sustained |
| Checkpoints | `lastCheckpointDuration`, `lastCheckpointSize`, `numberOfFailedCheckpoints`, `numberOfCompletedCheckpoints` | failed count rising; duration near timeout |
| Event-time progress | `currentInputWatermark` / `currentOutputWatermark` | now - watermark > N minutes |
| Source lag | source `pendingRecords` (records not yet fetched by the source) | lag growing for 10 min |
| JVM | `Status.JVM.Memory.Heap.Used`, `Status.JVM.GarbageCollector` metrics, `Status.JVM.CPU` metrics | heap near its limit sustained, GC time high |
Kafka consumer group lag can also be watched from the broker side (Burrow, kafka-exporter) — useful when the job is down and emits nothing.

## 3. Custom metrics
```java
public class ParseEvents extends RichMapFunction<String, Event> {
  private transient Counter badRecords;
  private transient Histogram payloadSize;
  @Override public void open(OpenContext ctx) {
    MetricGroup g = getRuntimeContext().getMetricGroup().addGroup("parser");
    badRecords = g.counter("bad_records");
    payloadSize = g.histogram("payload_bytes", new DropwizardHistogramWrapper(
        new com.codahale.metrics.Histogram(new com.codahale.metrics.SlidingWindowReservoir(500))));   // needs flink-metrics-dropwizard
  }
  @Override public Event map(String s) { payloadSize.update(s.length()); try { return Event.parse(s); } catch (Exception e) { badRecords.inc(); return null; } }
}
```
Gauges for current values (`g.gauge("cacheSize", () -> cache.size())`), meters for rates.

## 4. Dashboards
Per job: records in/out, source lag, watermark lag, checkpoint duration/size/failures, restarts, busy/backpressure per operator, TM heap/GC.

## 5. Alert rules (Prometheus examples)
```yaml
- alert: FlinkJobRestarting
  expr: increase(flink_jobmanager_job_numRestarts[15m]) > 3
- alert: FlinkCheckpointsFailing
  expr: increase(flink_jobmanager_job_numberOfFailedCheckpoints[30m]) > 2
- alert: FlinkKafkaLagGrowing
  expr: deriv(flink_taskmanager_job_task_operator_pendingRecords[10m]) > 0
```
Metric names depend on scope formats and reporter; confirm against your `/metrics` endpoint.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the metrics reference (`numRestarts`, deprecated `uptime` in favour of `runningTime`, checkpoint metrics, `numRecordsInPerSecond`/`numRecordsOutPerSecond`, busy/idle/back pressured time, watermark metrics, `Status.JVM.*` groups, counters/gauges/histograms/meters, Dropwizard histogram wrapper), the metric reporters page (`factory.class`, Prometheus reporter default port 9249, PushGateway reporter), the generated configuration table (`metrics.latency.interval`) and the Kafka connector page (`pendingRecords`). Removed the unconfirmed `currentEmitEventTimeLag` and `records-lag-max` metrics, the unlisted reporter names and the fixed alert thresholds; the Prometheus alert expressions are examples whose metric names depend on scope formats.

Method: documentation only; no commands were run.

## Verify
- [ ] Killing a TaskManager triggers the restart alert.
- [ ] Pausing the job makes the lag alert fire.
- [ ] Every production job appears on the dashboard with owner labels.
