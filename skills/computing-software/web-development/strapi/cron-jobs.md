---
id: computing-software.web-development.strapi.cron-jobs
name: cron-jobs
category: computing-software
field: web-development
product: strapi
tags: [strapi, cron, node-schedule, scheduling, cron-tasks, server-config]
level: practitioner
status: docs-checked
description: "Schedule functions in Strapi with cron-tasks.js in object format and enable them via cron.enabled in config/server."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/cron.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cron jobs

Powered by `node-schedule`. Format has 6 fields; the leading seconds field is optional: second (0-59), minute, hour, day of month, month (1-12), day of week (0-7, 0 or 7 is Sunday).

## Define (object format, recommended)
```js
module.exports = {
  /**
   * Simple example.
   * Every monday at 1am.
   */
  myJob: {
    task: ({ strapi }) => {
      // Add your own logic here (e.g. send a queue of email, create a database backup, etc.).
    },
    options: {
      rule: "0 0 1 * * 1",
    },
  },
};
```

`options` can also hold `tz` (e.g. `"Asia/Dhaka"`), `start`/`end` dates, or be a single `Date` to run once. The key format (`"0 0 1 * * 1": ({ strapi }) => {}`) makes an anonymous job that can cause issues disabling it or with some plugins.

## Enable
```js
const cronTasks = require("./cron-tasks");
module.exports = ({ env }) => ({
  host: env("HOST", "0.0.0.0"),
  port: env.int("PORT", 1337),
  cron: {
    enabled: true,
    tasks: cronTasks,
  },
});
```

The `cron.enabled` option must be `true` in `config/server`. Use `strapi.cron.add` to add jobs from custom code and `strapi.cron.remove` to remove them (jobs using the key as the rule cannot be removed).

## Checked

2026-11-04: checked against the Strapi docs page Cron jobs (configurations/cron). Confirmed: node-schedule, field list and ranges with optional seconds, object-format example, `tz`, `start`/`end`, single `Date`, key-format warning, `cron.enabled` and `tasks` in server config, `strapi.cron.add`. Removed: the claim that `cron.enabled` defaults to `false`, which the page does not state. Added: `strapi.cron.remove` and its key-format limitation from the page.

Method: documentation only; no commands were run.
