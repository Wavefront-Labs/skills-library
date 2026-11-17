---
id: computing-software.web-development.elysia.elysia-cron-schedule-jobs
name: elysia-cron-schedule-jobs
category: computing-software
field: web-development
product: elysia
tags: [cron, scheduling, plugin, croner]
level: practitioner
status: docs-checked
description: "Run, name, stop and schedule cron jobs inside an Elysia server with @elysia/cron, including predefined Patterns helpers."
sources:
  - https://elysiajs.com/plugins/cron.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run recurring work in-process and be able to stop it from a route.

1. Install: `bun add @elysia/cron`
2. Register a job:

```typescript
import { Elysia } from 'elysia'
import { cron } from '@elysia/cron'

new Elysia()
    .use(cron({
        name: 'heartbeat',
        pattern: '*/10 * * * * *',
        run() { console.log('Heartbeat') }
    }))
    .listen(3000)
```

This logs every 10 seconds. `name` registers the job on `store.cron` under that name; `pattern` is cron syntax with an OPTIONAL leading seconds field (second, minute, hour, day of month, month, day of week).

3. Extra options come from croner: `timezone` (like `Europe/Stockholm`), `startAt`, `stopAt`, `maxRuns`, `catch` (keep running after an unhandled error in the job), `interval` (minimum seconds between runs).

4. Stop a job from a route by reading it out of the store:

```typescript
.get('/stop', ({ store: { cron: { heartbeat } } }) => {
    heartbeat.stop()
    return 'Stop heartbeat'
})
```

5. Use predefined patterns instead of hand-written strings: `import { cron, Patterns } from '@elysia/cron'` then `pattern: Patterns.everySecond()`. Helper functions include `everySeconds(2)`, `everyMinutes(5)`, `everyHours(3)`, `everyHoursAt(3, 15)`, `everyDayAt('04:19')`, `everyWeekOn(Patterns.MONDAY, '19:30')`, `everyWeekdayAt('17:00')`, `everyWeekendAt('11:00')`. Aliases: `everySecond()`, `everyMinute()`, `hourly()`, `daily()` (midnight), `weekly()`, `monthly()`, `everyQuarter()`, `yearly()`. Constants include `EVERY_5_SECONDS` (`*/5 * * * * *`), `EVERY_30_MINUTES` (`0 */30 * * * *`), `EVERY_DAY_AT_MIDNIGHT` (`0 0 * * *`), `EVERY_WEEKDAY` (`0 0 * * 1-5`).

Gotchas:
- Constants differ in field count (5 vs 6 fields); the docs list `EVERY_MINUTE` as `*/1 * * * *` (no seconds field).

## Checked

Checked 2026-11-07 against the Elysia documentation source (plugins/cron.html); each claim, option name and default was compared with the page text. Removed the invented Verify step and the durable-scheduler gotcha (not on the page).

Method: documentation only; no commands were run.
