---
id: computing-software.systems-network-administration.netbird.remote-jobs
name: remote-jobs
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, remote-jobs, remote-debug-bundle, allow-remote-jobs, rbac]
level: advanced
status: docs-checked
description: "Run diagnostic Remote Jobs such as a debug bundle on a NetBird peer from the dashboard or API: opt-in flag, permissions, parameters, results and endpoints."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/remote-jobs.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Remote Jobs let admins run diagnostics on connected peers without CLI access.

Requirements: peer online, NetBird v0.64.0+, and opted in with `--allow-remote-jobs` or the `allowRemoteJobs` MDM policy (off by default; otherwise the Run Remote Job button is disabled).

Flow: admin creates a job; Management sends it over the peer's gRPC connection; the peer runs it and reports. One pending job per peer. Statuses: Pending, Succeeded, Failed. No response after 5 minutes marks it failed.

Permissions: the RemoteJobs RBAC module; Create to start jobs, Read to view history and results.

Debug Bundle parameters:
- Log File Count: 1 to 1000 (default 10).
- Bundle Duration: 1 to 5 minutes (disabled by default).
- Anonymize: off by default.
- Anonymization Level: `default` keeps private IP ranges readable; `strict` also anonymizes private, CGNAT and link-local addresses.
- Upload URL: HTTPS only; an MDM policy can override it.

On success an upload key is returned and expires after 30 days. Share with support; only post publicly if Anonymize was on.

Dashboard: Peers > select peer > Run Remote Job > Debug Bundle. API:
- `POST /api/peers/{peerId}/jobs`
- `GET /api/peers/{peerId}/jobs`
- `GET /api/peers/{peerId}/jobs/{jobId}`

## Checked

2026-11-04. Confirmed against the NetBird Remote Jobs page: v0.64.0 and opt-in flag, lifecycle and statuses, 5-minute timeout, RemoteJobs permissions, debug bundle parameters with ranges and defaults, upload key and 30-day expiry, dashboard path, API endpoints. Nothing removed.
Method: documentation only; no commands were run.
