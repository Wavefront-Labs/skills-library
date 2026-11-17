---
id: computing-software.database-administration.influxdb.send-alert-emails-with-a-task
name: send-alert-emails-with-a-task
category: computing-software
field: database-administration
product: influxdb
tags: [alerting, email, sendgrid, tasks, http-post, secrets]
level: practitioner
status: docs-checked
description: "Send alert emails through a third-party service by running a task that queries crit statuses in _monitoring and calls an email API with http.post."
sources:
  - https://docs.influxdata.com/influxdb/v2/monitor-alert/send-email/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A task queries the `statuses` measurement in `_monitoring` for crit statuses and posts to a third-party provider's HTTP API. The page documents SendGrid, Amazon SES, Mailjet and Mailgun, and its examples alert when more than 3 critical statuses occur since the previous task run.

Sketch:

```js
import "influxdata/influxdb/secrets"
import "http"

apiKey = secrets.get(key: "SENDGRID_API_KEY")
// from(bucket: "_monitoring") |> range(start: -task.every)
//   |> filter(fn: (r) => r._measurement == "statuses" and r._level == "crit")
// then http.post(url: ..., headers: ..., data: ...) per row
```

The page's examples read keys with `secrets.get()` rather than hard-coding them (see the secrets skills). It says to set the query range to the same interval the task is scheduled to run, for example `range(start: -task.every)`. The script above is abbreviated; consult the page for provider-specific headers and bodies. For Amazon SES the page notes the URL, authentication and request structure may vary.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 "Send alert email" page, lines 574-700 read from the downloaded text.

Confirmed: provider list, `_monitoring` `statuses` query with `_level`, `range(start: -task.every)`, `secrets.get()`, `http.post()`. Reworded the description, which wrongly claimed OSS lacks native email (the page does not say so).
