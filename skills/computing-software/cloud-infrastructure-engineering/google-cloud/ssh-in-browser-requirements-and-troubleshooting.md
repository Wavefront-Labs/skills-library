---
id: computing-software.cloud-infrastructure-engineering.google-cloud.ssh-in-browser-requirements-and-troubleshooting
name: ssh-in-browser-requirements-and-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, os-login, ssh-in-browser, console-ssh, iap-tcp-forwarding, ssh-troubleshooting]
level: practitioner
status: docs-checked
description: "Make the console SSH button work: IAM roles, firewall from Google source ranges or IAP for VMs without external IP, OS Login vs metadata keys, and common failure messages."
sources: ["https://cloud.google.com/compute/docs/ssh-in-browser", "https://cloud.google.com/iap/docs/using-tcp-forwarding"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH-in-browser requirements and troubleshooting

The console **SSH** button opens a browser terminal. It connects either directly to the VM's
external IP, or through **IAP TCP forwarding** when the VM has only an internal IP.

## Requirements
- IAM for the IAP path: `roles/iap.tunnelResourceAccessor` (grant on the VM or project); `roles/iam.serviceAccountUser` when using a service account.
- Firewall: allow tcp:22 from `35.235.240.0/20` (IAP) for internal-IP-only VMs. For external-IP connections the VPC must allow TCP ingress from 0.0.0.0/0.
- Guest: the guest environment must be installed and running (pre-installed on Google-provided public images).
- Network: no TLS inspection of HTTPS traffic; allow hostnames ending in google.com, gstatic.com and googleapis.com.
- Supports metadata SSH keys, OS Login and IAP TCP forwarding; user-uploaded keys for OS Login must be ECDSA.

## Limitations (from the docs)
- Not supported inside VPC Service Controls perimeters; use the gcloud CLI.
- Key transfer takes 2 to 25 seconds; there is no SLA on connection lifetime, so use tmux or screen for long sessions.
- Slow large file transfers: use `gcloud compute scp`.
- SSH-in-browser is documented for Linux VMs.

## Verify
- [ ] SSH button opens a shell on a private VM via IAP with only the documented roles.

## Checked
2026-11-01. Confirmed against the SSH-in-browser page and the IAP TCP forwarding page (35.235.240.0/20, roles/iap.tunnelResourceAccessor, roles/iam.serviceAccountUser, 0.0.0.0/0 ingress for external IP, guest environment, VPC-SC limitation, 2-25 second key transfer). Removed the error-message table, osAdminLogin/requireOsLogin, google-guest-agent, --troubleshoot and serial-port advice: the troubleshooting page returned 404 and none are stated on the pages read.
Method: documentation only; no commands were run.
