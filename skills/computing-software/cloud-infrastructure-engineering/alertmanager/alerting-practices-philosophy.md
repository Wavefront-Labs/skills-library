---
id: computing-software.cloud-infrastructure-engineering.alertmanager.alerting-practices-philosophy
name: alerting-practices-philosophy
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, alerting-practices, symptom-alerts, metamonitoring]
level: intro
status: docs-checked
description: "Prometheus alerting practices: alert on symptoms, naming, online serving, offline processing, batch jobs, capacity and metamonitoring of Alertmanager."
sources: ["https://prometheus.io/docs/practices/alerting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alerting practices

Summary from the Prometheus docs: keep alerting simple, alert on symptoms, have good consoles to pinpoint causes, and avoid pages where there is nothing to do.

- Naming: no strict restrictions; names may contain any Unicode characters, but the community uses CamelCase.
- Alert on end-user pain, as few alerts as possible. Link alerts to consoles. Allow slack for small blips.
- Online serving: alert on high latency and error rates as high up the stack as possible. Page on latency at one point in the stack only. Page on user-visible errors; add pages for non-user-visible failures that are still severe, such as losing money.
- Offline processing: page when data takes too long to get through the system.
- Batch jobs: page if the job has not succeeded recently enough to cause user-visible problems, generally at least enough time for 2 full runs. For a job running every 4 hours taking an hour, 10 hours is reasonable.
- Capacity: nearing capacity often needs human intervention before an outage.
- Metamonitoring: alert that Prometheus servers, Alertmanagers, PushGateways and other monitoring components are running correctly. A blackbox test that alerts travel from PushGateway to Prometheus to Alertmanager to email beats separate alerts on each. External blackbox monitoring catches invisible problems and is a fallback if internal systems fail.

## Checked

2026-11-08. Confirmed against the Prometheus Alerting practices page: naming, what to alert on, online serving, offline processing, batch jobs (2 full runs, 10 hours for a 4-hourly 1-hour job), capacity and metamonitoring.

Method: documentation only; no commands were run.
