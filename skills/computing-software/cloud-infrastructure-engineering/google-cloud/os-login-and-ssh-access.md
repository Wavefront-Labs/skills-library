---
id: computing-software.cloud-infrastructure-engineering.google-cloud.os-login-and-ssh-access
name: os-login-and-ssh-access
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, os-login, ssh-access, iap-tunnel, iap-tcp-forwarding, metadata-ssh-keys, enable-oslogin, oslogin-2fa, compute-oslogin, osadminlogin, posix-accounts, bastion, no-external-ip, sudo-access, ssh-audit, serial-console, windows-rdp, gcloud-compute-ssh]
level: practitioner
status: docs-checked
description: "SSH to Compute Engine without metadata keys: enable OS Login via metadata, map sudo to roles/compute.osAdminLogin, tunnel through IAP with no external IP, use serial console."
sources: ["https://docs.cloud.google.com/compute/docs/oslogin", "https://docs.cloud.google.com/compute/docs/oslogin/set-up-oslogin", "https://docs.cloud.google.com/compute/docs/instances/managing-instance-access", "https://docs.cloud.google.com/compute/docs/troubleshooting/troubleshooting-ssh"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OS Login and SSH access

**Goal:** SSH identity is the engineer's Google identity, revoked when IAM is revoked, with
sudo as a role, no public keys scattered in instance metadata, and no VM with a public IP.

## 1. Turn on OS Login everywhere
- Per project: `gcloud compute project-info add-metadata --metadata=enable-oslogin=TRUE`;
  per VM `--metadata=enable-oslogin=TRUE`. `enable-oslogin=FALSE` in instance metadata disables OS Login for that VM even when project metadata says TRUE; with OS Login disabled, metadata SSH keys work.
- Optional `enable-oslogin-2fa=TRUE` for a second factor at SSH time; it only takes effect when `enable-oslogin` is also `TRUE`, and users need 2-Step Verification set up.

## 2. IAM mapping
| Role | Result |
|---|---|
| `roles/compute.osLogin` | login as a POSIX user, no sudo |
| `roles/compute.osAdminLogin` | login with sudo |
| `roles/compute.osLoginExternalUser` | needed in addition for users from **another org** |
| `roles/iam.serviceAccountUser` | needed on the service account when the VM runs as one |

Grant `osLogin` or `osAdminLogin` on the project or instance; for SSH from the console or gcloud, grant at project level (or add a project-level role containing `compute.projects.get`).
The POSIX username is derived from the email (`USERNAME_DOMAIN_SUFFIX`; users from another organization get an `ext_` prefix, service accounts `sa_`; names over 32 characters are truncated); see it with
`gcloud compute os-login describe-profile`.

## 3. Connect with no external IP
```bash
gcloud compute ssh app-1 --zone=europe-west1-b --tunnel-through-iap
# plain ssh/scp/ansible through the same tunnel
gcloud compute ssh app-1 --tunnel-through-iap --dry-run   # prints the ProxyCommand to copy into ~/.ssh/config
```
Firewall: allow tcp:22 from `35.235.240.0/20`, the range IAP uses for TCP forwarding. Remove `0.0.0.0/0` on 22 entirely. Grant IAP tunnel access per the IAP documentation.
For a non-gcloud client register a key once: `gcloud compute os-login ssh-keys add --key-file=~/.ssh/id_ed25519.pub --ttl=8h`.

Service accounts can SSH too (CI runners, Ansible): grant `roles/compute.osAdminLogin` to the SA and run with that SA's credentials — its username is prefixed `sa_`.

## 4. Break-glass
- When SSH is broken (bad sshd config, full disk): **serial console** (the SSH troubleshooting page uses it for sshd, guest agent and full-disk problems; connecting for sshd work is as the root user) —
  `gcloud compute instances add-metadata VM --metadata=serial-port-enable=TRUE` then
  `gcloud compute connect-to-serial-port VM`; a Workspace policy or organization restrictions can block serial console access, so plan a documented exception.
- Alternative: attach the boot disk to a rescue VM and edit files.

## Gotchas
- Mixed state: a project with `enable-oslogin=TRUE` and a VM with `enable-oslogin=FALSE` uses metadata keys — audit per VM.
- Users in a *different* organization (contractors) need `osLoginExternalUser` granted on *your* organization by an organization administrator.

## Verify
- [ ] `gcloud compute instances describe VM --format='value(metadata.items)'` shows no `ssh-keys` and `enable-oslogin=TRUE`.
- [ ] A user with `osLogin` only cannot sudo; with `osAdminLogin` sudo works.
- [ ] Removing the user from the group ends access on the next login attempt.
- [ ] No firewall rule allows 22 from anything but `35.235.240.0/20` or the corporate range.

## Checked
2026-10-31. Confirmed on the OS Login overview, Set up OS Login, Managing instance access and SSH troubleshooting pages: `enable-oslogin` TRUE/FALSE and instance override, `enable-oslogin-2fa` needs both set TRUE plus 2-Step Verification, osLogin (no sudo) vs osAdminLogin (sudo), osLoginExternalUser granted on the Organization by an organization admin, serviceAccountUser on the service account, `ext_` / `sa_` prefixes and 32-character truncation, IAP range 35.235.240.0/20, serial console use. Removed: org policy names, `tunnelResourceAccessor`, the Windows section, audit method names, gcloud key-file behaviour and sudo error text (not on the fetched pages; the ssh-using-iap page was unreadable). Commands checked with check_commands.py.
Method: documentation only; no commands were run.
