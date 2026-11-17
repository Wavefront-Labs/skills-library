---
id: computing-software.systems-network-administration.healthchecks.ping-response-codes
name: ping-response-codes
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, response-codes, http-409, http-404, troubleshooting-pings]
level: practitioner
status: docs-checked
description: "Interpret Healthchecks Pinging API status codes: 200, 201 on auto-provisioning, 400 invalid URL, 404 unknown check or ping key, and 409 ambiguous slug."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/http_api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pinging API responses:

- 200 OK: the request succeeded; the body is `OK`.
- 201 Created: a slug endpoint with `create=1` auto-created a new check.
- 400 invalid url format: the URL does not match the expected format (slug and exit-status endpoints).
- 404 not found: no check matches the UUID, or for slug endpoints no check matches the ping key and slug. For exit-status slug endpoints the docs describe it as no project matching the ping key.
- 409 ambiguous slug: the slug matches more than one check; the ping is ignored.

Troubleshooting:
- 409: rename one of the duplicate checks, or ping by UUID, which always identifies one check.
- 404 after deleting and recreating a check: the UUID of a deleted check is gone permanently; update the client URL.
- A rate-limited ping may simply not be recorded (see ping-rate-limits).

## Checked

2026-11-04: confirmed against the Pinging API page (200, 201, 400, 404, 409 meanings, UUID of a deleted check cannot be recovered). Removed an unsourced curl `-f` remark.
Method: documentation only; no commands were run.
