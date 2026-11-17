---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.external-configuration-store
name: external-configuration-store
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, design-patterns-cloud, external-configuration-store, centralised-configuration, aws-appconfig, parameter-store, azure-app-configuration, feature-flags, dynamic-configuration, config-validation]
level: practitioner
status: docs-checked
description: "Move runtime config out of deploy packages into a managed store: what belongs there, caching and refresh, validation, staged rollout, fallback when it's down."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/external-configuration-store", "https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html", "https://learn.microsoft.com/azure/azure-app-configuration/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External configuration store

## What goes where
- Keep routine settings (feature flags, endpoints) in the configuration store; keep secrets (connection strings,
  API keys, certificates, passwords) in a dedicated secret-management system with encryption and controlled access.
- Settings shared by many services, or changed at runtime, suit the store.

Examples: AWS AppConfig (validators, deployment strategies, CloudWatch-alarm automatic rollback; it can deploy from its
hosted store, Secrets Manager, Parameter Store or S3), Azure App Configuration (labels, feature-flag management,
complements Key Vault).

## Steps
1. **Validate before deploy**: AppConfig validators check that data is syntactically and semantically correct.
2. **Roll out config like code**: use a deployment strategy to change gradually over a defined period, monitor
   alarms, and roll back automatically on alarm.
3. Client: cache configuration and use an expiration policy so it refreshes periodically; a change notification
   mechanism can also tell the app to reload.
4. Turn on audit logging for who reads or changes values, and apply the same audit requirements to local fallback
   copies. Version configuration values.

## Gotchas
- Caching covers transient outages, but typically not a store that is down at application start. Have the deployment
  pipeline supply the last known set of values in a file to use when live values cannot be fetched at startup.

## Verify
- [ ] Invalid config is rejected before it reaches any instance.
- [ ] Block access to the store: running and newly started instances still work on last-known-good.

## Checked
2026-11-01. Confirmed in the Azure Architecture Center External Configuration Store pattern (secrets vs settings,
cache expiry, last known values at startup, audit logging, versioning), the AWS AppConfig overview (validators,
deployment strategies, alarm rollback, supported sources) and the Azure App Configuration overview (labels,
feature flags, Key Vault). Removed: table of homes per setting, SSM/Consul/Spring/ConfigMap comparison, JSON Schema
step, 30-60 s polling, pod/TPS quota example, rollback-time target.
Method: documentation only; no commands were run.
