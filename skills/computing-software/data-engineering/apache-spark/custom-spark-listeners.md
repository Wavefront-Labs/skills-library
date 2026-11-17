---
id: computing-software.data-engineering.apache-spark.custom-spark-listeners
name: custom-spark-listeners
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark-listener, queryexecutionlistener, sparklistener, observability, lineage, spark-monitoring]
level: advanced
status: docs-checked
description: "Hook into Spark events with a custom SparkListener or QueryExecutionListener to emit job metrics, audit writes or capture lineage, and register them safely."
sources:
  - https://spark.apache.org/docs/latest/api/scala/org/apache/spark/scheduler/SparkListener.html
  - https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/util/QueryExecutionListener.html
  - https://spark.apache.org/docs/latest/configuration.html#spark-ui
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom SparkListener and QueryExecutionListener

**Use when:** you want per-job/per-stage metrics pushed to your monitoring system, an audit of every table written, or lineage (OpenLineage's Spark integration is itself a listener).

## SparkListener (scheduler events)
```scala
import org.apache.spark.scheduler._
class StageMetricsListener extends SparkListener {
  override def onStageCompleted(e: SparkListenerStageCompleted): Unit = {
    val i = e.stageInfo; val m = i.taskMetrics
    Metrics.emit("spark.stage", Map("stage" -> i.stageId.toString, "name" -> i.name),
      Map("runTimeMs" -> m.executorRunTime, "spillBytes" -> m.diskBytesSpilled,
          "shuffleReadBytes" -> m.shuffleReadMetrics.totalBytesRead,
          "failed" -> (if (i.failureReason.isDefined) 1 else 0)))
  }
  override def onApplicationEnd(e: SparkListenerApplicationEnd): Unit = Metrics.flush()
}
```
Register: `--conf spark.extraListeners=com.acme.StageMetricsListener` (class needs a no-arg or `SparkConf` constructor, jar on the driver classpath), or `spark.sparkContext.addSparkListener(new StageMetricsListener)` at runtime.

## QueryExecutionListener (SQL/DataFrame actions)
```scala
import org.apache.spark.sql.util.QueryExecutionListener
class WriteAudit extends QueryExecutionListener {
  def onSuccess(funcName: String, qe: org.apache.spark.sql.execution.QueryExecution, durationNs: Long): Unit =
    qe.analyzed.collect { case c: org.apache.spark.sql.execution.command.DataWritingCommand => c }
      .foreach(c => Audit.log(funcName, c.getClass.getSimpleName, durationNs))
  def onFailure(funcName: String, qe: org.apache.spark.sql.execution.QueryExecution, ex: Exception): Unit =
    Audit.fail(funcName, ex.getMessage)
}
```
Register with `spark.sql.queryExecutionListeners=com.acme.WriteAudit` or `spark.listenerManager.register(...)`.

## Rules
- Listener callbacks run on the single **listener bus thread** on the driver. Slow callbacks (synchronous HTTP calls) back up the queue and Spark drops events (the configuration page says to raise a queue's capacity if its events are dropped), which also breaks the UI. Hand off to a background executor/queue; never block.
- Tune `spark.scheduler.listenerbus.eventqueue.capacity` (default 10000) only after making callbacks fast.
- PySpark: `SparkListener` and `QueryExecutionListener` are JVM classes; register them through the configuration keys above.
- Exceptions in a listener are logged and swallowed; test it, or you silently lose metrics.

## Verify
- [ ] Run a sample job; metrics/audit records appear once per stage/write.
- [ ] Driver log has no dropped-event warnings under load.

## Checked

2026-10-28. Confirmed: spark.extraListeners (SparkConf or zero-argument constructor), spark.sql.queryExecutionListeners and the default eventqueue capacity of 10000 on the Spark configuration page. Removed: the quoted log line and the Python-registration claim.

Method: documentation only; no commands were run.
