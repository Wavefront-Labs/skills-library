---
id: computing-software.web-development.micronaut.micronaut-scheduled-tasks
name: micronaut-scheduled-tasks
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, scheduled-tasks, scheduled, cron, fixed-rate, task-scheduler, thread-pool]
level: intro
status: docs-checked
description: "Schedule Micronaut background tasks with @Scheduled (fixedRate, fixedDelay, cron, initialDelay), TaskScheduler, config placeholders, thread pool and exception handling."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/aop/scheduling.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run bean methods periodically or once after startup.

Add `@Scheduled` to any bean method and set one of `fixedRate`, `fixedDelay` or `cron`. It needs the `micronaut-context` dependency (a transitive dependency of `micronaut-http`).

Bean scope matters: a `@Singleton` shares field state across runs; a `@Prototype` bean gets a new instance for each execution.

```java
@Scheduled(fixedRate = "5m")                 // every five minutes
void everyFiveMinutes() { ... }

@Scheduled(fixedDelay = "5m")                // five minutes after the previous run ends
void fiveMinutesAfterLastExecution() { ... }

@Scheduled(cron = "0 15 10 ? * MON")         // Mondays 10:15AM, server time zone
void everyMondayAtTenFifteenAm() { ... }

@Scheduled(initialDelay = "1m")              // once, one minute after startup
void onceOneMinuteAfterStartup() { ... }
```

## Configurable schedule

```java
@Scheduled(fixedRate = "${my.task.rate:5m}", initialDelay = "${my.task.delay:1m}")
void configuredTask() { ... }
```

Properties `my.task.rate` and `my.task.delay` override the defaults.

## Which schedule fired

A parameter of type `ScheduledExecution` receives the invocation: the scheduled method and the `@Scheduled` declaration that triggered the call (useful with several schedules on one method). `ScheduledExecution.current()` gives the same value during the call, including to interceptors, and is empty when the method is called directly. Other scheduled-method arguments are resolved from the bean context.

## Programmatic scheduling

```java
@Inject
@Named(TaskExecutors.SCHEDULED)
TaskScheduler taskScheduler;
```

## Thread pool

Tasks run on a `ScheduledExecutorService` with twice as many threads as available processors by default. Configure it:

```yaml
micronaut:
  executors:
    scheduled:
      type: scheduled
      core-pool-size: 30
```

## Exceptions

By default `DefaultTaskExceptionHandler` (a `TaskExceptionHandler`) just logs the exception. Replace it with your own bean:

```java
@Replaces(DefaultTaskExceptionHandler.class)
```

on a `TaskExceptionHandler` implementation (for example to send an email or shut down the context).

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.
