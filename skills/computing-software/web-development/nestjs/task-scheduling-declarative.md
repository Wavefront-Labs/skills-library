---
id: computing-software.web-development.nestjs.task-scheduling-declarative
name: task-scheduling-declarative
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, schedule, cron, interval, timeout, scheduling]
level: practitioner
status: docs-checked
description: "Run NestJS code on a schedule with @nestjs/schedule using Cron, Interval and Timeout decorators, CronExpression, time zones and waitForCompletion."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/application/task-scheduling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install `npm install --save @nestjs/schedule` and import `ScheduleModule.forRoot()` once in the root module. Jobs start in `onApplicationBootstrap`.

```typescript
@Injectable()
export class TasksService {
  private readonly logger = new Logger(TasksService.name);

  @Cron('45 * * * * *')
  handleCron() { this.logger.debug('Called when the current second is 45'); }

  @Cron(CronExpression.EVERY_30_SECONDS)
  every30() {}

  @Interval(10000)
  handleInterval() {}

  @Timeout(5000)
  handleTimeout() {}
}
```

Cron fields: seconds (optional), minutes, hours, day of month, months, day of week. Examples: `0 */30 9-17 * * *` every 30 minutes between 9am and 5pm, `0 30 11 * * 1-5` weekdays at 11:30. A `Date` passed to `@Cron()` runs once, for example `@Cron(new Date(Date.now() + 10 * 1000))`.

`@Cron` options: `name`, `timeZone` (invalid zones throw), `utcOffset` (do not combine with `timeZone`), `waitForCompletion` (skip ticks while the previous run is active), `disabled`. Name intervals and timeouts as `@Interval('notifications', 2500)` and `@Timeout('notifications', 2500)` so they can be controlled later.

Every decorated method is wrapped in try-catch and errors are logged.

Gotchas:
- Call `forRoot()` in one module only. Each extra import registers every handler again, so three imports run each job three times.
- The scheduler runs jobs in every process. With several instances a nightly job runs once per instance; add `@OnOneInstance({ key: 'invoices:nightly-export' })` from `@nestjs/locks` next to the decorator, and `@WithoutOverlapping()` for jobs that may outlast their interval.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: Cron, Interval and Timeout decorators, Cron options, CronExpression, one-time Date, forRoot once, locks note (task-scheduling page). Removed: invented Verify step.

Method: documentation only; no commands were run.
