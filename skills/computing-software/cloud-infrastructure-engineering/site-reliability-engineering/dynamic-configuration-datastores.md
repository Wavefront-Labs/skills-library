---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.dynamic-configuration-datastores
name: dynamic-configuration-datastores
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [configuration-datastore, dynamic-config-store, configuration-design, feature-flags, etcd, consul-kv, aws-appconfig]
level: advanced
status: docs-checked
description: "Run a dynamic config datastore safely: when to use one vs files, staged value rollout, validation, versioning and rollback, client caching when the store is down."
sources: ["https://sre.google/workbook/configuration-specifics/", "https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html", "https://developer.hashicorp.com/consul/docs/dynamic-app-config/kv"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration datastores

Some configuration is better read at runtime from a datastore than baked into a deployment: AWS AppConfig
lists feature flags, allow and block lists, logging levels, service limits and throttling rules as values that
change often and cause issues if misconfigured. That brings availability and consistency concerns into the
configuration path. The SRE Workbook (Configuration Specifics) advises keeping config history, with who
changed it, and making rollback easy; source control gives that plus code review.

## Files vs datastore
| Files in the deploy (GitOps) | Datastore (Consul KV, AWS AppConfig, etc.) |
|---|---|
| change = deploy; reviewed, versioned, canaried | change without a deploy |
| fine for most config | flags, limits, throttling rules |
| no runtime dependency | runtime dependency on the store |

## Safety requirements for a config store
1. **Source of truth in version control** where possible; the store is a distribution mechanism, synced
   from Git by CI (keeps review and history).
2. **Validation before publish** (see `semantic-configuration-validation`).
3. **Staged rollout of values**: AWS AppConfig deployment strategies roll changes out gradually over a
   defined time, and CloudWatch alarms can trigger automatic rollback:
```bash
aws appconfig start-deployment --application-id <APP_ID> --environment-id <ENV_ID> \
  --configuration-profile-id <PROFILE_ID> --configuration-version <VERSION> \
  --deployment-strategy-id <STRATEGY_ID>
```
4. **Versioning and instant rollback** to the previous value.
5. **Client behaviour when the store is unavailable**: cache last-known-good locally (disk), start with
   it, keep serving. Never block startup or requests on the store.
6. **Avoid polling spikes**: spread client refreshes so they do not hit the store together.

## Client pattern
```python
cfg = load_cached("/var/cache/app/config.json")       # last known good
def on_update(new):
    if validate(new):
        atomic_write("/var/cache/app/config.json", new); swap_in_memory(new)
    else:
        log.error("rejected invalid config version %s", new.version)
watch(store, key="/apps/checkout/config", callback=on_update)
```

## Gotchas
- Global instant config changes are a classic outage trigger (see `change-and-process-induced-emergencies`).
- Expose the active config version as a metric/label so you can see which instances run which version.
- Too many tiny flags without owners become unmanageable; expire flags.

## Verify
- [ ] Store outage test: services keep running on cached config and restart successfully.
- [ ] Bad value rollout stops automatically on alarm and rolls back.

## Checked
2026-11-01. The `aws appconfig start-deployment` command was checked against the botocore model. Confirmed in the AWS AppConfig introduction (examples of dynamic config, deployment strategies, CloudWatch alarm rollback, agent caching), the Consul KV page (config parameters, replication) and the SRE Workbook Configuration Specifics chapter (history and easy rollback via source control). Removed: the named predefined strategy, etcd, ZooKeeper and flag-service claims, the watch advice and the attribution of the datastore idea to the Workbook.
Method: documentation only; no commands were run.
