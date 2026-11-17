---
id: computing-software.cloud-infrastructure-engineering.minio.software-checklist
name: software-checklist
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, software-checklist, kernel-6-6, time-sync, auditd, antivirus-exclusion, load-balancer, prerequisites, post-install]
level: practitioner
status: docs-checked
description: "Prepare hosts for a production MinIO cluster covering the 6.6+ kernel, time sync, services to disable such as auditd and mlocate, load balancer, Prometheus and post-install tasks."
sources: ["https://github.com/minio/docs/blob/main/source/operations/checklists/software.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO software checklist

## Pre-requisites
- Linux with a **6.6+ kernel** on an LTS, in-support release (RHEL 10 and Ubuntu LTS 22.04.01+ ship such kernels by default).
- Time synchronised across nodes (for example `ntp`, `timedatectl` or `timesyncd`; method varies by OS).
- Disable or uninstall services that index, scan or audit the filesystem or system calls, since they contend with or intercept MinIO operations: `mlocate` or `plocate`, `updatedb`, `auditd`, Crowdstrike Falcon, antivirus such as `clamav`. Alternatively exclude the MinIO process and all its drive paths.
- Administrator access to the servers and a management tool (Ansible, Terraform, or for Kubernetes the MinIO Operator).
- A load balancer (for example NGINX) to route requests.
- Prometheus or a compatible setup, plus Grafana for dashboards.
- Optionally `mc` on a workstation.

## Install
Install a matching MinIO version on every node.

## Post install
- Optional: `mc alias set` for each server.
- Configure bucket replication, site replication, lifecycle retention rules and tiering as required.
- Third-party identity provider tasks, including STS authentication (the checklist notes enabling it requires MinIO support).

Related: `computing-software.cloud-infrastructure-engineering.minio.hardware-checklist`, `computing-software.cloud-infrastructure-engineering.minio.security-checklist`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Software Checklist page (software.rst). Removed: the 'exclusive drive access' post-install item (not on this page).
Method: documentation only; no commands were run.
