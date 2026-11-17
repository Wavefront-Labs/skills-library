---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.logs-as-event-streams
name: logs-as-event-streams
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, 12-factor-app, twelve-factor, logs-as-event-streams, stdout-logging, log-routing, log-aggregation]
level: practitioner
status: docs-checked
description: "Apply factor XI: write the event stream, unbuffered, to stdout and let the execution environment capture, route and archive it; apps do not manage log files."
sources: ["https://12factor.net/logs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factor XI: treat logs as event streams

Logs are the stream of aggregated, time-ordered events collected from the output streams of all running
processes and backing services. In raw form they are typically text with one event per line (exception
backtraces may span several lines). They have no fixed beginning or end and flow continuously while the app runs.
A logfile on disk is only one output format.

**Rule:** a twelve-factor app never concerns itself with routing or storage of its output stream. It does not
write to or manage logfiles. Each running process writes its event stream, unbuffered, to stdout.

## Steps
1. Remove logfile writing and log management from the app. Write to stdout, unbuffered.
2. In local development, watch the stream in the foreground of the terminal.
3. In staging and production, let the execution environment capture each process's stream, collate it with the
   app's other streams and route it to one or more destinations for viewing and long-term archival. The app can
   neither see nor configure those destinations. The page names Logplex and Fluentd as open-source log routers.
4. Send the stream to a log indexing and analysis system (the page names Splunk) or a general-purpose data
   warehouse (Hadoop/Hive) to find past events, graph trends such as requests per minute, and alert on
   user-defined heuristics such as errors per minute over a threshold.

## Gotchas
- Logging to a file from inside the app puts routing and storage back in the app's hands.
- The stream may also be routed to a file or watched by real-time tail; that is a choice for the environment,
  not the app.

## Verify
- [ ] The app writes no log files of its own.
- [ ] Output reaches the environment's log destination without any app-side configuration of that destination.

## Checked
2026-11-09. Confirmed against the 12factor.net Logs page (read in full). Removed claims and sources that were
not read or are not on the page: JSON field conventions and sample event, trace and span correlation,
OpenTelemetry and Fluent Bit routing, platform-specific capture on ECS, Cloud Run and App Service, PII redaction,
retention classes and Docker non-blocking log modes.
Method: docs-checked 2026-11-09 against https://12factor.net/logs (read in full); documentation only, no commands run.
