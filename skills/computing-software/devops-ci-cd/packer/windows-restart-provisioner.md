---
id: computing-software.devops-ci-cd.packer.windows-restart-provisioner
name: windows-restart-provisioner
category: computing-software
field: devops-ci-cd
product: packer
tags: [windows-restart, reboot, provisioner, registry, prov-winrestart]
level: practitioner
status: docs-checked
description: "Reboot a Windows guest mid-build with windows-restart and wait until it is back."
sources:
  - "https://developer.hashicorp.com/packer/docs/provisioners/windows-restart/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `windows-restart` provisioner restarts the guest and waits for it to come back, so later provisioners can continue over WinRM.

```hcl
provisioner "windows-restart" {
  restart_timeout = "10m"
}
```

Settings and defaults:

- `restart_command` defaults to `shutdown /r /f /t 0 /c "packer restart"`.
- `restart_check_command` is run after `restart_command` to check the guest has restarted; it retries until the connection is back or `restart_timeout` is exceeded.
- `restart_timeout` is how long to wait for the restart; the default is 5 minutes.
- `check_registry` (beta) waits until the keys in `registry_keys` are no longer present before reconnecting; the docs recommend finishing auto-rebooting installs such as Windows Updates during the autounattend phase instead.

Packer detects that the reboot has finished through an RPC call over WinRM, not ACPI, so Windows must be fully booted. The docs suggest raising `restart_timeout` when installing updates or when there are many startup services.

## Checked
2026-11-03. Confirmed against the windows-restart provisioner page: purpose, WinRM-based detection, `restart_command` default, `restart_check_command`, `restart_timeout` default 5 minutes, beta `check_registry` and `registry_keys`. Removed unsourced sequencing advice.
Method: documentation only; no commands were run.
