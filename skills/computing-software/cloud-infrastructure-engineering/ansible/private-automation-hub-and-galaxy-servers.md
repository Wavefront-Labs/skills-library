---
id: computing-software.cloud-infrastructure-engineering.ansible.private-automation-hub-and-galaxy-servers
name: private-automation-hub-and-galaxy-servers
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-hub, private-automation-hub, galaxy-ng, pulp, galaxy, galaxy-server-list, server-list, collection-sync, requirements-sync, certified-collections, validated-content, approval-workflow, staging-repo, execution-environment-registry, container-registry, air-gapped-collections, galaxy-token, offline-token, pulp-remote, requirements-file-remote, offline-install, collection-tarball]
level: advanced
status: gated
description: "Run and consume a private automation hub (galaxy_ng/Pulp): server_list with tokens, sync certified/community collections, approve staging uploads, host EE images."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/managing_automation_content/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/rpm_installation/", "https://docs.ansible.com/projects/ansible/latest/collections_guide/collections_installing.html", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Private automation hub and Galaxy servers

**Goal:** every collection and execution environment used in production comes from a
server you control, with versions pinned, uploads reviewed, and no laptop pulling from
public Galaxy at deploy time.

## 1. Client configuration (`ansible.cfg`)
```ini
[galaxy]
server_list = hub_published, hub_certified, hub_community, galaxy

[galaxy_server.hub_published]        # your own approved collections
url = https://hub.example/api/galaxy/content/published/
token = <HUB_TOKEN>                  # from the hub UI "API token"; or use env ANSIBLE_GALAXY_SERVER_HUB_PUBLISHED_TOKEN

[galaxy_server.hub_certified]        # Red Hat certified, synced from console.redhat.com
url = https://hub.example/api/galaxy/content/rh-certified/
token = <HUB_TOKEN>

[galaxy_server.hub_community]        # community content synced from galaxy.ansible.com
url = https://hub.example/api/galaxy/content/community/
token = <HUB_TOKEN>

[galaxy_server.galaxy]               # last resort / dev only; remove in production
url = https://galaxy.ansible.com/
```
Resolution tries servers **in order** and uses the first that has the collection; put
`published` first so an internal fork wins over community. Env form of any key:
`ANSIBLE_GALAXY_SERVER_<NAME>_<KEY>`. `ansible-galaxy collection install -r requirements.yml -vvv`
shows which server served each collection. Console.redhat.com can also be configured as a Galaxy server using an offline token and its
`auth_url` token endpoint (see the collections guide's SSO examples for the `auth_url` form).

## 2. Populating the hub
- **Sync remotes** (UI: Collections → Repository Management → Remotes): `rh-certified` needs the
  console.redhat.com offline token and sync URL; `community` points at `https://galaxy.ansible.com/api/`
  with a `requirements.yml` listing exactly which collections (and versions) to mirror — never "sync all".
  Schedule syncs; each sync pulls new versions matching the requirement.
- **Upload** your own: `ansible-galaxy collection publish acme-platform-2.1.0.tar.gz --server hub_published`
  → lands in **staging**; an approver (Collection Curator role) moves it to `published`
  (the installer's `automationhub_require_content_approval` setting controls this). Rejected uploads go to `rejected`.
- **Signing**: hub can sign collections (installer settings such as `automationhub_create_default_collection_signing_service` and the signing key variables); clients verify with
  `ansible-galaxy collection install --keyring pubring.kbx --required-valid-signature-count all`.
- **Execution environments**: the hub includes a container registry — `podman login hub.example`,
  `podman push hub.example/acme/ee-platform:2.1`; use it as the EE image source in controller.
- **Namespaces** map to permissions; create `acme` before the first upload and give the CI
  service account "Upload to namespace".

## 3. Air-gapped
Export from a connected hub or build a bundle: `ansible-galaxy collection download -r requirements.yml -p bundle/`
(includes dependencies and a `requirements.yml`), move it, then publish each tarball to the offline hub
or install straight from the directory (`-r bundle/requirements.yml` with `type: file` entries).
Container images: `podman save`/`skopeo copy --all` into the hub registry.

## 4. API and automation
The `infra.aap_configuration` collection automates hub namespaces, remotes, syncs and groups
(roles `hub_collection_remote`, `hub_namespace`, `hub_group`, `hub_group_roles`; see its docs for
the variable format). `ansible.hub` is the certified module collection behind them.
Back up the Pulp database and its artifact storage (file storage path) together.

## Gotchas
- A hub token in `ansible.cfg` committed to git is a leaked credential; use env vars or the vault-ed `token` via `ANSIBLE_GALAXY_SERVER_*` in CI.
- `server_list` order silently decides which copy of `community.general` you get — a stale mirror can downgrade you. Pin versions in `requirements.yml`.
- Sync requirements `version: ">=8.0.0"` keeps pulling every new release; prefer explicit ranges and periodic review.
- Uploads with an already-published version are rejected; bump the version.
- The hub's `community` remote only syncs collections listed in its requirements; a missing collection means "add it to the sync list", not a client misconfiguration.
- Certified sync requires a current console.redhat.com token; expired offline tokens surface as 401 in sync tasks.

## Verify
- [ ] `ansible-galaxy collection install acme.platform -vvv` shows `Found ... on hub_published` and never reaches public Galaxy.
- [ ] A new upload appears in staging and is absent from clients until approved.
- [ ] `podman pull hub.example/acme/ee-platform:2.1` works from a controller execution node.
- [ ] With the public Galaxy entry removed from `server_list`, a clean project installs everything in `requirements.yml`.

## Checked

- 2026-10-31: `server_list` with per-server `url` (trailing slash required) and `token`, the `ANSIBLE_GALAXY_SERVER_<name>_<key>` environment-variable form, `auth_url`/`client_id` options, GPG keyring verification (`--keyring`, `GALAXY_REQUIRED_VALID_SIGNATURE_COUNT`), offline downloads (`ansible-galaxy collection download`) and the `publish`/`info`/`install` commands confirmed in the Ansible collections guide. rh-certified and community remotes, requirements-file-driven sync, offline/API tokens, approval pipelines, container registry in the hub, and `automationhub_require_content_approval` plus signing-service installer variables confirmed in AAP 2.5 Managing automation content and the RPM installation guide. `hub_collection_remote`/`hub_namespace`/`hub_group`/`hub_group_roles` role names confirmed in the redhat-cop roles listing.
- Removed: the `GALAXY_REQUIRE_CONTENT_APPROVAL`/`GALAXY_COLLECTION_SIGNING_SERVICE` setting names (replaced with documented installer variables), the `infra.ah_configuration.ah_*` role names (superseded by `hub_*` roles in `infra.aap_configuration`) and the `/api/galaxy/v3/...`/`/pulp/api/v3/` REST paths (not re-verifiable; galaxy-ng docs serve only a landing page).
- The galaxy-ng content endpoint path form (`/api/galaxy/content/<repository>/`) is kept as an example (gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
