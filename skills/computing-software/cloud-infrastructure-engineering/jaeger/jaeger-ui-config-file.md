---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-ui-config-file
name: jaeger-ui-config-file
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, ui-config-json, uiconfig-function, dag-max-num-services, jaeger-ui-config]
level: practitioner
status: docs-checked
description: "Point jaeger_query at a JSON or JavaScript UI config file and set dependencies, monitor, themes, archive and tracking options."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/frontend-ui/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: customize Jaeger UI.

```
extensions:
  jaeger_query:
    ui:
      config_file: /path/to/config-ui.json   # or .js
```
JSON files hold the configuration object directly. A `.js` file must define a top-level function `UIConfig()` returning the object; if missing, the query service fails to load the configuration at startup. JS permits comments and custom functions, such as a `tracking.customWebAnalytics` factory.

Options and defaults:
- `themes.enabled`: theme toggle, default false (UI always light). When on, the choice persists in local storage and otherwise follows `prefers-color-scheme`.
- `dependencies.dagMaxNumServices`: default 200 (more services disables the DAG view); `dependencies.menuEnabled`: default true.
- `monitor.menuEnabled`: default false; `monitor.docsLink` and `monitor.emptyState` customize the Monitor tab.
- `archiveEnabled`: default false; needs archive storage configured in Query.
- `tracking.gaID` (default null; non-null enables Google Analytics) and `tracking.trackErrors` (default true, needs a valid tracker).
- `traceIdDisplayLength`: default 7.
- `criticalPathEnabled`: default true.
- `topTagPrefixes`: for example `["http.", "db."]` shows matching tags first.
- `traceGraph.layoutManagerMemory`: power of two, default 16MB; raise on "Cannot enlarge memory arrays".

## Checked

2026-11-03. Confirmed against the Frontend/UI Configuration page: config_file under jaeger_query.ui, JSON versus JavaScript UIConfig() format and the startup failure when it is missing, and the defaults for themes.enabled, dependencies.dagMaxNumServices and menuEnabled, monitor.menuEnabled, archiveEnabled, tracking.gaID and trackErrors, traceIdDisplayLength, criticalPathEnabled, topTagPrefixes and traceGraph.layoutManagerMemory. Nothing removed.
Method: documentation only; no commands were run.
