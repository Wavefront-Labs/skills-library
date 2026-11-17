---
id: computing-software.messaging-and-integration.apache-activemq-artemis.critical-analyzer
name: critical-analyzer
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,critical-analyzer,critical-analyzer-policy,critical-analyzer-timeout,halt,shutdown,watchdog,activemq-artemis]
level: advanced
status: docs-checked
description: "Let the broker halt or shut itself down if queue delivery, journal storage or paging stalls, using critical-analyzer timeout, check period and policy LOG, HALT or SHUTDOWN."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/critical-analysis.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Critical analyzer

**Goal:** a safeguard that stops an unhealthy broker (bugs, IO errors, memory or CPU starvation) instead of letting it hang. It measures response time in queue delivery (adding to the queue), journal storage and paging operations; beyond the timeout the broker is deemed unstable and acts.

## Settings in broker.xml
| name | meaning | default |
|---|---|---|
| `critical-analyzer` | enable the analysis | `true` |
| `critical-analyzer-timeout` | response time limit | 120000 ms |
| `critical-analyzer-check-period` | how often to check | half the timeout |
| `critical-analyzer-policy` | `LOG`, `HALT` or `SHUTDOWN` | `LOG` |

The code default is `LOG`, but the generated `broker.xml` sets `HALT`, because the VM cannot be halted when the broker is embedded or in a multi-tenant host.

## What you see
- `HALT`: `AMQ224079: The process for the virtual machine will be killed, as component ... is not responsive`.
- `SHUTDOWN`: `AMQ224080: The server process will now be stopped ...`.
- `LOG`: `AMQ224081: The component ... is not responsive` at WARN.
A thread dump is logged (`AMQ222199`, between `AMQ119001` and `AMQ119003`). With an unwell system there is no guarantee that a stop will complete.

## Checked

Method: docs-checked 2026-11-09 against critical-analysis.adoc (read in full). Removed the Verify step.
