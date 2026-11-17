---
id: computing-software.qa-testing-engineering.selenium.grid-troubleshooting-session-queue
name: grid-troubleshooting-session-queue
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [session-queue, grid-troubleshooting, session-not-created, session-request-timeout, selenium-grid]
level: practitioner
status: docs-checked
description: "Troubleshoot Selenium Grid: queued and timed-out session requests, capability mismatches, nodes not registering, stale sessions and timeouts, using /status, logs and GraphQL."
sources:
  - https://www.selenium.dev/documentation/grid/advanced_features/endpoints/
  - https://www.selenium.dev/documentation/grid/configuration/cli_options/
  - https://www.selenium.dev/documentation/grid/advanced_features/graphql_support/
  - https://github.com/SeleniumHQ/docker-selenium/blob/trunk/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grid troubleshooting

## Symptom -> cause
| Symptom | Likely cause | Fix |
|---|---|---|
| Session creation fails after a long wait | request sat in the queue longer than `--session-request-timeout` (default 300s) | more slots, fewer parallel tests, raise timeout |
| Request never matches a node | browserName/version/platform or custom capability not offered by any node stereotype | check node stereotypes in the UI; drop overly specific caps |
| Nodes absent from UI | event bus ports 4442/4443 blocked, wrong `--hub`/host advertised | test connectivity; set `--host` / `SE_NODE_HOST` |
| Session dies mid-test | `--session-timeout` idle limit (300s) hit while test paused/debugging | raise for debugging; avoid long sleeps |
| Slots stuck "busy" | clients never called `quit()` | always quit in teardown; idle timeout cleans eventually |
| Chrome crashes | `/dev/shm` too small in Docker | `--shm-size=2g` |

## Tools
```bash
curl -s http://grid:4444/status
curl -s -X POST http://grid:4444/graphql -H 'Content-Type: application/json' \
  -d '{"query":"{ grid { sessionCount maxSession totalSlots sessionQueueSize } }"}'
curl -X DELETE http://grid:4444/session/<id>   # kill stuck session via the Grid URL
```
Queue: `GET /se/grid/newsessionqueue/queue`; clear: `DELETE /se/grid/newsessionqueue/queue` with `-H 'X-REGISTRATION-SECRET: <secret>'` if a secret is set.

## Logs
Start components with `--log-level FINE` (or, in docker-selenium, `SE_OPTS="--log-level FINE"`) and read the logs.

## Gotchas
- Keep the client-side HTTP timeout at least as long as `session-request-timeout`, so the client does not give up while a request is still queued.

## Verify
After fixes, queue size stays near zero under normal parallelism and sessionCount returns to 0 after the run.

## Checked

Checked 2026-10-25 against the Selenium documentation source (seleniumhq.github.io, pushed 2026-10-23, examples tracking Selenium 4.51) and the docker-selenium repository (pushed 2026-10-20, README, ENV_VARIABLES.md and the selenium-grid chart README and values.yaml, images tagged 4.51.0-20261010). Confirmed: `--session-request-timeout` and `--session-timeout` defaults (300 s), event bus ports 4442/4443, `--host` and `SE_NODE_HOST`, `--shm-size=2g` guidance, the Grid status, GraphQL, session delete (`DELETE /session/<id>` on the Grid URL and the node endpoint) and queue get/clear endpoints, `SE_OPTS`. Corrected: the registration-secret header was written `'X-REGISTRATION-SECRET;'` (sends an empty value). Removed as undocumented: the quoted exception messages, the jq pipeline and the demand-balancing advice.

Method: documentation only; no commands were run.
