---
id: computing-software.messaging-and-integration.node-red.node-red-settings-file-and-logging
name: node-red-settings-file-and-logging
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, settings-js, logging, log-level, metrics, audit, user-directory, flowfilepretty, custom-logger]
level: practitioner
status: docs-checked
description: "Configure Node-RED logging in settings.js: console logger level, metrics and audit output, and custom logger modules with a handler function."
sources: ["https://nodered.org/docs/user-guide/runtime/logging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Node-RED logging

Node-RED's logger writes to the console and supports custom logger modules. It is configured under the `logging` property of the settings file:

```javascript
logging: {
    console: { level: "info", metrics: false, audit: false }
}
```

`level` takes `fatal`, `error`, `warn`, `info`, `debug`, `trace` or `off`. Other than `off`, each level includes the more severe ones (`warn` includes `error` and `fatal`). `metrics: true` outputs flow execution and memory information: a `[metric]` line for each receive and send event in a node, and memory usage (`runtime.memory.rss`, `heapTotal`, `heapUsed`) every 15 seconds. `audit: true` logs Admin HTTP API access events, including the endpoint, IP address and timestamp, and the requesting user when `adminAuth` is enabled.

A custom logger is another entry in `logging` (the only reserved name is `console`) with the same `level`, `metrics` and `audit` properties plus a `handler` function. `handler(settings)` is called once at start-up and must return a function that is called with each log message, for example `function(msg) { console.log(msg.timestamp, msg.event); }`; this can send metrics to an external monitoring system. On a Raspberry Pi installed with the install script, the `node-red-log` command shows the service log.

## Checked

2026-11-04. Confirmed against the Node-RED user guide page Logging. Removed: the whole settings-file location and editing paragraph (user directory, --settings, 'Settings file' log line, flowFilePretty, comma advice), which the cited page does not cover.

Method: documentation only; no commands were run.
