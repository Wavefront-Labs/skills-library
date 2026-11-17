---
id: computing-software.qa-testing-engineering.selenium.grid-cloud-and-dockerized-cross-browser-execution
name: grid-cloud-and-dockerized-cross-browser-execution
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenium, selenium-grid, docker, docker-compose, browserstack, sauce-labs, lambdatest, remotewebdriver, capabilities, w3c-capabilities, cross-browser-testing, parallel-execution, video-recording, ci, scalability, grid-ui, node-registration, cloud-device-farm]
level: advanced
status: gated
description: "Run Selenium across real browser/OS combinations at scale: a Dockerized Grid for CI-local parallelism, and cloud grids (BrowserStack/Sauce Labs) for OS/device coverage you can't host."
sources:
  - https://www.selenium.dev/documentation/grid/getting_started/
  - https://www.selenium.dev/documentation/webdriver/troubleshooting/upgrade_to_selenium_4/
  - https://github.com/SeleniumHQ/docker-selenium/blob/trunk/README.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Selenium Grid, Docker, and cloud cross-browser execution

**Goal:** run the same WebDriver suite across many browser/OS combinations in
parallel, without each test fighting for the one locally installed browser.

## 1. Selenium Grid's architecture
A **Hub/Router** receives test sessions and routes them to registered **Nodes**,
each running one or more browser instances. Since Selenium 4, Grid is a single
jar/image with distinct roles (`standalone` for one machine, or
`hub`+`node`+`router` for a distributed setup) — most teams only need
`standalone` locally and a cloud provider for real scale, reserving a self-hosted
distributed Grid for cost-sensitive, high-volume, self-hosted CI fleets.

## 2. Dockerized Grid for CI-local parallelism
```yaml
# docker-compose.yml (pin a full tag: the docker-selenium README says to always use one)
services:
  chrome: { image: "selenium/standalone-chrome:<full-tag>", shm_size: 2gb }
  firefox: { image: "selenium/standalone-firefox:<full-tag>", shm_size: 2gb }
```
Point `RemoteWebDriver` at each container's `4444` port. **Always set `shm_size`**
— the docker-selenium README calls `--shm-size="2g"` a known workaround to
stop browsers crashing inside a container (the value is arbitrary but known to
work; tune it for your case). Recreate containers between CI runs rather than
reusing a long-lived Grid so browser state does not accumulate.

## 3. Cloud grids (BrowserStack, Sauce Labs, LambdaTest)
Needed for OS/device combinations you can't reasonably host (real iOS/Android,
older Safari, Edge IE-mode targets). Point `RemoteWebDriver` at the vendor's hub
URL with vendor-specific capabilities. The key names, platform strings and build
tagging options are vendor-defined (gated: unconfirmed, source is paywalled or blocked). Vendor documentation sites were not read in this review.
```python
options = webdriver.SafariOptions()
options.set_capability('bstack:options', {'projectName': 'checkout', 'buildName': run_id})
driver = webdriver.Remote(command_executor=HUB_URL, options=options)
```
Tag every run with a build identifier if the vendor supports one, so failures can be filtered to a pipeline run.

## 4. The W3C capabilities gotcha
Selenium 4 uses the W3C WebDriver standard and removed the legacy protocol. The
standard capabilities are `browserName`, `browserVersion`, `platformName`,
`acceptInsecureCerts`, `pageLoadStrategy`, `proxy`, `timeouts` and
`unhandledPromptBehavior`; any other capability needs a vendor prefix, and
capabilities that are not W3C compliant can stop the session from starting. Put
vendor settings under the vendor's prefixed key (for example `bstack:options`,
`sauce:options`) rather than flat at the top level; the exact key names are vendor-defined (gated: unconfirmed, source is paywalled or blocked).

## 5. Parallelism and resource limits
Parallel RemoteWebDriver sessions on a self-hosted Grid are bounded by node slots: new
session requests wait in the queue until `--session-request-timeout` (default 300 s).
The recommended maximum sessions per node is one per processor. Cloud plans have
their own concurrency limits (gated: unconfirmed, source is paywalled or blocked).
Check limits before scaling a CI matrix up.

## Verify
- [ ] Docker browser containers have `shm_size` explicitly set (2g is the documented value).
- [ ] Containers recreated fresh per CI run, not reused across runs.
- [ ] Vendor capabilities nested under the correct prefixed key, confirmed in the vendor dashboard.
- [ ] Every cloud session tagged with a build/run identifier for triage.
- [ ] CI matrix concurrency checked against the actual node or plan session limit.

## Checked

Checked 2026-10-25 against the Selenium documentation source (seleniumhq.github.io, pushed 2026-10-23, examples tracking Selenium 4.51) and the docker-selenium repository (pushed 2026-10-20, README, ENV_VARIABLES.md and the selenium-grid chart README and values.yaml, images tagged 4.51.0-20261010). Confirmed: Grid roles and standalone/hub/node modes, the `--shm-size="2g"` guidance and full-tag advice, the W3C standard capability list, the vendor-prefix requirement and that non-compliant capabilities can fail session creation, session queue timeout default and the per-processor session recommendation. Not confirmed: BrowserStack, Sauce Labs and LambdaTest capability keys, platform strings and plan concurrency limits, because their documentation is not in a public GitHub repository. Corrected: unprefixed capabilities are not silently dropped; the Selenium docs say they can fail the session. Removed: the Chrome error strings and the `:latest` image tags.

Method: documentation only; no commands were run.
