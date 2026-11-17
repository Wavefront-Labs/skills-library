---
id: computing-software.cloud-infrastructure-engineering.openbao.audit-devices
name: audit-devices
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, audit, hmac, log-raw, blocking]
level: practitioner
status: docs-checked
description: "OpenBao audit devices: what is logged and HMAC-hashed, blocking behaviour, multiple devices, common options and v2.3.2 creation flags."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/audit/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audit devices

Every request and response (including errors) is logged as JSON lines of `type` `request` or `response`, linked by a request ID. Nothing is enabled on a new server. Unaudited paths include `sys/init`, `sys/seal-status`, `sys/health`, `sys/leader`.

## HMAC

Most strings are hashed with HMAC-SHA256 and a salt. Verify a value with `/sys/audit-hash`. Only strings are hashed; integers, booleans and timestamps are logged in plaintext. Re-enabling a device at the same path creates a new salt.

## Blocking

A request succeeds if at least one device records it. But if a device blocks on write (more likely with network devices), OpenBao completes no requests until it can write. Run multiple devices; logs go to all, and you combine them for a complete record.

## Common options

`elide_list_responses` false, `format` `json` (only value), `hmac_accessor` true, `log_raw` false (unhashed secrets), `prefix` "", `skip_test` (skips the enable-time probe).

## Enabling

`bao audit enable file file_path=<path>`, or the `audit` config stanza.

## Gotchas

- Since v2.3.2, API/CLI creation needs `unsafe_allow_api_audit_creation = true`; `prefix` needs `allow_audit_log_prefixing = true`.
- Audit config replicates cluster-wide; confirm every node can write before enabling.

## Checked

2026-11-04. Confirmed against the Audit devices overview page: unaudited paths, HMAC-SHA256 with salt and /sys/audit-hash, string-only hashing, new salt on re-enable, blocking behaviour, common options and defaults, and the v2.3.2 unsafe_allow_api_audit_creation and allow_audit_log_prefixing requirements. Nothing removed.

Method: documentation only; no commands were run.
