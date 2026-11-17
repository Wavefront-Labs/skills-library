---
id: computing-software.cloud-infrastructure-engineering.azure.vm-extensions-custom-script-and-run-command
name: vm-extensions-custom-script-and-run-command
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-extensions, custom-script-extension, run-command, managed-run-command, vm-applications, vm-agent, waagent, windows-guest-agent, extension-ordering, protected-settings, dsc-extension, machine-configuration, key-vault-extension, azure-monitor-agent-extension, extension-troubleshooting, provisioning-failed, handler-logs]
level: practitioner
status: docs-checked
description: "Post-boot VM config with extensions: Custom Script with protectedSettings and managed-identity downloads, managed Run Command, VM Applications, and handler logs."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-machines/extensions/custom-script-linux", "https://learn.microsoft.com/en-us/azure/virtual-machines/extensions/custom-script-windows", "https://learn.microsoft.com/en-us/azure/virtual-machines/windows/run-command-managed", "https://learn.microsoft.com/en-us/azure/virtual-machines/vm-applications", "https://learn.microsoft.com/en-us/cli/azure/vm/run-command", "https://learn.microsoft.com/en-us/cli/azure/vm/application"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM extensions, Custom Script and Run Command — post-boot config that leaves a trail

**Goal:** bootstrap and break-glass scripts that run exactly once (or exactly when you
say), fetch artefacts without secrets, and whose failure you can diagnose from the handler log.

## 1. Which mechanism
| Need | Use |
|---|---|
| Run a script from a storage/Git URL, once, at deploy | **Custom Script Extension** (CSE) |
| Ad hoc or repeatable scripts from the control plane, output back to ARM, no inbound ports | **Managed Run Command** (`az vm run-command create`) |
| Install versioned packages across a fleet | **VM Applications** (Compute Gallery) |
| Agents (Monitor, Defender, Key Vault cert sync, DSC/Machine Configuration) | Their dedicated extensions |

## 2. Custom Script Extension
```bash
az vm extension set -g rg --vm-name vm-app-01 --publisher Microsoft.Azure.Extensions \
  --name CustomScript --version 2.1 \
  --protected-settings '{"fileUris":["https://stdeploy.blob.core.windows.net/scripts/bootstrap.sh"],"commandToExecute":"bash bootstrap.sh prod","managedIdentity":{}}'
# Windows: name CustomScriptExtension, typeHandlerVersion 1.10 (see the Windows page for settings)
```
- Microsoft strongly recommends protected settings over public settings; `managedIdentity` must
  be in protected settings only.
- `"managedIdentity": {}` (system-assigned) or `{"clientId": "..."}` / `{"objectId": "..."}`
  (user-assigned) downloads `fileUris` blobs with the VM's identity, version 2.1 and later on Linux,
  so no SAS or storage key. It cannot be combined with `storageAccountName`/`storageAccountKey`.
- Only one version of the extension applies to a VM; to run another script, update the existing
  extension. Changing `timestamp` (any different integer) triggers a rerun.
  Scripts must be **idempotent**.
- The script gets 90 minutes; longer fails the extension. For long installs, start a service and exit.
- Linux logs: `/var/log/azure/custom-script/handler.log` and the download folder under
  `/var/lib/waagent/custom-script/download/<n>/`.

## 3. Managed Run Command
```bash
az vm run-command create -g rg --vm-name vm-app-01 --run-command-name fix-dns \
  --script "sudo sed -i 's/^#DNS=.*/DNS=10.0.0.4/' /etc/systemd/resolved.conf && sudo systemctl restart systemd-resolved" \
  --timeout-in-seconds 600 --run-as-user root \
  --output-blob-uri "https://stlogs.blob.core.windows.net/rc/fix-dns.txt?<sas or MI>"
az vm run-command show -g rg --vm-name vm-app-01 --run-command-name fix-dns --instance-view
```
- Multiple run commands per VM, each an ARM resource with history; `--async-execution`
  for fire-and-forget; `--script-uri` for stored scripts; parameters/protected parameters.
- Multiple RunCommand resources deployed together execute simultaneously; use `dependsOn` to order them. The default timeout is 90 minutes.
- `treatFailureAsDeploymentFailure` (API 2023-03-01 and later) makes a script failure fail the deployment.
- Running a command needs `Microsoft.Compute/virtualMachines/runCommand/write` (Virtual Machine Contributor and above); it executes on the VM, so restrict it.

## 4. VM Applications
Package → `az sig gallery-application create` + `version create` (blob with the installer,
`--install-command`, `--remove-command`, `--update-command`) → `az vm application set --app-version-ids <id> --treat-deployment-as-failure true`.
Versions follow Major.Minor.Patch; only one version of a given application can be on a VM.
Setting `treatFailureAsDeploymentFailure` makes an install failure fail the VM deployment.

## 5. Troubleshooting
- Check the VM instance view for the agent status and each extension's provisioning state and message.
- Read the handler log first; the Custom Script pages list the log locations.

## Gotchas
- CSE scripts remain on disk with any secrets they wrote.

## Verify
- [ ] `az vm extension list` shows the extension `Succeeded`; the handler log ends with exit 0.
- [ ] Re-running the CSE (new timestamp) produces no change on an already-configured VM.
- [ ] Run Command output blob contains the expected stdout; the Activity log records who ran it.
- [ ] VM Application install succeeded on every targeted VM.

## Checked
2026-10-28. Confirmed on Microsoft Learn (Custom Script for Linux and Windows, managed Run Command, VM Applications, `az vm application` pages): 90-minute script limit, one extension version per VM, `timestamp` rerun, `managedIdentity` forms and protected-only rule, handler 2.1 and 1.10 versions, Linux log paths, concurrent RunCommand resources with `dependsOn`, `treatFailureAsDeploymentFailure`, application version format and one-version-per-VM rule. check_commands found no bad flags. Removed: legacy run-command limits, Arc and RBAC action name, WireServer and agent service troubleshooting, Windows log paths, cloud-init and stuck-extension advice.
Method: documentation only; no commands were run.
