---
id: computing-software.systems-network-administration.healthchecks.cloning-checks
name: cloning-checks
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, clone-check, create-a-copy, project-clone-script, migrate-checks]
level: practitioner
status: docs-checked
description: "Clone a Healthchecks check with Create a Copy, or copy every check into a new project with a Management API script using a read-only and a read-write key."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/cloning_checks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Single check: open Check Details and click "Create a Copy...". The copy lands in the same project and keeps name, tags, description, schedule, filtering rules and assigned integrations. It gets a new ping URL and an empty event log.

Whole project: the web UI has no project clone, so use the Management API. The docs script (Python with `requests`):

1. `API_URL` is the site's `/api/v3/checks/` endpoint.
2. `SOURCE_PROJECT_READONLY_KEY` is a read-only key for the source project; `TARGET_PROJECT_KEY` a key for the target.
3. GET the source checks with the source key in the `X-Api-Key` header.
4. For each item in `checks`, POST it as JSON to the same URL with the target key.

Notes on the script:
- It sends each check's JSON unchanged and has no error handling or status-code checks, so failed POSTs would go unreported. Test with one check first.
- The page does not say whether integrations carry over to the target project; check afterwards.

## Checked

2026-11-04: confirmed against the Cloning Checks page (Create a Copy contents, new ping URL and empty event log, no project clone in the UI, the requests script with X-Api-Key). Reworded the caveats so they are not attributed to the page and dropped a pagination remark.
Method: documentation only; no commands were run.
