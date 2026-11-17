---
id: computing-software.cloud-infrastructure-engineering.ansible.operating-private-automation-hub-tokens-and-backups
name: operating-private-automation-hub-tokens-and-backups
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-hub, hub-api-token, hub-backup, galaxy-server-list]
level: practitioner
status: docs-checked
description: "Configure ansible.cfg galaxy_server entries with automation hub API tokens and auth_url, keep tokens out of git with env vars, and know the token limits."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/shared_snippets/galaxy_server_list.txt", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/hub/proc-create-api-token-pah.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/hub/con-token-management-hub.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/hub/proc-revoking-token.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/platform/proc-aap-platform-gateway-backup.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Private automation hub: tokens and backups

## ansible.cfg servers
```ini
[galaxy]
server_list = pah_published, galaxy

[galaxy_server.pah_published]
url = https://hub.example.com/api/galaxy/
token = <hub API token>

[galaxy_server.galaxy]
url = https://galaxy.ansible.com/
```
- `server_list` is a prioritized list; installs search the servers in that order. The `url` of each server must end with `/`.
- Keys per server: `url` (required), `token`, `username` and `password` (basic auth; mutually exclusive with `token`), `auth_url` (Keycloak token endpoint for SSO, requires `token`), `client_id` (default `cloud-services`, for Red Hat SSO), `validate_certs`, `timeout`.
- `--server` on the command line selects one server from the list by name.
- Keep tokens out of git with environment variables of the form `ANSIBLE_GALAXY_SERVER_{ID}_{KEY}` where `{ID}` is the upper-case server id, for example `ANSIBLE_GALAXY_SERVER_PAH_PUBLISHED_TOKEN`.
- Red Hat's hosted automation hub uses an offline token with `auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token` and a URL under `https://console.redhat.com/api/automation-hub/content/published/`.

## Tokens
- Private automation hub: log in, open the API token page in the navigation panel and click Load Token. The API token does not expire; store it securely.
- The API token is meant only for `ansible-galaxy` collection operations (sync, install, publish). It is not supported for container registry operations such as `podman login` or `podman pull` of execution environment images; use username and password for those.
- The Red Hat docs state that automation hub does not support basic authentication or service accounts; authenticate with token management. Hosted automation hub uses an offline token, and a private hub that authenticates through Keycloak follows the offline token procedure too.
- Revoking Red Hat offline tokens (`POST` to the `sso.redhat.com` revoke endpoint with `client_id=cloud-services` and the refresh token) revokes all previously generated offline tokens; then generate a new one.

## Backup
- The platform operator has an `AutomationHubBackup` object; creating `AutomationControllerBackup` and `AutomationHubBackup` objects is a prerequisite step before an operator upgrade.
- Hub content storage lives under `/var/lib/pulp`, so size backup space for it.
- For installer-based backups see the aap-disaster-recovery skill.

## Verify
- [ ] `ansible-galaxy collection install <namespace>.<name> --server pah_published` succeeds from a clean machine.

## Checked
2026-11-09. Checked against the Ansible documentation galaxy server list snippet and the ansible/aap-docs hub modules (token management, creating the API token in private automation hub, revoking a token), the platform backup module (AutomationHubBackup) and the performance-tuning hub module (`/var/lib/pulp`).
Removed as unsupported: the claim that generating a new hub token invalidates the previous one (the docs say the private hub API token does not expire), the `/api/galaxy/content/published/` and `/community/` URL forms, per-consumer service-user advice, controller credential ordering claim, `setup.sh backup_dest` flag, `/var/lib/pulp` inclusion in the containerized backup playbook, S3 remark, upgrade and signature notes, and the `ansible-galaxy collection list --server` verify command.
Method: documentation only; no commands were run.
