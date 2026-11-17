---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-modify-user-data-on-existing-instance
name: ec2-modify-user-data-on-existing-instance
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, modify-user-data, user-data, cloud-init]
level: practitioner
status: docs-checked
description: "Change user data on an existing EC2 instance (stop, base64 encode, modify-instance-attribute), read it back, and make cloud-init run it again on next boot."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html", "https://docs.aws.amazon.com/cli/latest/reference/ec2/modify-instance-attribute.html", "https://cloudinit.readthedocs.io/en/latest/reference/modules.html", "https://cloudinit.readthedocs.io/en/latest/reference/cli.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing user data on an existing instance

## 1. Modify (instance must be stopped)
```bash
aws ec2 stop-instances --instance-ids i-0abc && aws ec2 wait instance-stopped --instance-ids i-0abc
base64 -w0 new-userdata.sh > ud.b64
aws ec2 modify-instance-attribute --instance-id i-0abc --attribute userData --value file://ud.b64
aws ec2 start-instances --instance-ids i-0abc
```
`modify-instance-attribute` expects the value already base64-encoded (unlike `run-instances --user-data`,
where the CLI encodes for you). Limit: 16 KB raw, before encoding.

## 2. Read it back
```bash
aws ec2 describe-instance-attribute --instance-id i-0abc --attribute userData \
  --query 'UserData.Value' --output text | base64 -d
```

## 3. Making it actually run
cloud-init runs user-data scripts once per instance by default; a changed script on reboot does nothing. Options:
- Run on every boot: write the script into the cloud-init `scripts/per-boot` directory (the per-boot scripts
  module runs every script there on every boot, in alphabetical order) or use cloud-config `bootcmd`
  (module frequency: always).
- One-off rerun: on the instance, `sudo cloud-init clean --logs && sudo reboot`. `clean` removes cloud-init
  state to simulate a clean instance, so first-boot modules run again; read its documentation before using
  it on a production host.
Windows: add `<persist>true</persist>` after the `<powershell>` or `<script>` block, or set `frequency: always`
on the task in EC2Launch v2 YAML user data.

## Gotchas
- In an ASG, change the launch template (or launch configuration) so that newly launched instances get the new user data.
- Never put secrets in user data; anyone with `ec2:DescribeInstanceAttribute` or IMDS access reads it.

## Verify
- [ ] `/var/log/cloud-init-output.log` shows the new script's output after the boot.

## Checked

Date: 2026-10-27. Sources: EC2 User Guide "Run commands at launch using instance user data"; AWS CLI 2.38.6 modify-instance-attribute reference; cloud-init 26.2 CLI and modules references.
Confirmed: the instance must be stopped, modify-instance-attribute does not base64-encode but run-instances does, userData is a modifiable attribute, describe-instance-attribute returns base64 (decode with base64 --decode), 16 KB raw limit, user data runs only on first launch by default, persist tag and frequency always on Windows, cloud-init clean --logs, per-boot scripts and bootcmd run on every boot.
Removed: the cloud_final_modules override and the claim that clean regenerates SSH host keys (not in the pages read).

Method: documentation only; no commands were run.
