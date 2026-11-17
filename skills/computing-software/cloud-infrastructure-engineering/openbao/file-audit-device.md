---
id: computing-software.cloud-infrastructure-engineering.openbao.file-audit-device
name: file-audit-device
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, file-audit, file-path, mode, log-rotation]
level: practitioner
status: docs-checked
description: "Enable the OpenBao file audit device: file_path including stdout, mode 0600, SIGHUP log rotation and the v2.4.0 mode rules."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/audit/file.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File audit device

## Options

- `file_path` (required): where to write. Special values `stdout` and `discard`.
- `mode` default `"0600"`: octal like `chmod`. `"0000"` stops OpenBao changing the file mode.

## Commands

```
bao audit enable file file_path=/var/log/openbao_audit.log
bao audit enable -path="openbao_audit_1" file file_path=/path/to/openbao_audit.log
bao audit enable file file_path=stdout
```

The second shows multiple copies at different paths; the third suits containers.

## Log rotation

The device does not rotate logs; use existing tools. Send `SIGHUP` to the OpenBao process and file audit devices close and reopen their file.

## Warnings

- The device can write to arbitrary files on the instance. Be careful letting operators create it via the API when `unsafe_allow_api_audit_creation=true`; prefer declarative config.
- Since v2.4.0, executable bits in `mode` are stripped automatically (`777` becomes `666`) and irregular modes are rejected.

## Checked

2026-11-04. Confirmed against the File audit device page: file_path with stdout and discard, mode default 0600 and 0000, the three example commands, SIGHUP reopen, the arbitrary-file warning and the v2.4.0 executable-bit and irregular-mode rules. Nothing removed.

Method: documentation only; no commands were run.
