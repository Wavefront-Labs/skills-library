---
id: computing-software.devops-ci-cd.release-engineering.audit-log-streaming-and-retention
name: audit-log-streaming-and-retention
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, audit-log-streaming, audit-log, github-audit-log, gitlab-audit-events, siem, log-retention]
level: practitioner
status: docs-checked
description: "Stream CI/CD platform audit logs to a SIEM or archive: GitHub Enterprise audit log streaming, GitLab audit event streaming, Jenkins audit trail, retention and useful detections."
sources:
  - https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/streaming-the-audit-log-for-your-enterprise
  - https://docs.gitlab.com/ee/user/compliance/audit_event_streaming.html
  - https://plugins.jenkins.io/audit-trail/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Audit log streaming and retention

The CI/CD platform holds the keys to production. Its audit log answers: who changed branch protection, added a deploy key, approved a deployment, read a secret, or changed a runner. Platform UIs keep logs for limited time (GitHub's organization audit log covers the last 180 days), so stream them.

## GitHub Enterprise Cloud
Supported streaming providers include Amazon S3, Azure Blob Storage, Azure Event Hubs, Datadog, Google Cloud Storage and Splunk.
- The stream contains both audit events and Git events.
- A paused stream retains its data (see the streaming page on data continuity); monitor stream health.
- The organization audit log needs a `created` date range to show events older than the default three months.

## GitLab
Audit event streaming sends events to an HTTP destination; a destination can carry up to 20 custom HTTP headers with each streamed event (see the GitLab audit event streaming page for destination types and filters).

## Jenkins
Audit Trail plugin (log file or syslog) plus Job Config History for config diffs; ship the files to your log store.

## Cloud and runners
Cloud provider audit logs record what CI identities did in the cloud; correlate them by identity or session name so deploys can be linked to pipeline runs.

## Detections worth alerting on
| Event | Why |
|---|---|
| branch protection/ruleset removed or bypass added (audit log category `protected_branch`) | disables review controls |
| deploy key or PAT created with write scope | persistent access |
| new self-hosted runner registered, runner group repo access changed | code execution in your network |
| secret created/updated in prod environment outside change window | possible tampering |
| environment protection rules changed | approval bypass |
| repo visibility changed to public | data exposure |
| org owner added, SSO/2FA requirement disabled | takeover |
| Actions policy changed to allow all actions | supply-chain risk |

## Retention
- Set retention from your own obligations (regulator, auditor, contract) and confirm the period with your compliance owner.
- Store in object storage with object lock/WORM and lifecycle to cold tiers; separate account from the platform admins.
- Normalise fields (actor, action, repo, ip, timestamp) for SIEM searches.

## Verify
- [ ] A test change to branch protection appears in the SIEM within minutes and fires the alert.
- [ ] Archive bucket has object lock and retention configured; stream health monitored.

## Checked

2026-10-28. Confirmed: GitHub organization audit log shows the last 180 days (default three months displayed, older needs a `created` range) and `protected_branch` is an audit log category; enterprise streaming providers (Amazon S3, Azure Blob Storage, Azure Event Hubs, Datadog, Google Cloud Storage, Splunk) and that streams carry audit and Git events; GitLab streaming accepts up to 20 custom HTTP headers; the Jenkins Audit Trail plugin and Job Config History plugin. Removed: Git events 7 days, menu paths, `gh api` audit query, exact action names (`protected_branch.destroy`, `repository_ruleset.update`), pause-and-email behaviour, the PCI DSS 10.5.1 / SOC 2 / 7 year retention figures, and the Jenkins no-built-in-log claim.

Method: documentation only; no commands were run.
