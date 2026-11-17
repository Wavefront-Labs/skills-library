---
id: computing-software.data-engineering.apache-hadoop.yarn-timeline-service-v2-setup
name: yarn-timeline-service-v2-setup
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, timeline-service, hbase, collector, flow-context]
level: advanced
status: docs-checked
description: "YARN Timeline Service v2 setup: enabling version 2.0f, the HBase writer, timeline_collector aux service, supported HBase versions, schema creation and flow context tags."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/TimelineServiceV2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timeline Service v2

Collectors (writers) are NM auxiliary services co-located with each application master; the RM has its own in-process collector emitting only YARN-generic lifecycle events. The reader is a separate daemon serving a REST API, currently a single instance. Storage is Apache HBase.

Core settings:
- `yarn.timeline-service.enabled` = true (default false)
- `yarn.timeline-service.version` = `2.0f` (default 1.0f); `yarn.timeline-service.versions` = `1.5f,2.0f` runs both, and defaults to the single version setting if not set
- `yarn.timeline-service.writer.class` and `yarn.timeline-service.reader.class`: default to the HBase writer and reader
- `yarn.nodemanager.aux-services`: `mapreduce_shuffle,timeline_collector`, with `yarn.nodemanager.aux-services.timeline_collector.class` = `org.apache.hadoop.yarn.server.timelineservice.collector.PerNodeTimelineCollectorsAuxService` (with an aux-services manifest, add a `timeline_collector` entry with `class.name` set to that class instead)
- `yarn.system-metrics-publisher.enabled` = true (default false)
- `yarn.timeline-service.reader.webapp.address`: default `${yarn.timeline-service.hostname}:8188`; HTTPS default port 8190
- Optional: set `yarn.resourcemanager.cluster-id` to a unique value if several clusters share one HBase; point clients at HBase with `hbase-site.xml` on the classpath or `yarn.timeline-service.hbase.configuration.file`
- Default HBase table prefix `yarn.timeline-service.schema.prefix` is `prod.`

HBase: supported versions are 1.2.6 (default, what Hadoop releases are built with) and 2.0.0-beta1 (build from source with `-Dhbase.profile=2.0`). The 1.0.x versions do not work.

Prepare storage:
1. Coprocessor: it is loaded dynamically as a table coprocessor on the `flowrun` table. Copy the timeline service coprocessor jar to HDFS, default `/hbase/coprocessor` (`hadoop fs -mkdir /hbase/coprocessor`, then `hadoop fs -put` the jar there as `hadoop-yarn-server-timelineservice.jar`). To use a different location set `yarn.timeline-service.hbase.coprocessor.jar.hdfs.location`.
2. Schema: run on the HBase cluster with the timelineservice-hbase client, timelineservice and hbase-common jars on `HBASE_CLASSPATH` (fetch them from the HDFS coprocessor directory):
```
bin/hbase org.apache.hadoop.yarn.server.timelineservice.storage.TimelineSchemaCreator -create
```
`-skipExistingTable` (`-s`) skips existing tables; `-help` prints usage; `-entityTableName`, `-appToflowTableName`, `-applicationTableName`, `-subApplicationTableName` override table names, in which case the matching `yarn.timeline-service.*.table.name` keys must be set in the `hbase-site.xml` that `yarn.timeline-service.hbase.configuration.file` points to.

Run: restart the RM and NMs (collectors start embedded in them), then start the reader as a separate daemon: `yarn-daemon.sh start timelinereader`. For MapReduce data set `mapreduce.job.emit-timeline-data` = true in `mapred-site.xml`.

Flow context comes from YARN application tags (`TimelineUtils.generateFlowNameTag`, `generateFlowVersionTag`, `generateFlowRunIdTag`). Defaults when absent: flow name is the application name (or application id if unset), run id is the application start time in Unix milliseconds, version "1". The RM lowercases application tags, so lowercase flow names and versions in REST queries. Entity types seen include `YARN_APPLICATION`, `YARN_APPLICATION_ATTEMPT`, `YARN_CONTAINER`, `YARN_FLOW_RUN`, `YARN_FLOW_ACTIVITY`.

Writing is only possible from inside a YARN application (no off-cluster client).

Verify: `GET /ws/v2/timeline/apps/<app id>` on the reader returns the `YARN_APPLICATION` entity.

## Checked
2026-11-08. Read in full: the Timeline Service v.2 page (the stable URL served Hadoop 3.3.5, published 2023-03-15), including the REST API section and example responses. Confirmed: all settings, defaults, HBase versions, coprocessor and schema steps, flow context defaults and the lowercasing note. Changed: removed the claim that the `-s` shorthand is separate from `-skipExistingTable`, and added reader daemon and REST path details from the page.
Method: documentation only; no commands were run.
