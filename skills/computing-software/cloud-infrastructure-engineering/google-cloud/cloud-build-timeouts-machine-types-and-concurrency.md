---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-build-timeouts-machine-types-and-concurrency
name: cloud-build-timeouts-machine-types-and-concurrency
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-build, build-timeouts, build-machine-type, concurrency, waitfor]
level: practitioner
status: docs-checked
description: "Make Cloud Build faster and predictable: build and step timeouts, queue TTL, machine types and disk size, parallel steps with waitFor, concurrency quotas, and private pool sizing."
sources: ["https://cloud.google.com/build/docs/build-config-file-schema", "https://cloud.google.com/build/docs/optimize-builds/increase-vcpu-for-builds", "https://cloud.google.com/build/docs/configuring-builds/configure-build-step-order", "https://cloud.google.com/build/quotas"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Build timeouts, machine types and concurrency

## 1. Timeouts
```yaml
timeout: 3600s           # whole build; default 60 minutes, maximum 24 hours
queueTtl: 1800s          # build expires (status EXPIRED) if queued longer than this
steps:
- id: test
  name: node:20
  entrypoint: npm
  args: [test]
  timeout: 900s          # per step
```
`gcloud builds submit --timeout=1h` sets it at submit time. Timed-out builds get status `TIMEOUT`. A step with no `timeout` runs until it completes or the build times out.

## 2. Machine type and disk
```yaml
options:
  machineType: E2_HIGHCPU_8      # also E2_HIGHCPU_32, E2_MEDIUM, E2_STANDARD_2; N1_HIGHCPU_8/32 are deprecated
  diskSizeGb: 200
```
The default pool runs builds on a standard VM; high-CPU types run faster but can increase startup time because the default pool starts non-standard machines on demand. Pricing: see the vendor pricing page.
Private pools: `options.pool.name: projects/<P>/locations/<R>/workerPools/<POOL>`; machine type is set on the pool (`--worker-machine-type`, `--worker-disk-size`).

## 3. Parallel steps
```yaml
steps:
- {id: deps, name: node:20, entrypoint: npm, args: [ci]}
- {id: lint, name: node:20, entrypoint: npm, args: [run, lint], waitFor: [deps]}
- {id: unit, name: node:20, entrypoint: npm, args: [test], waitFor: [deps]}
- {id: build, name: gcr.io/cloud-builders/docker, args: [build, -t, $_IMG, .], waitFor: ['-']}   # '-' starts immediately
- {id: push, name: gcr.io/cloud-builders/docker, args: [push, $_IMG], waitFor: [lint, unit, build]}
```

## 4. Concurrency
- Default pool: quotas apply per region to concurrent E2 CPUs and to concurrent builds (see the Cloud Build quotas page for current limits).
- Private pool: quotas apply per region to concurrent CPUs by machine family; when the quota is full, requests for more CPUs are queued and processed serially.
- Caching (`--cache-from`) and excluding files from the upload (`.gcloudignore` or `--ignore-file`) often save more time than bigger machines.

## Gotchas
- Local source uploads skip files listed in `.gcloudignore` (or the `--ignore-file`); without one, gcloud falls back to a generated ignore based on `.gitignore`.

## Verify
- [ ] `gcloud builds describe <ID>` shows step timings; parallel steps overlap in the build timeline.

## Checked

2026-10-27. Confirmed in the build config schema page, the Build and BuildOptions discovery schemas (cloudbuild v1), the increase-vCPU page, the step-order page, the quotas page and the `gcloud builds submit` reference: default build timeout 60 minutes and maximum 24 hours, `queueTtl` and the EXPIRED status, per-step timeout behaviour, `machineType` enum values (N1_HIGHCPU_* deprecated), `waitFor: ['-']`, default pool standard VM and on-demand start of non-standard machines, quota structure, `--timeout`, `--ignore-file`, `.gcloudignore` fallback. Removed: the 10-minute default and 30-minute queue claims (wrong), the `/workspace` race gotcha, unconfirmed `--format` projection, cost claims. Read end to end.

Method: documentation only; no commands were run.
