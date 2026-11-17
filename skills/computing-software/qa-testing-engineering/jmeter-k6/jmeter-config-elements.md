---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-config-elements
name: jmeter-config-elements
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [http-request-defaults, jmeter-config-elements, http-header-manager, http-cookie-manager, cache-manager]
level: practitioner
status: docs-checked
description: "Configure JMeter config elements: HTTP Request Defaults, Header Manager, Cookie Manager, Cache Manager, DNS Cache Manager, User Defined Variables and their scoping."
sources:
  - https://jmeter.apache.org/usermanual/component_reference.html#config_elements
  - https://jmeter.apache.org/usermanual/test_plan.html#config_elements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Config elements (HTTP Request Defaults, managers, variables)

## HTTP Request Defaults
Set protocol, server, port, path prefix, content encoding, connect and response timeouts (milliseconds), "Retrieve All Embedded Resources" with parallel downloads, and implementation (HttpClient4) once. Samplers leave those fields blank and inherit.
Parameterise: Server `${__P(host,localhost)}`, Port `${__P(port,8080)}`, Protocol `${__P(proto,http)}`.

## HTTP Header Manager
Common headers (`Content-Type: application/json`, `Accept`, `Authorization: Bearer ${token}`). Place a test-plan-level manager for global headers and sampler-level ones for overrides: JMeter merges them, with the sampler-level value winning for the same header name.

## HTTP Cookie Manager
Add one per Thread Group to give each thread (virtual user) its own cookie store, like a browser. Options:
- "Clear cookies each iteration" to simulate new sessions per iteration.
- Cookie policy `standard` (the default since 3.0); `ignoreCookies` is equivalent to omitting the Cookie Manager.
- `CookieManager.save.cookies=true` (a JMeter property) stores received cookies as variables named `${COOKIE_<name>}`.

## HTTP Cache Manager
Emulates browser caching: conditional headers (If-Last-Modified, If-None-Match) are set for cached URLs and, with "Use Cache-Control/Expires header", GET requests with unexpired entries are not sent. "Clear cache each iteration" gives first-visit behaviour.

## DNS Cache Manager
Per-thread DNS resolution, a Static Host Table (map a host name to another host name or IP address) and "Clear cache each iteration". Works with the HttpClient 4 implementation; place it at the root of a Thread Group or Test Plan, not under a sampler.

## User Defined Variables
Processed at the start of the test, in plan order top to bottom, then copied to each thread as its initial variables. UDVs are shared between Thread Groups, so use distinct names; for per-thread or dynamic values use CSV Data Set or functions.

## Scoping
Config elements apply to samplers in their scope (same level and below); an element in an inner branch takes precedence over the same element in a parent branch. Exception: User Defined Variables are processed at the start of the test wherever they are placed.

## Gotchas
- More than one Cookie Manager in a sampler's scope: there is no way to choose which is used and cookies are not shared between managers; keep one.
- Set connect and response timeouts in Defaults so stuck requests do not hold threads.

## Verify
View Results Tree (debug run, 1 thread) shows inherited host/headers and cookies sent on later requests.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: Header Manager merge rule, Cookie Manager policy default and clear-per-iteration option, `CookieManager.save.cookies` and the COOKIE_ prefix, Cache Manager behaviour, DNS Cache Manager static host table, UDV processing, scoping precedence.

Method: documentation only; no commands were run.
