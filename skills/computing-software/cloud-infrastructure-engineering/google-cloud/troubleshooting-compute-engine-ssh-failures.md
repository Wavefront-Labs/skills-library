---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-compute-engine-ssh-failures
name: troubleshooting-compute-engine-ssh-failures
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, ssh-troubleshooting, ssh-timeout, guest-agent-ssh, os-login, iap-tunnel, serial-console]
level: practitioner
status: docs-checked
description: "Diagnose gcloud compute ssh failures layer by layer: the troubleshoot flag, IAP firewall range, guest agent, full disks and the serial console."
sources: ["https://docs.cloud.google.com/compute/docs/troubleshooting/troubleshooting-ssh-errors", "https://docs.cloud.google.com/compute/docs/troubleshooting/troubleshooting-using-serial-console"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Compute Engine SSH failures

## 0. Let gcloud check first
```bash
gcloud compute ssh vm1 --zone=<ZONE> --troubleshoot --tunnel-through-iap
```
The SSH troubleshooting tool asks permission to run its tests, reports why the connection fails and gives
remediation steps. Use `--tunnel-through-iap` when you connect through IAP TCP forwarding. Without
`networkmanagement.connectivitytests.create`, `.delete` and `.get` on the VM it skips the network connectivity tests.

## 1. Read the symptom
| Symptom | Layer | Check |
|---|---|---|
| IAP error `4003: 'failed to connect to backend'` | network | firewall rule must allow `35.235.240.0/20`, the range IAP uses for TCP forwarding; confirm sshd is listening |
| Password prompt `USERNAME@compute.INSTANCE_ID's password:` | identity | see the matching section of the SSH errors page |
| Hangs after auth, or connection closed | guest | disk full, guest agent not running, broken `sshd_config` |

## 2. Network checks
```bash
gcloud compute firewall-rules list --filter='direction=INGRESS AND allowed[].ports:22' \
  --format='table(name,network,sourceRanges.list(),targetTags.list())'
gcloud network-management connectivity-tests create ssh-test --source-ip-address=<SOURCE_IP> \
  --destination-instance=projects/<PROJECT_ID>/zones/<ZONE>/instances/vm1 --destination-port=22 --protocol=TCP
```

## 3. Guest checks without SSH
```bash
gcloud compute instances get-serial-port-output vm1 --zone=<ZONE>
gcloud compute instances add-metadata vm1 --zone=<ZONE> --metadata=serial-port-enable=TRUE
gcloud compute connect-to-serial-port vm1 --zone=<ZONE>
```
- Interactive serial port access is disabled by default. `serial-port-enable` on the instance overrides the
  project setting (TRUE or FALSE). `connect-to-serial-port --dry-run` prints the SSH command it would run.
- In the serial console check the guest agent: `systemctl status google-guest-agent.service`, then
  `systemctl enable` and `systemctl start` it if stopped.
- Interactive console login needs a local user with a password. If none is set, a metadata startup script
  can set one (the SSH errors page shows `echo 'root:NEW_PASSWORD' | chpasswd`); remove it afterwards.
- A full disk: a startup script can delete files you know about; delete the `startup-script` metadata after you connect.

## Gotchas
- Check organization policy for serial port access before relying on the serial console.
- Test from Cloud Shell to separate local-network problems from IAP problems.

## Verify
- [ ] `--troubleshoot` reports no failing checks.
- [ ] SSH works with the user's own identity and no shared keys.

## Checked
2026-10-28. Confirmed against the Compute Engine "Troubleshoot SSH errors" page (troubleshoot flag,
permissions, IAP range, error 4003, guest agent unit, startup script remedies) and the serial console
page (`serial-port-enable`, `connect-to-serial-port`, `--dry-run`). Commands were checked against the
gcloud reference. Removed: IAP error 4033, `actAs`, OS Login role names, `block-project-ssh-keys`,
`getent`, the serial-port org policy name, WebSocket proxy claim and OS Login timing claims (not confirmed).
Method: documentation only; no commands were run.
