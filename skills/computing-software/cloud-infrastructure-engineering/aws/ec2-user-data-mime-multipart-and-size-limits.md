---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-user-data-mime-multipart-and-size-limits
name: ec2-user-data-mime-multipart-and-size-limits
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, user-data, mime-multipart, user-data-limit, cloud-init, gzip-user-data, launch-template]
level: practitioner
status: docs-checked
description: "Build EC2 user data that combines cloud-config and scripts with MIME multipart, stays under the 16 KB limit (gzip, fetch from S3), and runs on every boot when needed."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html", "https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html", "https://cloudinit.readthedocs.io/en/latest/explanation/format.html", "https://cloudinit.readthedocs.io/en/latest/reference/cli.html", "https://cloudinit.readthedocs.io/en/latest/reference/modules.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User data: MIME multipart and size limits

## 1. Limits and encoding
- **16 KB** raw (before base64; base64 length is ceil(n/3)*4). The API wants base64. The console and
  `run-instances --user-data` encode for you; `modify-instance-attribute` and PowerShell
  `New-EC2Instance` do not.
- Keep the raw size under the limit; plan for it before relying on an in-line script.

## 2. Combining formats with MIME multipart
cloud-init supports several user-data formats (cloud-config, user-data script, boothook, include,
Jinja, cloud-config archive, gzip) and can combine them in one MIME multi-part document. User data
scripts and cloud-init directives run only on the first boot of an instance by default.
```
Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"

#cloud-config
package_update: true
packages: [amazon-cloudwatch-agent, jq]
write_files:
  - path: /etc/app/env
    permissions: '0640'
    content: |
      APP_ENV=prod

--//
Content-Type: text/x-shellscript; charset="us-ascii"

#!/bin/bash
set -euo pipefail
systemctl enable --now amazon-cloudwatch-agent
/opt/app/bootstrap.sh
--//--
```
Generate it with Python `email.mime` or by hand. On EKS managed node groups, custom user data in a
launch template is merged with EKS bootstrap data into a MIME multi-part file; AL2023 nodes take
a `NodeConfig` part (`Content-Type: application/node.eks.aws`).

## 3. Shrinking it
- gzip: cloud-init lists gzip as a supported user-data format. The 16 KB limit applies to the
  compressed bytes before base64. EC2Launch v2 on Windows supports a zipped (.zip) user data script
  as a way past the limit.
- Move the bulk to S3 (or SSM Parameter Store / Secrets Manager): user data only fetches
  and runs a versioned bootstrap script:
```bash
#!/bin/bash
aws s3 cp s3://bootstrap-bucket/app/v42/bootstrap.sh /tmp/b.sh && bash /tmp/b.sh
```
  The instance role needs `s3:GetObject` on that prefix. Keeps secrets out of user data too.
- Better long term: bake software into the AMI; keep user data for per-instance config.

## 4. Running on every boot
Shell scripts in user data run once per instance. To run each boot:
- Put the script in the cloud-init `scripts/per-boot` directory via `write_files` (the per-boot scripts
  module runs them on every boot, in alphabetical order), or
- cloud-config `bootcmd` (module frequency: always; use it only for work that cannot happen later), or
  a systemd unit installed by user data.

## 5. Debugging
- `/var/log/cloud-init-output.log` (script stdout/stderr) and `/var/log/cloud-init.log`.
- `cloud-init status --long`; `cloud-init schema --system` validates the system cloud-config.
- Retrieve what the instance received:
  `curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/user-data`.

## Gotchas
- Validate cloud-config before launch with `cloud-init schema -c config.yaml`.
- Windows: `<powershell>` tags and `<persist>true</persist>` run user data on every boot; EC2Launch v2
  also accepts YAML user data with per-task frequency.
- User data is readable by anyone with `ec2:DescribeInstanceAttribute` and from IMDS on
  the instance; never put secrets in it.

## Verify
- [ ] `wc -c ud.txt` (or gz) under 16,384 bytes; launch succeeds.
- [ ] `cloud-init status` reports `done` without errors; both parts' effects present.
- [ ] Per-boot steps re-run after a reboot.

## Checked

Date: 2026-10-27. Sources: EC2 User Guide "Run commands at launch using instance user data" (user-data.html), EKS User Guide launch templates page, cloud-init 26.2 documentation (user-data formats, CLI reference, modules reference), AWS CLI 2.38.6 run-instances reference.
Confirmed: 16 KB raw limit and base64 rule; which tools encode for you; first-boot-only default; the MIME example shape (cloud-config plus x-shellscript parts); EC2Launch v2 zipped user data and persist tag; EKS MIME merge and the node.eks.aws NodeConfig part; cloud-init commands status --long and schema --system; per-boot scripts and bootcmd run on every boot; log paths /var/log/cloud-init.log and /var/log/cloud-init-output.log.
Removed (not confirmed in those pages): the exact error string for oversize user data, per-MIME-type run semantics, the make-mime helper, the claim that EKS requires MIME, fileb:// gzip upload, and the cloud_final_modules override.

Method: documentation only; no commands were run.
