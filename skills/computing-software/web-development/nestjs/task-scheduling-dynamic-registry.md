---
id: computing-software.web-development.nestjs.task-scheduling-dynamic-registry
name: task-scheduling-dynamic-registry
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, schedule, schedulerregistry, cronjob, dynamic-jobs]
level: advanced
status: docs-checked
description: "Create, inspect, stop and delete cron jobs, intervals and timeouts at runtime in NestJS using SchedulerRegistry from @nestjs/schedule."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/application/task-scheduling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Inject `SchedulerRegistry` (from `@nestjs/schedule`): `constructor(private schedulerRegistry: SchedulerRegistry) {}`. A declarative job is reachable by the `name` set in its decorator options.

Cron:

```typescript
const job = this.schedulerRegistry.getCronJob('notifications');
job.stop();
console.log(job.lastDate());
```

`CronJob` methods: `stop()`, `start()`, `setTime(time: CronTime)`, `lastDate()` (null before the first run), `nextDate()` (a Luxon `DateTime`; use `toJSDate()`), `nextDates(count)`.

Create (import `CronJob` from `cron`):

```typescript
const job = new CronJob(`${seconds} * * * * *`, () => this.logger.warn(`time for job ${name}`));
this.schedulerRegistry.addCronJob(name, job);
job.start();
```

Delete with `deleteCronJob(name)`; list with `getCronJobs()` (a `Map`).

Intervals and timeouts hold the native handles:

```typescript
const interval = setInterval(callback, milliseconds);
this.schedulerRegistry.addInterval(name, interval);
clearInterval(this.schedulerRegistry.getInterval('notifications'));
this.schedulerRegistry.deleteInterval(name);
this.schedulerRegistry.getIntervals();   // names
```

The timeout API is the same with `addTimeout`, `getTimeout`, `deleteTimeout`, `getTimeouts`.

Gotchas:
- `nextDate()` throws if a job has already fired and has no future date, so wrap it in try/catch when listing.
- Remember to inject `SchedulerRegistry` before accessing it, and import `CronJob` from the `cron` package.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: SchedulerRegistry usage, CronJob methods, nextDate throwing, addCronJob, intervals and timeouts API, cron import warning (task-scheduling page). Removed: invented Verify step.

Method: documentation only; no commands were run.
