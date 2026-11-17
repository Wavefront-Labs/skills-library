---
id: computing-software.cloud-infrastructure-engineering.graylog.url-allowlist-management
name: url-allowlist-management
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [url-allowlist, outbound-requests, ssrf-protection, external-endpoints]
level: practitioner
status: docs-checked
description: "Graylog blocks outgoing HTTP requests to URLs not on its allowlist; know the required external endpoints and who can edit the list."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/url_allowlist.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# url allowlist management

Graylog checks all outgoing HTTP requests against a URL allowlist and blocks any URL without an approved entry. Only a Graylog administrator can modify it.

Required external endpoints, to permit through firewalls or proxies as your deployment needs:
- `downloads.graylog.org`: release binaries
- `packages.graylog2.org`: APT and YUM packages
- `update.graylog.org`: update checks shown in the UI
- `docs.graylog.org`: documentation links from the UI
- `graylog.org/post`: landing page content feed
- `license.graylog.com`: license validation

The page lists further optional endpoints. The page names alerts and HTTP-based data adapters as components that make outgoing requests; if one fails to call out, check the allowlist as well as the network firewall. Add entries under System > Configurations > URL Whitelist as Exact match or Regex (Java Pattern).

## Checked

2026-11-04. Confirmed against the URL Allowlist page (blocking behaviour, administrator requirement, endpoint list, add-entry steps). Replaced the unstated mention of inputs with the page's alerts and HTTP-based data adapters.

Method: documentation only; no commands were run.
