---
id: computing-software.systems-network-administration.healthchecks.auto-provisioning
name: auto-provisioning
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, auto-provisioning, create-parameter, dynamic-infrastructure]
level: advanced
status: docs-checked
description: "Let Healthchecks create a check on its first ping with a slug URL and ?create=1: defaults for new checks, status codes, account limit headroom and a hostname script."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/autoprovisioning.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/http_api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use a slug-based ping URL and add `?create=1`: `<ping-endpoint><ping-key>/<slug>?create=1`. Healthchecks finds the project by ping key and looks for a check with that slug.

- No such check: it is created, the ping is recorded, response is HTTP 201.
- Check exists: the ping is recorded, response is HTTP 200.
- Works on success, start, failure, log and exit-status slug endpoints.

Defaults for auto-created checks: period 1 day, grace time 1 hour, all integrations enabled. The URL cannot set anything else; adjust later in the web UI or the Management API.

Limits: 20 checks on free accounts, 100 or 1000 on paid. Auto-provisioning may temporarily exceed the account limit, up to twice the limit.

Typical use is dynamic infrastructure: give every client the project ping key and let it pick its own slug.

```
PING_KEY=your-ping-key
SLUG=$(hostname)
curl -m 10 --retry 5 "<ping-endpoint>$PING_KEY/$SLUG?create=1"
```

## Checked

2026-11-04: confirmed against the Auto Provisioning page (create=1, 201 vs 200, default period 1 day and grace 1 hour, all integrations, limits 20 / 100 or 1000, up to two times the limit) and the Pinging API page (create parameter default 0, 201 Created). The hostname script is an illustration built from the page's curl line.
Method: documentation only; no commands were run.
