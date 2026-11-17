---
id: computing-software.cloud-infrastructure-engineering.docker.versioned-secret-names-for-swarm-rotation
name: versioned-secret-names-for-swarm-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm-secrets, versioned-secrets, secret-rotation, stack-deploy, swarm-configs, rolling-update]
level: advanced
status: docs-checked
description: "Rotate immutable Swarm secrets and configs from stack files by versioning name: (db_pw_${VER}) or content hashes, triggering rolling updates and pruning old versions."
sources: ["https://docs.docker.com/engine/swarm/secrets/", "https://docs.docker.com/engine/swarm/configs/", "https://docs.docker.com/engine/swarm/stack-deploy/", "https://github.com/compose-spec/compose-spec/blob/main/12-interpolation.md", "https://github.com/docker/cli/blob/master/cli/compose/schema/data/config_schema_v3.13.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Versioned secret names for Swarm rotation

Swarm secrets and configs are not edited in place: the Docker docs rotate a secret by creating a new one and swapping it, and suggest putting a version number in the name. So give each content
version its own name while keeping the in-container path stable.

## Pattern
```yaml
services:
  api:
    image: api:2.3
    secrets:
      - source: db_password
        target: db_password            # path stays /run/secrets/db_password
    configs:
      - source: api_config
        target: /etc/api/config.yaml
secrets:
  db_password:
    name: shop_db_password_${DB_PASSWORD_VERSION:?}
    file: ./secrets/db_password.txt
configs:
  api_config:
    name: shop_api_config_${API_CONFIG_HASH:?}
    file: ./config/api.yaml
```
```bash
export DB_PASSWORD_VERSION=7
export API_CONFIG_HASH=<short hash of config/api.yaml>
docker stack deploy -c stack.yaml --with-registry-auth shop
```
Swarm sees a new secret name in the service spec and performs a rolling update using the
service's `update_config`. A content hash for configs means "redeploy only when it changed".

## Database password rotation order
1. Add the new password to the database (both old and new valid).
2. Deploy with the new secret version; tasks roll over.
3. Remove the old password from the database.
4. Delete old secret versions with `docker secret rm <name>`.
`docker secret rm` refuses while a service still references a version, which is a useful
safety net.

## Gotchas
- Without `name:`, the object name comes from the stack name and key (stack deploy prefixes names with the stack name), so it does not change when the content does.
- Keep the version in a tracked place (CI variable, env file) so redeploys from another machine
  use the same name.
- Rolling updates with `order: start-first` briefly run old and new secrets together; the app
  must tolerate both during the window.

## Checked
2026-10-25, against docker/docs engine and swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master), the Compose specification interpolation page and the docker/cli stack schema v3.13. Confirmed: `${VAR:?err}` mandatory-variable interpolation; stack `secrets`/`configs` accept `name`, `file`, `external`; secret rotation by creating a new secret and `--secret-rm/--secret-add`; removing a secret in use fails; the docs recommend a version number in secret names; stack names prefix created objects. Removed: quoted error message, hash and cleanup shell pipelines.
Method: documentation only; no commands were run.
