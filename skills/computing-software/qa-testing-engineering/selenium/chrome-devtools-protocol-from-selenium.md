---
id: computing-software.qa-testing-engineering.selenium.chrome-devtools-protocol-from-selenium
name: chrome-devtools-protocol-from-selenium
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenium-cdp, chrome-devtools-protocol, network-interception, geolocation-emulation, selenium-4]
level: practitioner
status: docs-checked
description: "Use the Chrome DevTools Protocol from Selenium 4: executeCdpCommand, network conditions, geolocation, basic auth, console and network events, and moving to BiDi."
sources:
  - https://www.selenium.dev/documentation/webdriver/bidi/cdp/
  - https://www.selenium.dev/documentation/webdriver/bidi/cdp/network/
  - https://www.selenium.dev/documentation/webdriver/bidi/cdp/logging/
  - https://www.selenium.dev/documentation/grid/configuration/cli_options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chrome DevTools Protocol from Selenium

**Goal:** reach Chromium features WebDriver lacks (network emulation, geolocation, console logs, request interception). CDP is Chromium-only and version-specific; The Selenium docs say CDP support is temporary until WebDriver BiDi has been implemented.

## Raw CDP commands (simplest, version-independent call)
```java
ChromeDriver driver = new ChromeDriver();
driver.executeCdpCommand("Emulation.setGeolocationOverride",
    Map.of("latitude", 51.5074, "longitude", -0.1278, "accuracy", 1));
```
Python: `driver.execute_cdp_cmd("Network.setCookie", cookie)`. Raw commands work on Chrome and Edge, do not support features needing bidirectional events, and require you to know the domain, method and parameter names from the CDP reference.

## DevTools domains with events (Java)
```java
DevTools devTools = ((HasDevTools) driver).getDevTools();
devTools.createSession();
devTools.send(org.openqa.selenium.devtools.v153.network.Network.enable(Optional.empty(), Optional.empty(), Optional.empty()));
devTools.addListener(org.openqa.selenium.devtools.v153.network.Network.responseReceived(),
    r -> { if (r.getResponse().getStatus() >= 500) failures.add(r.getResponse().getUrl()); });
```
Version-specific packages (`v153` in the current docs examples) must match the browser's CDP version; the docs warn CDP functionality depends on the browser version.

## Higher-level helpers (Selenium 4)
- Basic auth: `((HasAuthentication) driver).register(UsernameAndPassword.of("u", "p"))`.
- Console logs and JS errors: BiDi `LogInspector` (`onConsoleEntry`, `onJavaScriptLog`, `onJavaScriptException`).
- Network interception: `NetworkInterceptor` with `Route.matching(...)` to stub responses.

## Remote/Grid
Grid proxies CDP when `--enable-cdp` is true (the default); an admin can disable it if the network does not allow WebSockets.

## Gotchas
- CDP is for Chrome and Edge; guard with `if (driver instanceof HasDevTools)`.
- Prefer BiDi APIs where they exist, because CDP has no stable API.

## Verify
Emulation settings are observable in the page (e.g. geolocation shown), and the code degrades gracefully on non-Chromium browsers.

## Checked

Checked 2026-10-25 against the Selenium documentation source (pushed 2026-10-23; Java examples use devtools v153). Confirmed: `executeCdpCommand`/`execute_cdp_cmd` on Chrome and Edge only for unidirectional commands; `HasDevTools.getDevTools()`; `HasAuthentication.register`; `NetworkInterceptor` with `Route.matching`; `LogInspector` handlers; CDP is documented as temporary until WebDriver BiDi lands; Grid option `--enable-cdp` (default true). Corrected: stale `v129` package version, the invented `Events` helper and `se:cdp` capability wording. Removed: the example network emulation and blocked-URL commands, which the docs do not show.

Method: documentation only; no commands were run.
