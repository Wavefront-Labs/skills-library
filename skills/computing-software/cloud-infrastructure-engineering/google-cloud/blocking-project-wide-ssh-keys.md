---
id: computing-software.cloud-infrastructure-engineering.google-cloud.blocking-project-wide-ssh-keys
name: blocking-project-wide-ssh-keys
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, block-project-ssh-keys, metadata-ssh-keys, ssh-key-management, os-login]
level: practitioner
status: docs-checked
description: "Stop project-wide metadata SSH keys granting access to every VM: block-project-ssh-keys per instance, audit and expire metadata keys, and move to OS Login."
sources: ["https://docs.cloud.google.com/compute/docs/connect/restrict-ssh-keys", "https://docs.cloud.google.com/compute/docs/oslogin/set-up-oslogin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocking project-wide SSH keys

Public keys in **project metadata** `ssh-keys` are accepted by every VM in the project unless the VM sets `block-project-ssh-keys=TRUE`. One stale key can mean access to all VMs.

## 1. Audit
```bash
gcloud compute project-info describe --project=<P> --format=json \
  | jq -r '.commonInstanceMetadata.items[]? | select(.key=="ssh-keys") | .value' | cut -d' ' -f1,3-
gcloud compute instances list --format='table(name,zone.basename(),metadata.items.filter(key:block-project-ssh-keys).extract(value).flatten())'
```

## 2. Block per sensitive VM
```bash
gcloud compute instances add-metadata db-1 --zone=<Z> --metadata=block-project-ssh-keys=TRUE
```
Put it in instance templates for whole MIGs.

## 3. Expire keys that must exist
```text
deploy:ssh-ed25519 AAAA... google-ssh {"userName":"deploy@example.com","expireOn":"2026-10-17T00:00:00+0000"}
```
Compute Engine treats a key past its `expireOn` as expired; when a user's last key expires or is removed, it deletes that user's `~/.ssh/authorized_keys` on the VM.

## 4. The real fix: OS Login
```bash
gcloud compute project-info add-metadata --project=<P> --metadata=enable-oslogin=TRUE
gcloud compute project-info remove-metadata --project=<P> --keys=ssh-keys
```
With OS Login on, access is IAM (`roles/compute.osLogin`, `roles/compute.osAdminLogin`); setting `enable-oslogin` to FALSE brings metadata keys back.

## Gotchas
- `remove-metadata --keys=ssh-keys` also removes keys used by automation (Ansible, old CI); inventory users first.

## Verify
- [ ] Project metadata has no `ssh-keys` entry, or every entry has `expireOn`.
- [ ] A user with only a project-wide key cannot SSH to a VM with `block-project-ssh-keys=TRUE`.

## Checked
2026-10-31. Confirmed on the Compute Engine "Restrict SSH keys" and Set up OS Login pages: `block-project-ssh-keys=TRUE` via `gcloud compute instances add-metadata`, `ssh-keys` entry format with `google-ssh {"userName","expireOn"}`, authorized_keys deletion when the last key expires, `enable-oslogin` TRUE/FALSE. Removed: claims about gcloud ssh writing project keys, root-capable access, guest-agent behaviour, `compute.requireOsLogin`, image and Windows gotchas (not on fetched pages). Commands checked with check_commands.py.
Method: documentation only; no commands were run.
