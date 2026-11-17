---
id: computing-software.cloud-infrastructure-engineering.google-cloud.vm-manager-and-os-patching
name: vm-manager-and-os-patching
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vm-manager, os-config, os-patch, patch-management, os-policy, os-policy-assignments, os-inventory, patch-deployment, patch-jobs, vulnerability-reports, compliance-reporting, osconfig-agent, guest-policies, fleet-patching]
level: practitioner
status: docs-checked
description: "Patch Compute Engine fleets with VM Manager: enable OS Config, schedule patch deployments with reboot and rollout controls, enforce OS policies, read inventory and CVE reports."
sources: ["https://cloud.google.com/compute/docs/vm-manager", "https://cloud.google.com/compute/docs/os-patch-management", "https://cloud.google.com/compute/docs/os-configuration-management/working-with-os-policies", "https://cloud.google.com/compute/docs/instances/os-inventory-management", "https://cloud.google.com/compute/docs/instances/view-os-details"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM Manager and OS patching

**Goal:** every VM reports its installed packages and CVEs, is patched on a schedule you
control (with reboots in the window you chose), and drifts back to policy if someone hand-edits it.

## 1. Enable
- Enable the OS Config API and set metadata `enable-osconfig=TRUE` at project level (`gcloud compute project-info add-metadata --metadata=enable-osconfig=TRUE`).
- VMs without external access can use Cloud NAT or another proxy to reach external update sources.
- Check: `gcloud compute os-config inventories list --location=<ZONE>` lists the VMs with inventory data.

## 2. Patch deployments
```bash
gcloud compute os-config patch-deployments create weekly-prod \
  --file=patch.yaml
```
`patch.yaml`:
```yaml
instanceFilter:
  groupLabels: [{labels: {env: prod}}]
  zones: [europe-west1-b, europe-west1-c]
patchConfig:
  rebootConfig: DEFAULT        # ALWAYS | NEVER | DEFAULT (the agent decides from signals such as /var/run/reboot-required)
  apt: {type: DIST, excludes: [docker-ce*]}
  yum: {security: true}
  windowsUpdate: {classifications: [CRITICAL, SECURITY]}
  preStep:  {linuxExecStepConfig: {gcsObject: {bucket: ops-scripts, object: drain.sh, generationNumber: 1}}}
  postStep: {linuxExecStepConfig: {gcsObject: {bucket: ops-scripts, object: verify.sh, generationNumber: 1}}}
recurringSchedule:
  timeZone: {id: Europe/London}
  frequency: WEEKLY
  weekly: {dayOfWeek: TUESDAY}
  timeOfDay: {hours: 2}
rollout:
  mode: ZONE_BY_ZONE
  disruptionBudget: {percent: 10}
duration: 3600s
```
- `rollout.mode: ZONE_BY_ZONE` patches one zone at a time (starting with the zone with the fewest targeted VMs); `CONCURRENT_ZONES` patches all zones at once. `disruptionBudget` is the maximum number or percentage of VMs per zone disrupted at a time.
- MIG instances: VM Manager does not patch VMs in a managed instance group unless you opt in (`migInstancesAllowed` / `--mig-instances-allowed`). A MIG that repairs or autoscales recreates VMs from the instance template, which can revert them to an unpatched state, so prefer patching the image and rolling the template (see `custom-images-and-image-pipelines`).
- One-off: `gcloud compute os-config patch-jobs execute --instance-filter-all --dry-run` (instances are contacted but not patched) then without `--dry-run`; watch with `patch-jobs list-instance-details`.

## 3. OS policies (desired state)
```yaml
osPolicies:
- id: ops-agent
  mode: ENFORCEMENT
  resourceGroups:
  - resources:
    - id: ops-agent-pkg
      pkg: {desiredState: INSTALLED, apt: {name: google-cloud-ops-agent}}
    - id: sshd-config
      file: {path: /etc/ssh/sshd_config.d/99-hardening.conf, state: PRESENT,
             content: "PasswordAuthentication no\nPermitRootLogin no\n", permissions: "0644"}
instanceFilter: {inclusionLabels: [{labels: {env: prod}}]}
rollout: {disruptionBudget: {percent: 20}, minWaitDuration: 300s}
```
`gcloud compute os-config os-policy-assignments create ops-baseline --location=<ZONE> --file=policy.yaml`.
Modes: `VALIDATION` only reports compliance; `ENFORCEMENT` also changes resources to the desired state. In `exec` resources a validate script exits **100** when compliant and **101** when not (which runs `enforce`), and an enforce script exits 100 to report its changes were made.
Assignments are **zonal**: create one per zone (a project can have at most 20 OS policy assignments per zone unless the quota is raised).

## 4. Inventory and vulnerabilities
- `gcloud compute os-config vulnerability-reports describe <VM> --location=<ZONE>` shows the vulnerability report for a VM.
- CVE information appears in VM Manager, Security Command Center and Cloud Asset Inventory within about two hours of a package change; the OS Config agent scans inventory every 10 minutes by default (`osconfig-poll-interval` metadata, in minutes). Cloud Asset Inventory has an `os-inventory` content type for fleet-wide queries.

## Gotchas
- Apt patching runs `apt-get update && apt-get upgrade` (`type: DIST` runs `dist-upgrade`); yum patching runs `yum update`.
- `rebootConfig: DEFAULT` lets the agent decide from signals such as registry keys or `/var/run/reboot-required`.
- The schedule's `timeZone` defines what `timeOfDay` is relative to, and daylight saving rules follow that time zone.

## Verify
- [ ] Every production VM appears in `inventories list` with a recent `updateTime`.
- [ ] Dry-run patch job lists expected instances only; real run shows `SUCCEEDED` (or `SUCCEEDED_REBOOT_REQUIRED`) per instance.
- [ ] `gcloud compute os-config os-policy-assignment-reports list --location=<ZONE> --assignment-id=ops-baseline` shows the VMs as compliant.
- [ ] Vulnerability report shows fewer CVEs after the patch run.

## Checked
2026-10-27. Confirmed against the OS Config discovery document (PatchConfig, PatchRollout modes, AptSettings, YumSettings, schedule fields, OS policy file and exec resource schemas), gcloud reference pages for os-policy-assignments create/update/describe/list-revisions, os-policy-assignment-reports list, inventories list/describe, vulnerability-reports describe (all take --location with a zone name, not --zone), and the VM Manager, OS patch management, working-with-OS-policies, view-os-details and OS inventory pages (enable-osconfig metadata, osconfig-poll-interval, 10-minute scan, two-hour CVE latency, MIG behaviour, policy modes, exit codes 100 and 101, zonal assignments and the 20-per-zone limit). Removed: Google-image and SA-must-exist claims, hourly re-apply claim, the sshd restart exec resource (its validate script could never trigger enforce), Terraform resource name, held-package and first-boot claims, kernel-versus-library reboot claim. Corrected: --zone replaced by --location in the os-config commands.
Method: documentation only; no commands were run.
