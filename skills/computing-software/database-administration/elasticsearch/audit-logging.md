---
id: computing-software.database-administration.elasticsearch.audit-logging
name: audit-logging
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, elasticsearch-security, elasticsearch-audit-logging, audit-events, xpack-security-audit, include-request-body, ignore-filters, compliance]
level: practitioner
status: docs-checked
description: "Turn on Elasticsearch security audit logging, choose events, filter noise with ignore_filters, and ship the JSON audit log to a separate cluster or SIEM."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/monitor/stack-audit-logging/enabling-audit-logs.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/monitor/stack-audit-logging/logfile-audit-events-ignore-policies.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/auding-settings.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/elasticsearch-audit-events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audit logging

**Goal:** a record of authentication failures, access denials and security config changes, without logging every search body.

## Enable (cluster settings, per node log file)
```json
PUT _cluster/settings
{ "persistent": {
  "xpack.security.audit.enabled": true,
  "xpack.security.audit.logfile.events.include": ["authentication_failed", "access_denied", "tampered_request", "connection_denied", "run_as_denied", "security_config_change", "anonymous_access_denied"],
  "xpack.security.audit.logfile.events.emit_request_body": false
} }
```
Before Stack 9.5, `xpack.security.audit.enabled` is static: set it in `elasticsearch.yml` on every node and do a rolling restart (the `PUT` above then only works for the dynamic `events.*` and `ignore_filters` settings). From 9.5 it is dynamic. Output: `<cluster>_audit.json` in the logs dir (layout in `log4j2.properties`).

## Event types
`authentication_success`, `authentication_failed`, `access_granted`, `access_denied`, `security_config_change` (users/roles/API keys changed), `connection_granted/denied` (IP filter), `run_as_granted/denied`, `tampered_request`, `system_access_granted`. Including `access_granted` logs every action: very high volume.

## Ignore filters (drop noise)
```json
PUT _cluster/settings
{ "persistent": {
  "xpack.security.audit.logfile.events.ignore_filters.monitoring.users": ["kibana_system", "remote_monitoring_user"],
  "xpack.security.audit.logfile.events.ignore_filters.health.actions": ["cluster:monitor/health", "cluster:monitor/nodes/stats"]
} }
```
A policy (`ignore_filters.<policy_name>`) can match `users`, `realms`, `actions`, `roles`, `indices` (wildcards or Lucene regex). An event is ignored if it matches all the rules of any one policy.

## Shipping
Filebeat/Elastic Agent with the Elasticsearch module reads `*_audit.json` and sends it to a **separate** monitoring cluster (an attacker with access to the production cluster should not be able to edit audit data).

## Gotchas
- Audit logs are only available on certain subscription levels; check the Elastic subscriptions page for your tier.
- `emit_request_body: true` can log credentials and PII in request bodies.
- Every node writes its own file; collect from all nodes, including coordinating nodes.

## Verify
A login with a wrong password produces an `authentication_failed` event with the user and origin address; creating a role produces `security_config_change`.

## Checked

Checked 2026-10-25 against the elastic/docs-content and elastic/elasticsearch `main` documentation (Stack 9.5/9.6 docs). Confirmed: `xpack.security.audit.enabled` default false and dynamic only from 9.5 (static before); `events.include`, `emit_request_body` and `ignore_filters.<policy>.users|realms|actions|roles|indices` are dynamic settings; event type names; ignore policy semantics (all rules of a policy must match, any matching policy ignores the event); output file `<clustername>_audit.json` on every node. The exact licence tier was not stated in the page read, so the skill now defers to the subscriptions page.

Method: documentation only; no commands were run.
