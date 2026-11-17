---
id: computing-software.software-engineering.clojure.tools-logging-slf4j-logback-and-timbre
name: tools-logging-slf4j-logback-and-timbre
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, logging, tools.logging, slf4j, logback, timbre, mulog, log-levels, structured-logging, mdc, logging-tools-logging, clojure-logging]
level: practitioner
status: docs-checked
description: "Log with clojure.tools.logging (level macros, throwable-first, f variants, spy), select the backend with the factory property, and know Timbre as the pure-Clojure alternative."
sources: ["https://github.com/clojure/tools.logging", "https://clojure.github.io/tools.logging/", "https://github.com/taoensso/timbre"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging

**Goal:** consistent, searchable, configurable logs.

```clojure
(require '[clojure.tools.logging :as log])
(log/info "started" {:port 3000})
(log/debugf "user %s" id)                       ; format variants end in f
(log/error e "failed to save" id)               ; pass the Throwable FIRST to log its stack trace
(log/spy :info (compute))                       ; log and return a value
```
- tools.logging only provides the macros and delegates to a backend chosen when `clojure.tools.logging` is first loaded. Levels, formatting and appenders are configured in the backend, which is out of scope for the library.
- Backend selection: set the system property `clojure.tools.logging.factory` to a no-arg function returning a `clojure.tools.logging.impl/LoggerFactory`, e.g. `-Dclojure.tools.logging.factory=clojure.tools.logging.impl/slf4j-factory`. If unset, the first of SLF4J, Apache Commons Logging, Log4J 2, Log4J and java.util.logging that loads is used.
- The logger name is the current namespace (`*ns*`), so backends can set levels per namespace; configure the backend to display the logger name.
- Messages are evaluated only when the level is enabled. Inside a running STM transaction the call is made through an agent.
- `log-capture!` redirects `System.out`/`System.err` to the log, and `with-logs` binds `*out*`/`*err*`.
- Timbre is a pure Clojure/Script logging library configured with one Clojure config map; it can interoperate with tools.logging and SLF4J v2. Its README recommends Telemere to new users.
- Do not log secrets or full request bodies; redact tokens and personal data.

## Failure modes
- Transitive dependencies pull in several logging implementations and the wrong one is auto-selected: set the factory system property.
- The README warns that a backend using stack inspection instead of the passed logger name prints unhelpful names.

## Self-check
Set the backend's level to DEBUG for your namespace only (the logger name) and verify other namespaces stay quiet.

## Checked
2026-11-03. Confirmed against the tools.logging README and API page (log macros, f variants, throwable-first signature, spy, logger name from *ns*, factory system property and auto-selection order, log-capture!/with-logs, agent use in transactions) and the Timbre README (pure Clojure/Script, config map, tools.logging and SLF4J v2 interop, Telemere recommendation). Removed: Logback artifact and XML examples, MDC, JSON encoders, mulog, the println remark and the multiple-SLF4J-bindings warning (not in the pages read).
Method: documentation only; no commands were run.
