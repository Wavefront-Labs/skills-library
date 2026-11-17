---
id: computing-software.qa-testing-engineering.selenium.grid-toml-configuration
name: grid-toml-configuration
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [grid-toml, selenium-grid, node-stereotypes, grid-configuration, max-sessions]
level: practitioner
status: docs-checked
description: "Configure Selenium Grid 4 with TOML: node stereotypes and max sessions, relay nodes to Appium or cloud, session timeouts, Docker node config, and verifying registration."
sources:
  - https://www.selenium.dev/documentation/grid/configuration/toml_options/
  - https://www.selenium.dev/documentation/grid/configuration/cli_options/
  - https://www.selenium.dev/documentation/grid/architecture/
  - https://github.com/SeleniumHQ/docker-selenium/blob/trunk/ENV_VARIABLES.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grid TOML configuration and node stereotypes

**Goal:** a Grid whose nodes advertise exactly the browsers they can run, at the right concurrency.

## Node with explicit stereotypes
```toml
# node.toml
[node]
detect-drivers = false
max-sessions = 4
session-timeout = 300            # seconds idle before a session is killed

[[node.driver-configuration]]
display-name = "Chrome"
stereotype = '{"browserName": "chrome", "browserVersion": "<major-version>", "platformName": "linux"}'
max-sessions = 4

[[node.driver-configuration]]
display-name = "Firefox"
stereotype = '{"browserName": "firefox", "platformName": "linux"}'
max-sessions = 2
webdriver-executable = "/opt/geckodriver"
```
```bash
java -jar selenium-server-4.x.jar node --config node.toml --hub http://hub.example.test:4444
```
`override-max-sessions = true` lets `max-sessions` exceed the number of processors (the recommended maximum; default `false`).

## Hub / standalone options
```toml
[sessionqueue]
session-request-timeout = 300    # how long a request waits in the queue
session-retry-interval = 15       # milliseconds

[router]
username = "admin"               # basic auth on the Grid UI/API
password = "<from-secret>"

[distributor]
slot-selector = "org.openqa.selenium.grid.distributor.selector.DefaultSlotSelector"
```

## Relay to Appium or a service
```toml
[relay]
url = "http://appium:4723"
status-endpoint = "/status"
configs = ["5", '{"browserName": "chrome", "platformName": "android", "appium:platformVersion": "14"}']
```

## Docker
docker-selenium images take env vars (`SE_NODE_MAX_SESSIONS`, `SE_NODE_SESSION_TIMEOUT`, `SE_NODE_OVERRIDE_MAX_SESSIONS`) or a mounted `config.toml` (the default path inside the images is `/opt/selenium/config.toml`).

## Verify registration
- Grid UI at `/ui` shows nodes and slots.
- `curl http://hub:4444/status` lists each node's slots and stereotypes.
- Request a session with the stereotype's capabilities; mismatched capabilities wait in the queue until `session-request-timeout`.

## Gotchas
- A stereotype is the minimal set of capabilities a slot supports; custom capabilities must be set on every node and included in every session request.
- The recommended `max-sessions` is one per processor; `override-max-sessions` allows more but session stability may suffer.

## Verify
Every node shows the expected slots at `/status`, and a test matrix requesting each stereotype gets a session within seconds.

## Checked

Checked 2026-10-25 against the Selenium documentation source (seleniumhq.github.io, pushed 2026-10-23, examples tracking Selenium 4.51) and the docker-selenium repository (pushed 2026-10-20, README, ENV_VARIABLES.md and the selenium-grid chart README and values.yaml, images tagged 4.51.0-20261010). Confirmed: `[node] detect-drivers`, `[[node.driver-configuration]]` keys (`display-name`, `stereotype`, `max-sessions`, `webdriver-executable`), `session-timeout` default 300, `[sessionqueue] session-request-timeout` (default 300) and `session-retry-interval` (default 15 ms), `[router] username`/`password`, `[distributor] slot-selector` default class, `[relay]` `url`/`status-endpoint`/`configs`, docker-selenium variables `SE_NODE_MAX_SESSIONS`, `SE_NODE_SESSION_TIMEOUT`, `SE_NODE_OVERRIDE_MAX_SESSIONS`. Corrected: stale pinned Chrome version replaced by a placeholder, the exact-match stereotype claim. Removed: the jq pipeline.

Method: documentation only; no commands were run.
