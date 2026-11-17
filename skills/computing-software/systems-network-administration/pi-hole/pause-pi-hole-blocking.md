---
id: computing-software.systems-network-administration.pi-hole.pause-pi-hole-blocking
name: pause-pi-hole-blocking
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [disable-blocking, blocking-timer, dns-blocking-endpoint]
level: intro
status: docs-checked
description: "Temporarily disable Pi-hole blocking from the CLI, the config key or the REST API with an automatic re-enable timer."
sources: ["https://docs.pi-hole.net/main/pihole-command/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pause blocking

**CLI**

```bash
pihole disable 5m
pihole enable
```

`pihole disable` optionally takes a duration after which blocking returns automatically. See `pihole disable --help` and `pihole enable --help`.

**Persistent switch.** The config key `dns.blocking.active` (default `true`) controls whether FTL blocks queries:

```bash
sudo pihole-FTL --config dns.blocking.active false
```

**REST API.** Authenticate first, then send the session ID (SID):

```bash
curl -k -X POST "https://pi.hole/api/dns/blocking" \
  -H "X-FTL-SID: <sid>" \
  --data '{"blocking": false, "timer": 300}'
```

The Home Assistant guide uses `"timer": "300"` for a 5-minute disable and notes it can be `null` for permanent. `GET /api/dns/blocking` returns the current state, for example `{"blocking": true}`.

Automation tools such as Home Assistant use this same sequence: log in with `POST /api/auth`, set blocking, then log out with `DELETE /api/auth`.

**Checklist**

1. Confirm with `pihole status`.
2. Log out API sessions you create, because the API allows only a limited number of concurrent sessions.

## Checked

2026-11-03. Read The pihole Command page (`disable 5m`, `enable`, `status`), the FTL configuration reference (`dns.blocking.active` default true), the API pages (`GET /api/dns/blocking` response, `X-FTL-SID` header, `DELETE /api/auth`, concurrent session limit) and the Home Assistant guide (POST `/dns/blocking` with `blocking` and `timer`, login and logout sequence). Removed the timer-choice advice. The 300 = 5 minutes figure is from the Home Assistant guide.

Method: documentation only; no commands were run.
