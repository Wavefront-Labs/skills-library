---
id: computing-software.devops-ci-cd.release-engineering.config-stores-aws-appconfig-and-consul-kv
name: config-stores-aws-appconfig-and-consul-kv
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, appconfig, consul-kv, configuration-store, aws-appconfig, consul-template, feature-configuration]
level: practitioner
status: draft
description: "Manage runtime configuration in a config store: AWS AppConfig validators and deployment strategies, Consul KV with consul-template, versioning and rollback."
sources:
  - https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html
  - https://developer.hashicorp.com/consul/docs/dynamic-app-config/kv
  - https://github.com/hashicorp/consul-template
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Config stores (AWS AppConfig / Consul)

Put configuration that changes more often than code (limits, toggles, endpoints, tuning) in a store with validation, versioning and gradual rollout. Secrets go in a secrets manager, not here.

## AWS AppConfig
Model: Application > Environment (dev, prod) > Configuration profile (freeform JSON/YAML or feature flags) > Hosted configuration versions > Deployment with a strategy.
```bash
aws appconfig create-hosted-configuration-version --application-id app1 --configuration-profile-id prof1 \
  --content-type application/json --content fileb://config.json version.out
aws appconfig start-deployment --application-id app1 --environment-id prod --configuration-profile-id prof1 \
  --configuration-version 7 --deployment-strategy-id AppConfig.Linear20PercentEvery6Minutes
```
- Validators: JSON Schema or a Lambda run before deployment; invalid config never reaches clients.
- Deployment strategies roll out over time with **bake time**; attach CloudWatch alarms to the environment for automatic rollback.
- Clients fetch with the AppConfig Agent (Lambda extension, ECS/EKS sidecar, or local agent at `localhost:2772/applications/app1/environments/prod/configurations/prof1`) which caches and polls - don't call the data plane API on every request.
- Sources besides hosted: S3, SSM Parameter Store, Secrets Manager.

## Consul KV
```bash
consul kv put config/app/prod/max_connections 200
consul kv get -recurse config/app/prod/
consul kv export config/app/ > backup.json; consul kv import @backup.json
consul kv put -cas -modify-index=1234 config/app/prod/max_connections 250   # check-and-set to avoid lost updates
```
Delivery to apps:
- consul-template renders files and runs a reload command on change:
```hcl
template {
  source      = "/etc/app/app.ctmpl"     # {{ key "config/app/prod/max_connections" }}
  destination = "/etc/app/app.conf"
  command     = "systemctl reload app"
}
```
- `consul watch -type=keyprefix -prefix=config/app/prod/ /usr/local/bin/handler`.
- Native SDKs with blocking queries (`?index=N&wait=5m`).
Protect with ACL policies per prefix (`key_prefix "config/app/prod/" { policy = "read" }`) and keep the KV under Git (git2consul-style sync or Terraform `consul_keys`) for review and history.

## Practices
- Treat config changes like deploys: review, staged rollout, monitoring, rollback path (AppConfig versions; Consul via Git revert).
- Schema-validate config in CI as well as in the store.
- Clients must survive store outages: cache last known good config; start with defaults.

## Verify
- [ ] A bad config version is blocked by validation, and an alarm during rollout triggers automatic rollback.
- [ ] Apps keep running with last-known-good config when the store is unreachable.
