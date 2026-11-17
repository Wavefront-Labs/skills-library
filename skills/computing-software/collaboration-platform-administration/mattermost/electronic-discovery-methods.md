---
id: computing-software.collaboration-platform-administration.mattermost.electronic-discovery-methods
name: electronic-discovery-methods
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [ediscovery, compliance-api, legal, sql]
level: advanced
status: docs-checked
description: "Extract Mattermost post data for eDiscovery using compliance exports, the compliance reports REST API with curl, or direct SQL on the Posts table."
sources: ["https://docs.mattermost.com/administration-guide/comply/electronic-discovery.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# eDiscovery extraction

eDiscovery means searching electronic data as legal evidence; a legal hold extends it by forbidding deletion of possibly relevant information. Mattermost offers three ways to extract post data.

1. Compliance exports (Enterprise): export message content and who could have seen it in Actiance XML, Global Relay EML or generic CSV, on a schedule to a shared location.

2. REST API: authenticate as an account with manage_system permission. Log in with curl -i -d '{"login_id": "username", "password": "password"}' https://yourmattermosturl/api/v4/users/login, then take the token from the response headers and send it as an Authorization: Bearer header on later calls. Create a report with a POST to /api/v4/compliance/reports using JSON that includes user_id, start_at, end_at (Unix epoch milliseconds), keywords and emails. The response shows status running with an id. When it finishes, GET /api/v4/compliance/reports/<id>/download with --output report-zip.zip to save the archive. Run time depends on record count and load.

3. SQL: select a user's messages with SELECT * FROM mattermost.Posts WHERE UserId = (SELECT Id FROM mattermost.Users WHERE Username = 'username'); and limit by time by adding AND CreateAt > <start> AND CreateAt < <end> to the outer WHERE clause (the docs' own date example places the CreateAt conditions inside the subquery, which filters the user lookup rather than the posts). Dates are stored as Unix epoch values, so convert before filtering.

Choose the compliance export or API for auditable, formatted output; use SQL only when direct database access is acceptable. Handle the exported data as sensitive evidence.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/comply/electronic-discovery (three methods, compliance API calls). Corrected the SQL date filter: the docs' example puts CreateAt inside the user subquery, so the skill places it on the outer WHERE.

Method: documentation only; no commands were run.
