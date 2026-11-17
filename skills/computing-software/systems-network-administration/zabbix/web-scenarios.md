---
id: computing-software.systems-network-administration.zabbix.web-scenarios
name: web-scenarios
category: computing-software
field: systems-network-administration
product: zabbix
tags: [web-monitoring, web-scenario, steps, variables, libcurl, web, scenario, http]
level: practitioner
status: docs-checked
description: "Monitor sites with multi-step web scenarios, variables, headers, retries and simulated logins."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/web_monitoring
  - https://www.zabbix.com/documentation/current/en/manual/web_monitoring/items
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A web scenario is one or more HTTP request steps executed in order by the server, or by the proxy if the host is proxied. The server needs cURL (libcurl) support. Create it from Data collection > Hosts (or Templates) > Web > Create web scenario; scenarios on templates apply to many hosts.

Collected for the scenario: average download speed, number of the failed step and last error message. Per step: download speed, response time and response code. Data feeds graphs, triggers and notifications.

You can check that a page contains a string, simulate a login and follow a path of clicks. HTTP and HTTPS are supported. Cookies persist during a single scenario run. Redirects are optionally followed, with a hard-coded maximum of 10.

Scenario options:
- Update interval with time suffixes and user macros. If a user macro changes (for example 5m to 30s), the next check still follows the previous value.
- Attempts: up to 10 retries per step on network problems.
- HTTP proxy in [protocol://][user[:password]@]host[:port] form (CURLOPT_PROXY).
- Variables {macro}=value, or extracted with regex:, jsonpath: or xmlxpath: prefixes, usable in step URLs and post variables.
- Headers, applied to all steps unless overridden.

Steps define URL (Unicode domains are punycode-converted), GET and POST variables (URL-encoded automatically), step variables that override scenario ones, and headers.

User macros in the scenario name stay unresolved in web item names.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (web_monitoring; web_monitoring/items): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
