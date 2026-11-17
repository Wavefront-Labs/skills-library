---
id: computing-software.cloud-infrastructure-engineering.google-cloud.patch-pre-post-scripts-and-reboot-settings
name: patch-pre-post-scripts-and-reboot-settings
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vm-manager, patch-pre-post-scripts, patch-reboot-config, os-config, patch-jobs, pre-step-post-step]
level: practitioner
status: docs-checked
description: "Add pre-patch and post-patch scripts to VM Manager patch jobs (drain, stop services, health check), choose reboot behaviour, and read per-VM script results."
sources: ["https://docs.cloud.google.com/compute/vm-manager/docs/patch/create-patch-job", "https://docs.cloud.google.com/sdk/gcloud/reference/compute/os-config/patch-jobs/execute", "https://docs.cloud.google.com/sdk/gcloud/reference/compute/os-config/patch-jobs/list-instance-details", "https://osconfig.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patch pre/post scripts and reboot settings

## Scripts
A patch job takes one pre-patch and one post-patch script for Linux and one of each for Windows; Linux scripts run only on Linux VMs and Windows scripts only on Windows VMs. Pre-patch runs before patching (before any required reboot); post-patch runs after patching and after any reboot. A VM whose pre or post step fails counts against the disruption budget.

Scripts live on the VM (absolute path) or in a **versioned** Cloud Storage bucket as `gs://BUCKET/OBJECT#GENERATION`. Linux scripts need a shebang line (for example `#!/bin/bash`).
```bash
gcloud compute os-config patch-jobs execute --instance-filter-group-labels=env=prod,role=web \
  --display-name="web-oct" \
  --pre-patch-linux-executable=gs://ops-scripts/drain.sh#<GENERATION> \
  --post-patch-linux-executable=gs://ops-scripts/healthcheck.sh#<GENERATION> \
  --pre-patch-linux-success-codes=0,10 \
  --reboot-config=default --rollout-mode=zone-by-zone --rollout-disruption-budget-percent=25
```
- `--pre-patch-linux-success-codes` and the other three `*-success-codes` flags set the exit codes treated as success; the API default (`allowedSuccessCodes`) is `[0]`.
- Windows: `--pre-patch-windows-executable` and `--post-patch-windows-executable` (the docs show `.cmd` and `.ps1` scripts; the REST `interpreter` is `SHELL` or `POWERSHELL`).
- If a Cloud Storage object is not publicly readable, the service account attached to the VM needs IAM permission to read it. If your org enforces the Resource Location Restriction constraint, keep script buckets in permitted locations.
- In the console, picking a Cloud Storage script uses the latest object version by default.

Typical drain script: take the VM out of load balancing (for example by flipping a flag your health endpoint reads), stop the app, flush caches. Post script: start the app, wait for the health endpoint, put the VM back.

## Reboot config
| Value | Behaviour (per docs) |
|---|---|
| `default` | the agent checks well-known OS signals to decide; multiple reboots may occur, possibly before patches are installed |
| `always` | the machine reboots after the update completes |
| `never` | no reboot; in some cases not all patches are fully applied |

## Results
```bash
gcloud compute os-config patch-jobs list-instance-details <JOB_ID> \
  --format="table(name.basename(),state,failureReason,attemptCount)"
```
Per-instance `state` values include `FAILED` and `TIMED_OUT`; `failureReason` and `attemptCount` are fields of the instance details. For `NO_AGENT_DETECTED` or `TIMED_OUT` check that the VM is running, VM Manager setup and network access to the OS Config API. The OS Config agent logs to Cloud Logging (filter by patch job ID) and the serial console; set metadata `osconfig-log-level=debug` for debug logging.

## Gotchas
- A patch job times out if it does not finish within its `--duration`; no new work starts after the window ends, though downloads or reboots in progress may run past it.
- A single patch job patches at most 500 VMs, simultaneously unless you set rollout options.
- VMs in MIGs are skipped unless `migInstancesAllowed` is true.

## Verify
- [ ] Test job on one VM shows pre/post steps succeeded and the app returned to load balancing.

## Checked
2026-10-28. Confirmed against the "Create a patch job" page (script counts and order, shebang, versioned buckets, IAM note, reboot option wording, debug steps, 500-VM limit, MIG rule), the gcloud `patch-jobs execute` reference (script and success-code flags, rollout flags) and the OS Config v1 discovery document (`allowedSuccessCodes` default, `failureReason`, `attemptCount`, instance states). Removed: the unverified root/SYSTEM and timeout claims, the post-script-always-runs claim, OS reboot file paths, the exact error string and log name, and a specific gcloud backend command.
Method: documentation only; no commands were run.
