---
id: computing-software.systems-network-administration.healthchecks.uuid-vs-slug-urls
name: uuid-vs-slug-urls
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, slug-url, uuid-url, ping-key, ambiguous-slug]
level: practitioner
status: docs-checked
description: "Choose between Healthchecks UUID ping URLs and slug URLs using a project ping key: character rules, duplicate-slug 409 behaviour and the display selector."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/slug_urls.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/http_api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two ping URL formats exist.

UUID URL: the check's UUID is appended to the ping endpoint. The UUID is assigned automatically, is immutable and cannot be replaced; deleting a check loses it permanently. It is a per-check secret and hard to remember.

Slug URL: `<ping-endpoint><ping-key>/<slug>`. All checks in a project share one ping key, shown on the project's Settings page. A slug uses only `a-z`, `0-9`, hyphens and underscores, and can be changed later. Slug URLs support the same start, failure, exit-code and log suffixes, and enable auto-provisioning with `?create=1`.

Because the ping key is the secret, slugs can be hardcoded or shared without exposing checks to arbitrary pings.

Slugs are not guaranteed unique. Pinging a slug that matches several checks returns HTTP 409 (ambiguous slug) and the request is ignored. UUID URLs for those checks still work, and the web UI warns about duplicates.

The "UUID / Slug" selector in the checks list and check details only changes which format is displayed. Both formats work for pinging either way.

## Checked

2026-11-04: confirmed against the Slug URLs page (ping key as the secret, allowed slug characters, mutable slug, 409 ambiguous slug, UUID/Slug selector display-only) and the Pinging API page (UUID immutable and not recoverable).
Method: documentation only; no commands were run.
