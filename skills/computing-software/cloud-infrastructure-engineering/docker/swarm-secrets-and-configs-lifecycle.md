---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-secrets-and-configs-lifecycle
name: swarm-secrets-and-configs-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm, swarm-secrets, swarm-configs, docker-secret, secret-create, secret-rotation, config-create, config-mount-target, external-secret, stack-secrets, secret-target, secret-mode, config-template, templating]
level: advanced
description: "Create, mount and rotate Swarm secrets and configs: targets, uid/gid/mode, external secrets in stacks, versioned names for rotation, and Go-templated configs."
sources: ["https://docs.docker.com/engine/swarm/secrets/", "https://docs.docker.com/engine/swarm/configs/", "https://docs.docker.com/reference/cli/docker/config/create/", "https://docs.docker.com/reference/cli/docker/service/update/", "https://github.com/docker/cli/blob/master/cli/compose/schema/data/config_schema_v3.13.json", "https://github.com/moby/swarmkit/blob/master/template/context.go"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Swarm secrets and configs lifecycle

## Create
```sh
printf '%s' "$DB_PASSWORD" | docker secret create db_password_v1 -     # stdin: not in shell history
docker secret create tls_key_v1 ./tls.key
docker config create nginx_conf_v1 ./nginx.conf
docker secret ls; docker secret inspect db_password_v1                 # metadata only, never the value
```
Secrets are stored in the encrypted Raft log and mounted in an in-memory filesystem at `/run/secrets/<target>` (Linux). Configs are not encrypted at rest on the node and are mounted
into the container filesystem without a RAM disk (default path `/<config-name>`). Neither is edited in place - rotate by creating a new object.

## Mounting with target, ownership and mode
```yaml
services:
  api:
    secrets:
      - source: db_password_v2
        target: db_password            # stable filename regardless of version
        uid: "10001"
        gid: "10001"
        mode: 0400
    configs:
      - source: nginx_conf_v1
        target: /etc/nginx/conf.d/default.conf
        mode: 0444
secrets:
  db_password_v2:
    external: true                     # created out of band with docker secret create
  api_key:
    file: ./secrets/api_key            # created by stack deploy
    name: shop_api_key_v3              # explicit name for versioning
configs:
  nginx_conf_v1:
    file: ./nginx.conf
```

## Rotation (immutable objects)
```sh
printf '%s' "$NEW" | docker secret create db_password_v2 -
docker service update --secret-rm db_password_v1 \
  --secret-add source=db_password_v2,target=db_password shop_api
docker secret rm db_password_v1          # fails while any service still uses it
```
A rolling update restarts tasks with the new file. For databases, rotate in two phases (add
new credential to the DB, roll services, then remove the old credential). In stacks, bump the
secret's `name:` (e.g. with a content hash) so `stack deploy` creates and swaps it.

## Templated configs/secrets
```sh
docker config create --template-driver golang app_conf_v1 app.conf.tmpl
```
```
# app.conf.tmpl
service={{ .Service.Name }} task={{ .Task.Slot }} node={{ .Node.Hostname }}
db_password={{ secret "db_password" }}
log_level={{ env "LOG_LEVEL" }}
```
Stack: `configs: { app_conf: { file: ./app.conf.tmpl, template_driver: golang } }`. The
service must also have the referenced secret attached; `secret` looks it up by its target file name.

## Verify
`docker exec $(docker ps -q -f name=shop_api) ls -ln /run/secrets` shows owner 10001 and mode 0400;
`docker service inspect shop_api -f '{{json .Spec.TaskTemplate.ContainerSpec.Secrets}}'`.

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master), the docker/cli stack schema v3.13 and moby/swarmkit `template/` source. Confirmed: secrets stored in the encrypted Raft log and mounted in an in-memory filesystem at `/run/secrets/<name>` (Linux); configs not encrypted at rest, default mount `/<config-name>`; `docker service update --secret-rm/--secret-add`; removing a secret in use fails; stack `uid`, `gid`, `mode`, `external`, `file`, `name`, `template_driver`; template functions `env`, `secret` and fields `.Service.Name`, `.Task.Slot`, `.Node.Hostname`.
Method: documentation only; no commands were run.
