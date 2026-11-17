---
id: computing-software.cybersecurity-defensive.security-operations.soar-playbook-testing-and-versioning
name: soar-playbook-testing-and-versioning
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soar, playbook-testing, playbook-versioning, staging-environment, test-containers, mock-integrations, change-management]
level: advanced
status: draft
description: "Test and version SOAR playbooks like code: dev/staging/prod, test containers and replayed alerts, mocking destructive actions, source control export and safe rollout."
sources: ["https://docs.splunk.com/Documentation/SOAR/current/Playbook/Overview", "https://xsoar.pan.dev/docs/integrations/test-playbooks", "https://learn.microsoft.com/en-us/azure/logic-apps/devops-deployment-single-tenant-azure-logic-apps"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing and versioning SOAR playbooks

A broken playbook either does nothing (silent failure during an incident) or does the wrong thing
fast (isolating the CEO's laptop, disabling service accounts). Treat playbooks as production code.

## Environments
- **Dev**: author freely, integrations point at sandboxes or mocks.
- **Staging**: same versions as prod, connected to non-production tenants (test EDR group, test
  mailbox, test AD OU).
- **Prod**: only promoted versions.
Splunk SOAR and XSOAR support exporting/importing playbooks and syncing with Git
(SOAR source control repositories; XSOAR content packs with `demisto-sdk`); Logic Apps via ARM/Bicep.

## Test data
- Save real alerts (sanitised) as fixtures: SOAR "containers" exported as JSON, XSOAR incidents,
  Sentinel incident payloads.
- Cover branches: malicious verdict, benign, missing fields, integration timeout, empty results,
  huge result sets.
- XSOAR has formal **test playbooks** that run with `demisto-sdk test-content`; Splunk SOAR playbooks
  can be run against test containers via the debugger and REST API.

## Mocking destructive actions
- A global "dry run" flag (custom list/asset setting) checked before any contain/disable/delete
  action; in dry run, log the intended action instead.
- In staging, scope actions to test entities only (allow list of test hostnames/users) as a second
  safety net.

## Version control and review
- Every change via pull request with diff of the exported playbook and code blocks.
- Peer review focuses on: input validation, guardrails (caps on number of entities), error handling
  (what happens when an API fails), and idempotency (re-running does not double-act).
- Tag releases; keep the previous version importable for rollback.

## Rollout
Deploy to prod disabled or in "notify only" mode, watch several real runs, then enable automatic actions.

## Monitoring in prod
- Alert on playbook failures and unusually long runs.
- Track per-playbook action counts; a sudden spike in "disable account" is a bug or an attack.

## Gotchas
- API credential changes break playbooks silently; test integrations health daily.
- Vendor API changes (deprecated endpoints) break things on upgrades; re-run the test suite after
  app/integration updates.
- Copy-paste between environments carries hardcoded IDs; parameterise.

## Verify
The test suite passes in staging for every PR, and a quarterly game-day runs key playbooks end to
end against staging with expected outcomes recorded.
