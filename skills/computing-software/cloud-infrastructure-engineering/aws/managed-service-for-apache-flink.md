---
id: computing-software.cloud-infrastructure-engineering.aws.managed-service-for-apache-flink
name: managed-service-for-apache-flink
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, managed-flink, apache-flink, kinesis-data-analytics, kinesisanalyticsv2, stream-processing, kpu, checkpoints, snapshots, parallelism, kinesis-data-streams, msk, flink-studio]
level: advanced
status: docs-checked
description: "Run Apache Flink apps on Amazon Managed Service for Apache Flink: package and deploy, size KPUs and parallelism, checkpoints/snapshots, upgrades, autoscaling and lag alarms."
sources: ["https://docs.aws.amazon.com/managed-flink/latest/java/what-is.html", "https://docs.aws.amazon.com/managed-flink/latest/java/how-scaling.html", "https://docs.aws.amazon.com/managed-flink/latest/java/best-practices.html", "https://docs.aws.amazon.com/managed-flink/latest/java/metrics-dimensions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amazon Managed Service for Apache Flink

(The API namespace is `kinesisanalyticsv2`.)

**Goal:** a stateful streaming job reads from Kinesis or MSK, writes to sinks, survives restarts from snapshots and
scales without losing state. The service provides compute provisioning, AZ failover resilience, parallel computation,
automatic scaling, and application backups implemented as checkpoints and snapshots.

## 1. Package
- Build an uber JAR with the minimum code needed: no source classes, test datasets or bootstrap state; pull static
  resources (a model, state bootstrap) from S3 at runtime. The service supports 512 MB JARs but treat that as the
  exception; the docs give about 104 MB as the target maximum.
- Dependencies the runtime already provides use `provided` scope in Maven/SBT or `compileOnly` in Gradle (a provided
  dependency bundled in the JAR is ignored because of Flink's parent-first class loading). Connectors not in the runtime
  (except the FileSystem connector) go in with default scope.
- The runtime provides `com.amazonaws:aws-kinesisanalytics-runtime:1.2.0` to read application runtime properties; read
  stream names and similar settings from there instead of hard-coding them.
- Add the Maven shade plugin's `ServiceResourceTransformer` so Service Provider Interface files from several
  dependencies do not clash.
- Do not call `System.exit()`; throw an exception instead. From a user-defined function the job manager fails and
  restarts the job.
- From Flink 1.15, the service refuses to start or update applications that bundle an unsupported Kinesis connector;
  use 1.15.2 or newer.

## 2. Create
```bash
aws s3 cp target/app-1.0.jar s3://<ARTIFACT_BUCKET>/app-1.0.jar
aws kinesisanalyticsv2 create-application --application-name clickstream-agg \
  --runtime-environment FLINK-1_20 \
  --service-execution-role arn:aws:iam::<ACCOUNT_ID>:role/flink-app \
  --application-configuration '{
    "ApplicationCodeConfiguration":{"CodeContent":{"S3ContentLocation":{"BucketARN":"arn:aws:s3:::<ARTIFACT_BUCKET>","FileKey":"app-1.0.jar"}},"CodeContentType":"ZIPFILE"},
    "FlinkApplicationConfiguration":{
      "CheckpointConfiguration":{"ConfigurationType":"DEFAULT"},
      "ParallelismConfiguration":{"ConfigurationType":"CUSTOM","Parallelism":8,"ParallelismPerKPU":1,"AutoScalingEnabled":true},
      "MonitoringConfiguration":{"ConfigurationType":"CUSTOM","MetricsLevel":"OPERATOR","LogLevel":"INFO"}},
    "EnvironmentProperties":{"PropertyGroups":[{"PropertyGroupId":"app","PropertyMap":{"input.stream":"clicks"}}]},
    "ApplicationSnapshotConfiguration":{"SnapshotsEnabled":true}}' \
  --cloud-watch-logging-options LogStreamARN=arn:aws:logs:<REGION>:<ACCOUNT_ID>:log-group:/flink/clickstream:log-stream:app
aws kinesisanalyticsv2 start-application --application-name clickstream-agg \
  --run-configuration '{"ApplicationRestoreConfiguration":{"ApplicationRestoreType":"RESTORE_FROM_LATEST_SNAPSHOT"}}'
```
The API model lists `ApplicationRestoreType` values `SKIP_RESTORE_FROM_SNAPSHOT`, `RESTORE_FROM_LATEST_SNAPSHOT` and
`RESTORE_FROM_CUSTOM_SNAPSHOT`, and `FlinkRunConfiguration.AllowNonRestoredState`. For VPC access (MSK, RDS) add
`VpcConfigurations` with `SubnetIds` and `SecurityGroupIds`.

## 3. Sizing and scaling
- A KPU is 1 vCPU and 4 GB of memory, with 50 GB of running application storage per KPU.
- Allocated KPUs = `Parallelism / ParallelismPerKPU`, plus one additional KPU charged for orchestration.
- `Parallelism` defaults to 1 (default maximum 256); `ParallelismPerKPU` defaults to 1 (maximum 8). For applications with
  blocking operations such as I/O, a higher `ParallelismPerKPU` uses KPU resources fully. The default KPU limit is 64
  and can be raised through Service Quotas.
- Automatic scaling adds resources quickly in response to spikes and removes them gradually afterwards; set
  `AutoScalingEnabled` to false to turn it off.
- A job cannot scale past the smallest `maxParallelism` of its operators. If you set none and start at parallelism of
  128 or less, every operator gets 128; set it explicitly to scale beyond 128. Changing `maxParallelism` on an existing
  application means it cannot restart from earlier snapshots. Scaling beyond it makes the application fail to start.
- Per-operator parallelism: `setParallelism(x)` at or below the application parallelism, ideally as a function of the
  application parallelism so autoscaling moves all operators proportionally. A source over a Kinesis stream is often set
  to the shard count; pass it as an application property.
- Changing an operator's parallelism can make older snapshots unrestorable.

## 4. State, checkpoints, snapshots
- Keep checkpointing enabled: it gives fault tolerance during scheduled maintenance and unexpected failures.
- A snapshot is created on every application stop. During development or troubleshooting set `SnapshotsEnabled` to
  false so a stop of an unhealthy application is not blocked; set it true once production is stable. The docs
  recommend snapshots several times a day, with frequency depending on your business logic (more frequent costs more).
- Set an explicit UID on every operator. Without it Flink generates IDs that may differ between job graph builds, and
  the job can fail to start from a snapshot with an operator ID mismatch, which is most likely during maintenance runs.
- `UID` setting is available only with the DataStream API (Java and Python).
- Update with `update-application` and the current application version ID.

## 5. Monitor
Metrics documented for the service: `cpuUtilization`, `heapMemoryUtilization`, `lastCheckpointDuration`,
`lastCheckpointSize`, `numberOfFailedCheckpoints`, `KPUs`, `millisBehindLatest` (Kinesis source) and `records_lag_max`
(MSK/Kafka source). `backPressuredTimeMsPerSecond` and `busyTimeMsPerSecond` are documented as Flink 1.13 only.
Flink 2.2 changes: `fullRestarts` removed (use `numRestarts`), `downtime` and `uptime` deprecated in favour of
`restartingTime`, `cancellingTime`, `failingTime` and `runningTime`.
Also enable CloudWatch logging, avoid a log entry per record (it causes backpressure), and create alarms.

## Gotchas
- Choose DataStream API when you need fine-grained state control, async calls to external endpoints, custom timers, or
  to change the flow without resetting state. Not all connectors are supported in Python; use Java or Scala for
  low latency or high throughput.
- Studio notebooks are for ad-hoc exploration; for Git/CI/CD and unit testing the docs recommend a packaged application.
- Idle shards and watermark strategy can stop windows from closing; use a bounded-out-of-orderness strategy or allowed
  lateness.

## Verify
- [ ] Application is `RUNNING` and `numberOfFailedCheckpoints` stays at 0.
- [ ] Source lag metric stays stable under peak load.
- [ ] A code update restores from snapshot and window state continues.
- [ ] A stop and start drill restores from the latest snapshot.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the what-is, application scaling, best-practices and metrics pages, plus the botocore
kinesisanalyticsv2 model (field names, runtime and restore enums). The snapshot page returned no readable content. Removed:
the PyFlink packaging property, checkpoint default interval, built-in autoscaling doubling and cooldown behaviour, RocksDB
default backend, enhanced fan-out quota, the CloudWatch namespace, the restart-loop and DLQ advice, and the
in-place runtime upgrade claim.
