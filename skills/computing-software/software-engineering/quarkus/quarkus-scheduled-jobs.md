---
id: computing-software.software-engineering.quarkus.quarkus-scheduled-jobs
name: quarkus-scheduled-jobs
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, scheduler, scheduled, cron, periodic-tasks]
level: intro
status: docs-checked
description: "Run periodic tasks in Quarkus with the scheduler extension: @Scheduled every= and cron= expressions, config-driven cron, cron syntax choice, Quartz for clusters."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/scheduler.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduling periodic tasks in Quarkus

Add the extension: `quarkus extension add scheduler` (dependency `io.quarkus:quarkus-scheduler`). For a clustered scheduler use the Quartz extension instead.

## Declare jobs

Put `@Scheduled` methods on a bean (the guide uses `@ApplicationScoped`).

```java
@ApplicationScoped
public class CounterBean {
    private AtomicInteger counter = new AtomicInteger();

    @Scheduled(every="10s")
    void increment() { counter.incrementAndGet(); }

    @Scheduled(cron="0 15 10 * * ?")
    void cronJob(ScheduledExecution execution) {
        System.out.println(execution.getScheduledFireTime());
    }

    @Scheduled(cron = "{cron.expr}")
    void cronJobWithExpressionInConfig() { }
}
```

- `every="10s"` runs every 10 seconds; the cron example runs at 10:15am daily.
- A method may take a `ScheduledExecution` parameter (`getScheduledFireTime()`).
- `cron = "{cron.expr}"` reads the expression from `application.properties`, e.g. `cron.expr=*/5 * * * * ?`.

## Behaviour to know

- The scheduler uses 10 worker threads. If none is free, the invocation is re-scheduled by default, meaning it runs as soon as possible.
- Each invocation is independent of the status or result of the previous one.
- Cron syntax defaults to Quartz style. Switch with `quarkus.scheduler.cron-type=unix`.

## Try it

Run dev mode (`quarkus dev`), then `curl localhost:8080/count` a few times; the counter grows. The console prints "Cron expression configured in application.properties" each time the config-driven cron fires.

## Checked

2026-11-07. Matched against the text (with includes) of: scheduler.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the wrong CLI order `quarkus add extension scheduler`; the page's devtools include gives `quarkus extension add scheduler`.

Method: documentation only; no commands were run.
