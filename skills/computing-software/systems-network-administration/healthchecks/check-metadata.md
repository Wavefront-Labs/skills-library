---
id: computing-software.systems-network-administration.healthchecks.check-metadata
name: check-metadata
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, check-name, check-tags, check-description, slug-rules]
level: intro
status: docs-checked
description: "Set a Healthchecks check's name, slug, tags and description: allowed slug characters, space-separated tags and what to record in the description."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/configuring_checks.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Checks are created in the web UI or via the Management API. Pricing plans are based mainly on the number of checks.

- Name: optional but recommended as the count grows. Appears in the UI, email reports and notifications. API max 100 characters.
- Slug: identifier for slug-based ping URLs. Only lowercase letters, digits, hyphens and underscores. May be empty if you use UUID URLs. API max 100 characters.
- Tags: space-separated labels for grouping (environment, role or any scheme). Tags also drive badges and Prometheus `hc_tag_up`, and the API list call can filter by `tag`.
- Description: free-form notes for your team or future you: purpose, owner, failure-response steps, reference links. API max 10,000 characters.

Practice: put the runbook link and owner in the description so whoever receives the alert knows what to do.

API example for a custom slug:

```
{"slug": "my-custom-slug"}
```

Slug duplicates are allowed, but pinging an ambiguous slug returns 409.

## Checked

2026-11-04: confirmed against the Configuring Checks page (name, slug, tags, description) and the Management API page (100 character limits for name and slug, 10000 for description, tag filter), the Status Badges page and the Prometheus page (hc_tag_up).
Method: documentation only; no commands were run.
