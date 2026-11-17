---
id: computing-software.cloud-infrastructure-engineering.openbao.recovery-mode
name: recovery-mode
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, recovery-mode, recovery-token, generate-root, sys-raw]
level: sme
status: docs-checked
description: "Start OpenBao with -recovery, mint a recovery token with generate-root and OTP, and use sys/raw to repair storage safely."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/recovery-mode.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovery mode

Warning from the docs: be very careful modifying or deleting keys in recovery mode, and always have a snapshot ready. Have recovery/unseal keys ready too.

## Steps

```
bao server -config /path/to/config.hcl -recovery
```

Startup logs should show `Recovery Mode: true`. Then:

```
bao operator generate-root -generate-otp -recovery-token
bao operator generate-root -init -otp=<otp> -recovery-token
bao operator generate-root -nonce <nonce> -recovery-token <recovery/unseal-key>
bao operator generate-root -decode=<encoded-token> -otp=<otp> -recovery-token
```

`-init` prints a nonce. Submit shares until the threshold is met; an encoded token is returned, which you decode. Use it:

```
export BAO_TOKEN=<recovery-token>
bao list sys/raw
```

## Notes

- Only one recovery token per session; to replace a lost one, restart and generate again.
- Recovery tokens are not persisted; a restart needs a new one.
- With Integrated Storage, pick the node with the highest `AppliedIndex` (from `bao status` on sealed nodes).
- After recovery the Raft cluster must be re-formed before returning to service.

## Checked

2026-11-04. Confirmed against the Recovery mode page: the -recovery flag and the Recovery Mode: true log line, the four generate-root commands with nonce and OTP, one recovery token per session, no persistence across restarts, sys/raw, the AppliedIndex rule for Integrated Storage, and re-forming the Raft cluster. Nothing removed.

Method: documentation only; no commands were run.
