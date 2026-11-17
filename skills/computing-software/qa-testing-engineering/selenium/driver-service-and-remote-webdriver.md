---
id: computing-software.qa-testing-engineering.selenium.driver-service-and-remote-webdriver
name: driver-service-and-remote-webdriver
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [driver-service, remotewebdriver, chromedriver-logs, service-args, selenium-manager]
level: practitioner
status: gated
description: "Configure Selenium driver services (path, port, logs, args) and RemoteWebDriver for Grid/cloud with client config, timeouts and capability passing."
sources:
  - https://www.selenium.dev/documentation/webdriver/drivers/service/
  - https://www.selenium.dev/documentation/webdriver/drivers/remote_webdriver/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Driver service, logs and RemoteWebDriver

## Service (local drivers)
```python
from selenium.webdriver.chrome.service import Service
service = Service(
    executable_path=None,            # None -> Selenium Manager resolves/downloads chromedriver
    port=0,                          # random free port
    service_args=["--verbose", "--append-log"],
    log_output="chromedriver.log",   # or subprocess.STDOUT
)
driver = webdriver.Chrome(service=service, options=options)
```
Ran: `Service(service_args=["--verbose", "--append-log"], log_output=<path>)` wrote a ~21 KB chromedriver log. Firefox uses `selenium.webdriver.firefox.service.Service` and Edge `selenium.webdriver.edge.service.Service` (Python names; not run).

Driver logs are where "session not created", crashes and version mismatches are explained.

## Selenium Manager
Shipped with every Selenium release as of 4.6 (Selenium Manager docs); it finds or downloads the browser driver (and browser, with the `browser_version` option). Override the driver with an explicit `executable_path` or the env var read by the Python service, `SE_CHROMEDRIVER` (`SE_GECKODRIVER`, `SE_EDGEDRIVER`); ran: `SE_CHROMEDRIVER` pointing at a missing file gave `NoSuchDriverException`, whereas `SE_DRIVER_PATH` had no effect. Offline mode is `SE_OFFLINE=true` (env form of `--offline`) for locked-down CI.

## RemoteWebDriver
```python
options = webdriver.ChromeOptions()
options.set_capability("se:name", "checkout test")       # Grid UI label
options.set_capability("se:recordVideo", True)            # dynamic grid video
driver = webdriver.Remote(command_executor="http://grid:4444", options=options)
```
The Grid labels `se:name` and `se:recordVideo` were not run (gated: unconfirmed, source is paywalled or blocked) (no Grid or Docker here). Client HTTP timeouts: Python `ClientConfig(remote_server_addr=..., timeout=300)` imports from `selenium.webdriver.remote.client_config` and returned `timeout == 300` (ran); the Selenium Python changelog lists "Remote connection use timeout from ClientConfig" in 4.26.1.

Upload local files to remote nodes: `driver.file_detector = LocalFileDetector()` (Python, from `selenium.webdriver.remote.file_detector`).

## Gotchas
- Always `driver.quit()` in teardown (not `close()`), or orphaned drivers/browsers pile up locally and sessions stay busy on Grid.
- The `desired_capabilities` argument is gone: `webdriver.Chrome(desired_capabilities={})` raised `TypeError ... unexpected keyword argument` on 4.51 (the Python changelog's 4.10.0 entry says significant deprecated code was removed); pass options objects.

## Verify
Driver log file is written; Grid UI shows the session with your `se:name`.
