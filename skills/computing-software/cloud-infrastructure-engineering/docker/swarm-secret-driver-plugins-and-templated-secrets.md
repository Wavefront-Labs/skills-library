---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-secret-driver-plugins-and-templated-secrets
name: swarm-secret-driver-plugins-and-templated-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm-secrets, secret-driver, docker-plugin, template-driver, vault, external-secrets]
level: sme
status: docs-checked
description: "Source Swarm secrets from an external store via secret driver plugins (--driver, driver_opts), templated secrets with template_driver, their limits, and safer Vault alternatives."
sources: ["https://docs.docker.com/reference/cli/docker/secret/create/", "https://github.com/docker/cli/blob/master/cli/compose/schema/data/config_schema_v3.13.json", "https://docs.docker.com/engine/swarm/secrets/", "https://docs.docker.com/engine/swarm/configs/", "https://github.com/moby/swarmkit/blob/master/template/context.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Swarm secret driver plugins and templated secrets

By default the secret value lives in the Swarm Raft store. Two extension points change that.

## 1. Secret driver plugins
`docker secret create --driver <name>` ("Secret driver") selects an external secret driver instead of the
Swarm Raft store, and the stack-file `secrets` entry accepts `driver` and `driver_opts`:
```yaml
secrets:
  db_password:
    driver: <driver-name>
    driver_opts: {}      # plugin-specific
```
The Docker documentation reviewed here does not describe the driver plugin interface or any supported plugins. Read the
plugin's own documentation, including what happens to task starts when the external store is unreachable.

## 2. Templated secrets and configs
`template_driver: golang` (CLI: `--template-driver golang`) renders Go templates on the swarm agent when the task starts, with access to task metadata
and the secrets attached to the service:
```yaml
configs:
  app_conf:
    file: ./app.conf.tmpl
    template_driver: golang
secrets:
  db_password: { external: true }
```
```text
# app.conf.tmpl
node={{ .Node.Hostname }} service={{ .Service.Name }} task={{ .Task.Slot }}
db_password={{ secret "db_password" }}
```
The rendered result is delivered to the task; the template file itself has no secret values. `secret` looks the value up by the secret's target file name on the service.

## Verify
```bash
docker secret inspect db_password
docker service ps shop_app --no-trunc       # task errors if the driver failed
```

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master), the docker/cli stack schema v3.13 and moby/swarmkit `template/` source (master). Confirmed: `docker secret create --driver` and `--template-driver` exist; stack secrets accept `driver`, `driver_opts`, `template_driver` and configs accept `template_driver`; the only template engine is `golang`, evaluated on the agent, with functions `secret`, `config`, `env` and fields `.Service.Name`, `.Node.Hostname`, `.Task.Slot`; `secret` matches the secret's target file name on the task. Removed: Vault plugin install and path examples, the plugin-maintenance claims and the Vault Agent section (no Docker documentation for them).
Method: documentation only; no commands were run.
