---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-appsec-waf-overview-and-setup
name: crowdsec-appsec-waf-overview-and-setup
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [appsec, waf, virtual-patching, appsec-datasource, inband, outofband, owasp-crs]
level: practitioner
status: docs-checked
description: "What the CrowdSec AppSec component is, how in-band and out-of-band rules differ, and the setup checklist that avoids the common mistakes."
sources: ["https://docs.crowdsec.net/docs/appsec/intro", "https://docs.crowdsec.net/docs/appsec/troubleshooting"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The AppSec component turns the Security Engine into a WAF: virtual patching, legacy ModSecurity rules support, behaviour detection and bot detection. Remediation components in a web server or reverse proxy (Nginx, Traefik, HAProxy and others) forward each request to the engine over a local HTTP interface, the engine evaluates AppSec rules, and the web server blocks or serves. One engine can protect many web servers because each forwards to the same AppSec `listen_addr`, so rules update in one place.

## In-band versus out-of-band

- **In-band**: evaluated first and can block the request immediately (the remediation component returns a 403 or a captcha challenge). A match appears in `cscli alerts list` and also raises an internal event.
- **Out-of-band**: evaluated in the background by dedicated workers, so it does not affect response time. A match emits an event that the engine processes like a log line; nothing is blocked immediately. If the workers cannot keep up, requests queue and, once the queue is full, skip out-of-band evaluation.

## Common gotchas

- Installing rules is not enough: you must enable the AppSec acquisition datasource and restart CrowdSec.
- The bouncer must support AppSec forwarding and point at the same `listen_addr` as the acquisition file.
- An in-band match returns an action for the current request (`ban` or `captcha`); longer bans come from scenarios and decisions.

## Verifying

The AppSec acquisition looks like `source: appsec`, `listen_addr: 127.0.0.1:7422`, `labels: type: appsec` and an `appsec_configs` list. Check the key works:

```console
cscli bouncers add appsec_test -k SOME_KEY
curl -I -X POST localhost:7422/ -H 'x-crowdsec-appsec-api-key: SOME_KEY' -H 'x-crowdsec-appsec-ip: 192.168.1.1' -H 'x-crowdsec-appsec-uri: /test' -H 'x-crowdsec-appsec-host: test.com' -H 'x-crowdsec-appsec-verb: GET'
```

200 means authenticated; 401 means a bad key or wrong setup. `cscli metrics` and `cscli appsec-rules inspect <rule>` show request and rule counts; set `log_level: debug` in the acquisition or config for runtime rule evaluation logs.

## Checked
2026-11-08. Confirmed against the AppSec introduction and WAF Troubleshooting pages: feature list, request flow, one-listen_addr model, gotchas, in-band versus out-of-band processing and post-processing, authentication test with the 200/401 results, `cscli metrics`, `cscli appsec-rules inspect`, cascading debug. Fixed: in-band matches also raise an event; removed OWASP CRS (not on the intro page) and the `cscli metrics show appsec` form.
Method: documentation only; no commands were run.
