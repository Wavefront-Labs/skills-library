---
id: computing-software.digital-forensics-incident-response.evidence-handling.collecting-saas-evidence-via-vendor-apis
name: collecting-saas-evidence-via-vendor-apis
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [saas-evidence-collection, slack-audit-logs, github-audit-log, box-events, cloud-forensics, dfir]
level: practitioner
status: draft
description: "Collect SaaS evidence through vendor APIs: Slack Audit Logs API, GitHub audit log and git events, Box enterprise events; plan-tier limits, retention, pagination and hashing."
sources: ["https://api.slack.com/admins/audit-logs", "https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/using-the-audit-log-api-for-your-enterprise", "https://developer.box.com/guides/events/enterprise-events/for-enterprise/", "https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Collecting SaaS evidence via vendor APIs

SaaS logs live only with the vendor, often with short retention and plan-gated access. Export early through official APIs using a dedicated read-only admin token, and keep the raw JSON.

## Slack
- **Audit Logs API** (Enterprise Grid only): `GET https://api.slack.com/audit/v1/logs?oldest=<epoch>&action=user_login,file_downloaded` with an org-level user token holding `auditlogs:read`. Paginate with `cursor` (`response_metadata.next_cursor`). Actions of interest: `user_login`, `file_downloaded`, `file_public_link_created`, `app_installed`, `role_change_to_admin`, `user_session_reset_by_admin`.
- Non-Grid plans: `team.accessLogs` (logins by IP/user-agent) and workspace exports; message content needs Discovery API or export under Legal approval.

## GitHub
- Organisation audit log: `GET /orgs/{org}/audit-log?phrase=created:>=2026-10-01&include=all&per_page=100` (Enterprise Cloud for API access; `include=git` adds clone/push events retained for 7 days only). Follow `Link` headers for pagination.
- Look for `repo.download_zip`, `git.clone` bursts, `org.add_member`, `oauth_authorization.create`, `personal_access_token.request_created`, `repo.access` (visibility change), `secret_scanning_alert` changes, and actor IPs (IP disclosure must be enabled).
- Enterprise accounts can stream audit logs to S3/Azure/Splunk; enable it during the incident if not already.

## Box
- Enterprise events: `GET https://api.box.com/2.0/events?stream_type=admin_logs&created_after=...` with an admin-scoped app. Event types: `DOWNLOAD`, `PREVIEW`, `SHARE`, `COLLABORATION_INVITE`, `LOGIN`, `ADMIN_LOGIN`. Use `admin_logs_streaming` for recent near-real-time data; page with `stream_position`.

## Collection practice
1. Note plan tier and documented retention per source before starting; record gaps.
2. Script exports to write raw responses page by page (`page_0001.json`...), plus a manifest with request URL, time, token identity and SHA-256 per file.
3. Respect rate limits (HTTP 429 with `Retry-After`); retries must not drop pages.
4. Normalise to a timeline afterwards; never edit the raw files.

## Gotchas
- Some events only identify actors by internal IDs; also export user lists to resolve them.
- Creating the collection token is itself an audited admin action; document it so it is not mistaken for attacker activity.

## Verify
Event counts per day show no unexplained holes, the manifest hashes match the stored files, and the export window covers the full incident period or the gap is documented.
