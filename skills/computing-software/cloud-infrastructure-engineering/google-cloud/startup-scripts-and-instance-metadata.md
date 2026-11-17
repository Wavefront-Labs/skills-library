---
id: computing-software.cloud-infrastructure-engineering.google-cloud.startup-scripts-and-instance-metadata
name: startup-scripts-and-instance-metadata
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, startup-script, instance-metadata, custom-metadata, shutdown-script, metadata-server]
level: practitioner
status: docs-checked
description: "Bootstrap VMs with startup and shutdown scripts, read custom metadata from the metadata server (including wait-for-change), and debug scripts that did not run."
sources: ["https://cloud.google.com/compute/docs/instances/startup-scripts/linux", "https://cloud.google.com/compute/docs/metadata/querying-metadata", "https://cloud.google.com/compute/docs/metadata/setting-custom-metadata", "https://cloud.google.com/compute/docs/shutdownscript"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Startup scripts and instance metadata

## 1. Keys the guest agent runs
| Key | When |
|---|---|
| `startup-script` (up to 256 KB) / `startup-script-url` (Cloud Storage, for scripts over 256 KB) | every boot, as root |
| `shutdown-script` / `shutdown-script-url` | before the VM stops or is preempted, best effort |
```bash
gcloud compute instances create vm1 --zone=<Z> --metadata-from-file=startup-script=./boot.sh
gcloud compute instances add-metadata vm1 --zone=<Z> --metadata=startup-script-url=gs://<B>/boot.sh,app-env=prod
```
A `*-url` script in Cloud Storage runs with the VM's service account permissions, so that account must be able to read the object. A VM-level or zonal metadata value takes precedence over the project-level value for the same key.

## 2. Write idempotent scripts
Startup scripts run on **every** boot. Guard one-time work:
```bash
#!/bin/bash
set -euo pipefail
[ -f /var/lib/bootstrap.done ] && exit 0
apt-get update && apt-get install -y nginx
ENV=$(curl -sf -H 'Metadata-Flavor: Google' http://metadata.google.internal/computeMetadata/v1/instance/attributes/app-env)
echo "env=$ENV" > /etc/app.env
touch /var/lib/bootstrap.done
```

## 3. Metadata server essentials
```bash
MD=http://metadata.google.internal/computeMetadata/v1
curl -H 'Metadata-Flavor: Google' "$MD/instance/attributes/?recursive=true"
curl -H 'Metadata-Flavor: Google' "$MD/instance/service-accounts/default/token"
curl -H 'Metadata-Flavor: Google' "$MD/project/project-id"
# block until a key changes (config reload without polling)
curl -H 'Metadata-Flavor: Google' "$MD/instance/attributes/app-config?wait_for_change=true"
```
Use `&last_etag=<etag>` with `wait_for_change` to avoid missing changes between calls; a 503 means the wait timed out with no change, so loop again.

## 4. Debug
```bash
sudo journalctl -u google-startup-scripts.service --no-pager
sudo google_metadata_script_runner startup            # rerun now
gcloud compute instances get-serial-port-output vm1 --zone=<Z> | grep -i startup-script
```

## Gotchas
- Each metadata value is limited to 256 KB and the combined total to 512 KB; larger scripts go in Cloud Storage via `startup-script-url`.
- Never put secrets in metadata: any process on the VM and anyone with `compute.instances.get` can read it. Use Secret Manager.
- Shutdown scripts run only best effort during the limited shutdown period (120 seconds between ACPI soft off and mechanical off for standard VMs, 30 seconds for Spot VMs).
- Container-Optimized OS has limited or no support for some startup script features; check its page.

## Verify
- [ ] Reboot the VM; the script's marker shows it skipped one-time work and services are up.
- [ ] `journalctl -u google-startup-scripts.service` shows the script ran without errors.

## Checked

Checked 2026-10-27 against the Linux startup scripts page, Set custom metadata, Query metadata, Run shutdown scripts and the Compute Engine v1 API discovery document (shutdown timing). Confirmed: 256 KB per value and 512 KB combined, startup-script-url for scripts above 256 KB, scripts run as root at boot, google-startup-scripts.service and google_metadata_script_runner, wait_for_change and last_etag, zonal and VM metadata precedence over project metadata, and shutdown scripts being best effort. Removed timeout_sec, the Windows keys, the cloud-init claim and the exit-status log text, none of which the documentation confirms.

Method: documentation only; no commands were run.
