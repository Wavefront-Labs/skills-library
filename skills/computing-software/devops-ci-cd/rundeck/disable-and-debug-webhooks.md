---
id: computing-software.devops-ci-cd.rundeck.disable-and-debug-webhooks
name: disable-and-debug-webhooks
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, webhook-debugging, webhooks-enabled, webhook-log, log4j]
level: practitioner
status: docs-checked
description: "Turn Rundeck webhooks off with a feature flag (including Docker) or log webhook events to a file with log4j to debug why a webhook did not fire."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/webhooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Webhooks are on by default as of 3.2.0.

Disable for WAR, Deb or RPM installs in `rundeck-config.properties`:

```properties
rundeck.feature.webhooks.enabled=false
```

For Docker set the environment variable `RUNDECK_FEATURE_WEBHOOKS_ENABLED=false`.

Debugging "why didn't my webhook do X": Runbook Automation (Enterprise) has a Webhook Debugger built into the webhook builder, useful with the Advanced Rule Processing handlers.

Alternatively log webhook events to a file (the page labels this the default log4j configuration):

```properties
log4j.logger.org.rundeck.webhook.events=INFO,webhook
log4j.additivity.org.rundeck.webhook.events=false
log4j.appender.webhook=org.apache.log4j.DailyRollingFileAppender
log4j.appender.webhook.file=${rundeck.log.dir}${file.separator}rundeck.webhook.log
log4j.appender.webhook.append=true
log4j.appender.webhook.layout=org.apache.log4j.PatternLayout
log4j.appender.webhook.layout.ConversionPattern=[%d{ISO8601}] %-5p %c{2} - %m%n
```

Gotcha: the page says `rundeck.webhooks.log` in one place but the appender writes `rundeck.webhook.log`; check the log directory for the real file name.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Webhooks: on by default as of 3.2.0, rundeck.feature.webhooks.enabled=false for WAR/Deb/RPM, RUNDECK_FEATURE_WEBHOOKS_ENABLED for Docker, the Webhook Debugger, the log4j block, and the rundeck.webhooks.log vs rundeck.webhook.log inconsistency. Nothing removed.

Method: documentation only; no commands were run.
