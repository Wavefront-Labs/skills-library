---
id: computing-software.software-engineering.spring-boot.task-pools-and-schedulers
name: task-pools-and-schedulers
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, task-scheduling, enablescheduling, threadpooltaskscheduler, spring-task-execution-pool, virtual-threads]
level: practitioner
status: docs-checked
description: "Tune the auto-configured thread pool with spring.task.execution.pool, configure the scheduler with spring.task.scheduling and use the task executor and scheduler builders."
sources:
  - https://docs.spring.io/spring-boot/reference/features/task-execution-and-scheduling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Executor pool: an auto-configured `ThreadPoolTaskExecutor` has 8 core threads that grow and shrink with load. Tune under `spring.task.execution`:
```yaml
spring:
  task:
    execution:
      pool:
        max-size: 16
        queue-capacity: 100
        keep-alive: "10s"
```
This gives a bounded queue; when it is full (100 tasks) the pool grows to at most 16 threads. Shrinking is more aggressive: idle threads are reclaimed after 10 seconds instead of 60.

Scheduler: a scheduler is auto-configured when associated with scheduled task execution (for example `@EnableScheduling`). With virtual threads enabled (Java 21+ and `spring.threads.virtual.enabled=true`) it is a `SimpleAsyncTaskScheduler` using virtual threads, which ignores any pooling properties. Otherwise it is a `ThreadPoolTaskScheduler`, which uses one thread by default; tune under `spring.task.scheduling`:
```yaml
spring:
  task:
    scheduling:
      thread-name-prefix: "scheduling-"
      pool:
        size: 2
```

Builders: `ThreadPoolTaskExecutorBuilder`, `SimpleAsyncTaskExecutorBuilder`, `ThreadPoolTaskSchedulerBuilder` and `SimpleAsyncTaskSchedulerBuilder` beans are available to create custom executors or schedulers. The `SimpleAsync*` builders are auto-configured to use virtual threads when they are enabled.

## Checked

2026-11-07. Read features/task-execution-and-scheduling.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
