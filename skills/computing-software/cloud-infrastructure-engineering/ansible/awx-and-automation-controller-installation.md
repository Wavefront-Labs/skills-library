---
id: computing-software.cloud-infrastructure-engineering.ansible.awx-and-automation-controller-installation
name: awx-and-automation-controller-installation
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, awx-install, awx-operator, controller-install, automation-controller, ansible-automation-platform, aap, containerized-installer, rpm-installer, setup-sh, inventory-file-aap, postgresql, kubernetes-operator, kustomize, tls-certificates, subscription-manifest, platform-gateway, aap-2-5, sizing]
level: advanced
status: docs-checked
description: "Install AWX (operator via kustomize) or Ansible Automation Platform controller (containerized or RPM installer): prerequisites, database, TLS, admin password, sizing."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/installation/basic-install.md", "https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/network-and-tls-configuration.md", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/containerized_installation/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/rpm_installation/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/planning_your_installation/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/tested_deployment_models/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWX and automation controller installation

**Goal:** a controller you can rebuild from a committed manifest, with an external or
backed-up database, TLS that browsers trust, and the admin password stored somewhere
other than a terminal scrollback.

## 1. AWX on Kubernetes (operator)
```bash
# kustomization.yaml
resources:
  - github.com/ansible/awx-operator/config/default?ref=2.19.1
  - awx.yaml
images: [{name: quay.io/ansible/awx-operator, newTag: 2.19.1}]
namespace: awx
# awx.yaml
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata: {name: awx}
spec:
  service_type: ClusterIP
  ingress_type: ingress
  ingress_hosts:                        # hostname/ingress_tls_secret are deprecated
    - hostname: awx.example
      tls_secret: awx-tls
  postgres_configuration_secret: awx-postgres-configuration   # external DB; omit for the bundled one
  admin_password_secret: awx-admin-password
  projects_persistence: true
  projects_storage_class: nfs
  extra_settings: [{setting: MAX_UI_JOB_EVENTS, value: "4000"}]
```
```bash
kubectl apply -k .           # operator + CR
kubectl -n awx logs deploy/awx-operator-controller-manager -c awx-manager -f
kubectl -n awx get secret awx-admin-password -o jsonpath='{.data.password}' | base64 -d
```
External PostgreSQL secret keys: `host port database username password sslmode target_session_attrs type=unmanaged` (PostgreSQL 15 by default).
Pin the operator tag; upgrades are `ref=` bumps applied with `kubectl apply -k` (the operator runs the DB migrations).
Persistent projects storage must be shared if the web/task replicas are scaled out.

## 2. Ansible Automation Platform (Red Hat)
Two supported installers for 2.5:
- **Containerized** (Podman, rootless, single or multi node): extract `ansible-automation-platform-containerized-setup-bundle-*.tar.gz`, edit `inventory`, `ansible-playbook -i inventory ansible.containerized_installer.install`.
- **RPM**: `setup.sh` from the setup bundle with an `inventory` file.
Minimal containerized inventory shape (2.5, with the platform gateway in front of controller, hub, EDA):
```ini
[automationgateway]
gw.example
[automationcontroller]
ctl.example
[automationhub]
hub.example
[database]
db.example
[all:vars]
postgresql_admin_password=<SET_ME>
registry_username=<RH_REGISTRY_SERVICE_ACCOUNT>
registry_password=<SET_ME>
gateway_admin_password=<SET_ME>
gateway_pg_host=db.example
gateway_pg_password=<SET_ME>
controller_admin_password=<SET_ME>
controller_pg_host=db.example
controller_pg_password=<SET_ME>
hub_admin_password=<SET_ME>
hub_pg_host=db.example
hub_pg_password=<SET_ME>
# TLS: custom_ca_cert=, controller_tls_cert=/controller_tls_key=, gateway_tls_cert= ...
```
Keep the inventory in git with the passwords vaulted; the installer is itself an Ansible
playbook, so `-e @vault.yml --vault-id` works. Re-running the installer is the upgrade and
repair path. After install: upload the **subscription manifest** (console.redhat.com → Subscription
Allocations) or use the credentials dialog; controller is read-only until licensed.

Prereqs that bite: RHEL 9.6 or later (containerized installer), 16 GB RAM / 4 vCPU per node as in the
tested deployment models, DNS and reverse DNS, ports 443 (gateway/controller/hub), 5432 (db) and the
receptor mesh listener port, `/var/lib/awx` on fast storage (80 GB minimum with 20 GB free).

## 3. Sizing
Documented fork-capacity algorithm: RAM forks = `(mem - 2048) / mem_per_fork` (mem in MB;
`mem_per_fork` via SYSTEM_TASK_FORKS_MEM, a 4 GB node runs about 20 forks) and CPU forks =
`cpus * fork_per_cpu` (fork_per_cpu via SYSTEM_TASK_FORKS_CPU, default 4). Scale execution
nodes horizontally rather than growing control nodes. Database: separate host, PostgreSQL 15,
tune `shared_buffers` (default 128 MB); job events dominate size — schedule the management
cleanup jobs (Cleanup Job Details, Cleanup Activity Stream, Cleanup Expired Sessions) from day one.

## 4. First login checklist
Change `admin` password → create an org, an LDAP/SAML/OIDC auth mapping (the gateway
authenticators in 2.5) → set a default execution environment from your hub → galaxy credentials
for the org → disable public Galaxy if the hub mirrors it → set `AWX_TASK_ENV` proxies if needed →
schedule the Management Jobs (Cleanup Job Details, Cleanup Activity Stream, Cleanup Expired Sessions).

## Gotchas
- AWX (upstream) has no support lifecycle and the operator moves fast; AAP is the supported product with the same API. Do not mix AWX operator with AAP images.
- The bundled Postgres in the operator is fine for labs; for prod use `type: unmanaged` and your own backups.
- Containerized installer runs as a non-root user with lingering enabled; running it as root breaks the rootless layout.
- Wrong `registry_*` creds fail late (image pulls); test `podman login registry.redhat.io` first.
- Behind a corporate proxy, set `HTTP_PROXY`/`NO_PROXY` in the installer inventory *and* in controller settings (`AWX_TASK_ENV`) or EE pulls and Galaxy syncs fail.
- Browser TLS errors after install mean the gateway cert was not set; set `custom_ca_cert` and the per-service cert/key.

## Verify
- [ ] `https://<host>/api/v2/ping/` (controller) returns version, instance groups and an active instance; `kubectl -n awx get awx awx -o yaml` shows no reconcile errors (operator).
- [ ] Admin login works and the licence/subscription page shows the manifest as valid.
- [ ] A demo job template runs successfully on the default execution environment.
- [ ] Re-running the installer (or `kubectl apply -k`) is a no-op.

## Checked

- 2026-10-31: kustomize pattern (`github.com/ansible/awx-operator/config/default?ref=<tag>`, images newTag, namespace), `apiVersion: awx.ansible.com/v1beta1`, `kubectl apply -k`, `service_type`/`ingress_type` values, `postgres_configuration_secret` secret keys, `admin_password_secret` (and the `<resourcename>-admin-password` retrieval command), `projects_persistence`, and `extra_settings` format confirmed against the awx-operator GitHub docs (basic-install, network-and-tls, database-configuration, admin-user-account-configuration, extra-settings). Containerized bundle name, `ansible-playbook -i inventory ansible.containerized_installer.install`, inventory variable names (postgresql_admin_password, registry_username, automationgateway_*/automationhub_* RPM names with controller_*/hub_* container names), subscription manifest via Subscription Allocations, RHEL 9.6+, PostgreSQL 15 and the capacity algorithm confirmed against the AAP 2.5 containerized/RPM installation and planning guides. `hostname`/`ingress_tls_secret` are documented as deprecated in favour of `ingress_hosts`.
- Removed: `replicas`, `web_resource_requirements`/`task_resource_requirements` CR fields and the ~120-forks figure (undocumented); the wrong fork formula replaced with the documented one; the 27199/chrony specifics replaced with the documented requirements.
Method: documentation only; no commands were run.
