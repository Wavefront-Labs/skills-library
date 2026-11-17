---
id: computing-software.cloud-infrastructure-engineering.ansible.installing-private-automation-hub
name: installing-private-automation-hub
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-hub, private-automation-hub, hub-install, hub-installer, aap-installer, containerized-installer, aap-operator, galaxy-ng, pulp-storage]
level: advanced
status: docs-checked
description: "Install private automation hub with the AAP RPM or containerized installer or the operator: inventory variables, database, shared storage for Pulp, TLS, sizing."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/containerized_installation/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/rpm_installation/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/managing_automation_content/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing private automation hub

Goal: a supported private automation hub (galaxy_ng + Pulp) that serves collections and EE
images to controller and developers, with storage and database that survive upgrades.

## Pick the install method
| Method | When |
|---|---|
| RPM installer (`setup.sh`) | Existing RHEL VM estates |
| Containerized installer (AAP 2.5+) | New VM installs; podman on RHEL 9 |
| Operator on OpenShift (`AutomationHub` CR, or platform CR in 2.5) | You already run controller on OpenShift |
Upstream galaxy_ng without a subscription is possible (pulp-operator / container compose) but unsupported.

## Containerized installer (2.5) inventory excerpt
```ini
[automationhub]
hub1.example.com

[database]
db1.example.com              # or omit and point at an external PostgreSQL 15

[all:vars]
postgresql_admin_username=postgres
postgresql_admin_password=<PG_ADMIN_PASSWORD>
hub_admin_password=<HUB_ADMIN_PASSWORD>
hub_pg_host=db1.example.com
hub_pg_password=<HUB_DB_PASSWORD>
hub_tls_cert=/path/to/hub.crt
hub_tls_key=/path/to/hub.key
# multiple hub nodes need shared storage (NFS with RWX):
# hub_shared_data_path=nfs.example.com:/exports/hub
```
```bash
ansible-playbook -i inventory ansible.containerized_installer.install
```
The RPM installer uses the same idea with the `automationhub_*` inventory names
(`automationhub_admin_password`, `automationhub_pg_host`, `automationhub_pg_password`,
`automationhub_ssl_cert`/`automationhub_ssl_key`), then `./setup.sh`. The installation guide has
the full RPM-vs-containerized variable mapping table — check it for your version.

## Operator (OpenShift)
The AAP operator deploys automation hub from an `AutomationHub` custom resource; shared (RWX) or
object storage is required for multi-replica hubs. See "Installing on OpenShift Container Platform"
in the AAP 2.5 documentation for the current CR fields.

## Sizing and storage
- Artifacts (collection tarballs and EE image layers) live in Pulp storage — plan for EE images: 100–500 GB is common.
- More than one hub node requires shared storage (NFS / RWX / S3); local disks diverge.
- Back up the DB and the storage together (see backup skill); one without the other is useless.

## After install
1. Log in as admin, create an API token, add the Red Hat certified remote (offline token) and sync
   (Automation Content → Remotes).
2. Create namespaces and groups (see the namespaces/RBAC skill).
3. Configure controller: Galaxy/Automation Hub credentials per org, container registry credential for EE pulls.
4. Trust the hub's CA on controller nodes and developer machines (`podman` and `ansible-galaxy` both validate TLS).

## Gotchas
- A self-signed cert makes `ansible-galaxy` fail with SSL errors; distribute the CA rather than disabling validation.
- Firewall: 443 to hub from controller, execution nodes (EE pulls) and developer networks.
- The installer re-run is the upgrade path; never hand-edit generated settings files that the installer will overwrite.

## Verify
- [ ] The hub's API status endpoint answers and lists healthy workers.
- [ ] `ansible-galaxy collection install ansible.posix -s <hub rh-certified endpoint URL> --token <HUB_TOKEN>` works after a sync.
- [ ] `podman login hub.example.com` and a push/pull of a test image succeed.

## Checked

- 2026-10-31: containerized installer command (`ansible-playbook -i inventory
ansible.containerized_installer.install`), the hub container variable names (`hub_admin_password`,
`hub_pg_host`, `hub_pg_password`, `hub_tls_cert`/`hub_tls_key`, `hub_shared_data_path` NFS/RWX,
`hub_storage_backend`), the RPM `automationhub_*` equivalents, PostgreSQL 15, required shared
storage for HA hubs, offline/API tokens and rh-certified/community remotes all confirmed in the
AAP 2.5 installation guides (containerized, RPM) and Managing automation content.
- Removed: the `AutomationHub` CR field block (`file_storage_storage_class` etc. — not in the fetched
  OpenShift installation doc; replaced with a pointer) and the specific galaxy/pulp status and
  content endpoint URLs.
Method: documentation only; no commands were run.
