---
id: computing-software.cloud-infrastructure-engineering.google-cloud.windows-server-vms-passwords-and-sysprep
name: windows-server-vms-passwords-and-sysprep
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, windows-vm, windows-password-reset, sysprep, gcesysprep, rdp, windows-activation]
level: practitioner
status: docs-checked
description: "Run Windows Server on Compute Engine: public images, credentials via reset-windows-password, RDP through IAP, KMS activation on private subnets, and GCESysprep for golden images."
sources: ["https://docs.cloud.google.com/compute/docs/instances/windows/creating-managing-windows-instances", "https://docs.cloud.google.com/compute/docs/instances/windows/generating-credentials", "https://docs.cloud.google.com/compute/docs/instances/windows/creating-windows-os-image", "https://docs.cloud.google.com/iap/docs/using-tcp-forwarding", "https://docs.cloud.google.com/compute/docs/instances/startup-scripts/windows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Server VMs, passwords and sysprep

## 1. Create
```bash
gcloud compute images list --project=windows-cloud --no-standard-images
gcloud compute instances create win-1 --zone=<Z> --machine-type=<MACHINE_TYPE> \
  --image-family=<WINDOWS_IMAGE_FAMILY> --image-project=windows-cloud \
  --no-address \
  --metadata-from-file=windows-startup-script-ps1=./setup.ps1
```
Take the image family from the `images list` output. Bring-your-own-licence images need compliant hardware such as sole-tenant nodes (see the sole-tenant skills); images that rely on Google's licensing activate against Google's KMS (section 4).

## 2. Credentials
```bash
gcloud compute reset-windows-password win-1 --zone=<Z> --user=ops-admin   # prints ip_address, username and the new password
```
- Prompts for confirmation: resetting an existing account's password can lose data encrypted with the current password (encrypted files, stored passwords).
- Roles needed: Compute Instance Admin (v1) on the VM or project, plus Service Account User if the VM uses a service account. The instance must be online and ready.
- Do not generate credentials on an Active Directory domain controller without care: it can reset a domain user's password or create a domain user; disable the account manager to prevent it.
- Built-in accounts such as Administrator are disabled by default; a reset does not enable them. Credential management expects English names for key accounts and groups (Administrator, Administrators).
- Store the output in a vault, never in tickets.

## 3. Connect without a public IP
```bash
gcloud compute start-iap-tunnel win-1 3389 --local-host-port=localhost:13389 --zone=<Z>
# then RDP to localhost:13389
```
Firewall: allow ingress TCP 3389 from `35.235.240.0/20`, the range IAP uses for TCP forwarding. IAP disconnects sessions after one hour of inactivity.

## 4. Activation on private subnets
Windows activates against `kms.windows.googlecloud.com` (35.190.247.13). The VM needs a route to it whose next hop is the default internet gateway, and egress firewall rules must allow it. Cloud NAT and instance-based NAT gateways cannot activate Windows, because the KMS server rejects requests from addresses not confirmed to be Compute Engine instances. VMs without external IPs, or behind Cloud NAT, also need **Private Google Access** enabled on the subnet.

## 5. Golden image
```powershell
# on the configured VM, with administrative rights: generalises and shuts the VM down
GCESysprep
```
```bash
gcloud compute images create win2022-app-v3 --source-disk=win-1 --source-disk-zone=<Z> \
  --family=win2022-app --storage-location=europe-west2
```
GCESysprep disables the GCEStartup task, clears temp files and event logs, runs `sysprep.exe /generalize /oobe /quit /unattend`, configures `instance_setup.ps1` to run at first boot, deletes the RDP certificate, enables RDP and WinRM firewall rules, disables the Google OS Config service and shuts the instance down. Run it before creating the image; `--force` creates an image from a disk attached to a running instance.

## Gotchas
- Windows instances start slowly because of sysprep; the console may show running before setup is done. Check `gcloud compute instances get-serial-port-output win-1` for `Instance setup finished`.
- To make credential resets fail less often, keep key account and group names in English.
- `windows-startup-script-ps1` runs on every boot after the initial boot, so make it idempotent. A script stored in a less secure Cloud Storage bucket than metadata can enable privilege escalation, because it runs as LocalSystem with the VM service account's permissions.

## Verify
- [ ] Serial port output contains `Instance setup finished`.
- [ ] RDP via IAP works; the firewall exposes 3389 only to the IAP range.

## Checked
2026-10-28. Confirmed against "Create and manage Windows Server VMs" (serial-port check, KMS host and IP, route, Cloud NAT limit, Private Google Access), "Manage accounts and credentials on Windows VMs" (roles, confirmation prompt, domain controller warning, built-in accounts), the Windows image page (GCESysprep steps, `images create` flags), the IAP TCP forwarding page (IAP range, 3389, tunnel flags, one-hour idle disconnect) and the Windows startup scripts page (every-boot behaviour, LocalSystem risk). Removed: the pay-as-you-go statement, SQL image project, the metadata-mechanism explanation, `slmgr` check and "Activation successful" string, first-boot timing, Windows Update/WSUS advice, SID duplication claim, disk size and Secure Boot flags.
Method: documentation only; no commands were run.
