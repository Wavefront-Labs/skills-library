---
id: computing-software.cloud-infrastructure-engineering.aws.cloud-init-debugging-and-user-data-rerun
name: cloud-init-debugging-and-user-data-rerun
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, user-data, cloud-init, cloud-init-log, cloud-config, user-data-rerun, bootstrap]
level: practitioner
status: docs-checked
description: "Debug EC2 user data: where cloud-init logs and scripts live, cloud-config vs shell scripts, multipart MIME, running on every boot, re-running after edits, and size limits."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html", "https://cloudinit.readthedocs.io/en/latest/reference/cli.html", "https://cloudinit.readthedocs.io/en/latest/reference/modules.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cloud-init debugging and re-running user data

## 1. Where to look (Linux)
| File | Contains |
|---|---|
| `/var/log/cloud-init-output.log` | console output of your user data script; start here |
| `/var/log/cloud-init.log` | cloud-init's own log |
| `/var/lib/cloud/instance/user-data.txt` | the user data cloud-init received (collected by `cloud-init collect-logs`) |
| `/var/lib/cloud/instances/<instance-id>/` | where a user data script is copied to and run from; it is not deleted afterwards |
```bash
cloud-init status --long          # status plus extended_status, errors, recoverable_errors
cloud-init analyze show           # time-ordered cost of operations per boot stage
sudo cloud-init schema --system   # validate the system cloud-config user data
```
`cloud-init status` exits 1 if cloud-init crashes, 2 if it finished with recoverable errors, 0 if it ran without error.
`cloud-init status --wait` blocks until cloud-init completes. `cloud-init collect-logs` tars logs and system information for triage.

## 2. Formats
- Starts with `#!`: shell script. Runs as root, so do not use `sudo`; it is not interactive, so commands that prompt
  (such as `yum update` without `-y`) will hang or fail.
- Starts with `#cloud-config`: declarative cloud-init directives (for example `packages`, `write_files`, `runcmd`).
- Both together: MIME multipart (`Content-Type: multipart/mixed`) with parts of content type `text/cloud-config` and
  `text/x-shellscript`. By default user data holds only one content type at a time.
- If the script calls AWS APIs (including the AWS CLI), the instance needs an instance profile.
- Limit: user data is 16 KB in raw form, before base64 encoding. User data must be base64-encoded; the console and
  `run-instances` in the AWS CLI encode for you, `modify-instance-attribute` does not.
- Adding work at boot lengthens boot time: allow a few minutes before judging whether the script finished.

## 3. Running again
By default user data scripts and cloud-init directives run only during the boot cycle when the instance is first
launched. Editing user data:
- The instance must be stopped (Actions, Instance settings, Edit user data in the console); when running you can only
  view it. The instance must have an EBS root volume.
- After you start the instance the new user data is visible but the scripts are **not** run.
- CLI form: `aws ec2 modify-instance-attribute --instance-id <ID> --attribute userData --value file://my_script_base64.txt`
  (base64-encode the file first).

To make cloud-init treat the next boot as a first boot, `cloud-init clean` removes artifacts from `/var/lib/cloud`
and cloud-init re-runs all stages on reboot:
```bash
sudo cloud-init clean --logs --reboot     # --logs also removes /var/log cloud-init logs; --reboot reboots afterwards
```
The cloud-init docs warn that `clean` is a best-effort simulation of a clean instance and that re-running modules is
not always idempotent. Run it on a production instance only if re-running every stage (including user setup) is safe.
For running on every boot, the cloud-init `scripts-per-boot` module runs scripts in its per-boot scripts directory
every time the system boots, in alphabetical order. The AWS page points to its Knowledge Center article for
configuring Linux instances to run user data on every restart.

## 4. Windows
- Scripts must be wrapped in `<script>` (batch) or `<powershell>` (case-sensitive) tags. If both are present, batch
  runs first.
- By default scripts run once at launch. Add `<persist>true</persist>` to run on every reboot or start. With
  EC2Launch v2, the user data task is evaluated each boot and YAML tasks use `frequency: once` or `frequency: always`.
- EC2Launch v2 logs to `agent.log` under `ProgramData\Amazon\EC2Launch\log` (the folder may be hidden).
- EC2Launch v2 accepts zipped user data for content over the 16 KB limit.

## Gotchas
- Delete user data scripts from `/var/lib/cloud/instances/<instance-id>/` before creating an AMI from the instance,
  or they remain on every instance launched from it. User data itself is not included in an AMI.
- User data is opaque to EC2; the instance interprets it.

## Verify
- [ ] `cloud-init status` reports `status: done` with no errors on a fresh instance.
- [ ] `/var/log/cloud-init-output.log` shows your script's output and any error messages.
- [ ] Bootstrap duration from `cloud-init analyze show` is acceptable for your Auto Scaling health-check grace period.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the EC2 user data page and the cloud-init CLI and modules pages: log and script locations, the 16 KB
limit, base64 handling, shell/cloud-config/multipart formats, run-once default, stop-before-edit, `clean` and its
options, `status` exit codes, `schema --system`, per-boot module, Windows tags, persist, EC2Launch v2 frequency and
zipped user data. Removed: the `part-001` path, the `cloud_final_modules ... always` override (the scripts_user module is
documented as once-per-instance), the per-boot directory path, the get-console-output claim, network-readiness and
launch-template claims, and the `/var/log/user-data.log` suggestion.
