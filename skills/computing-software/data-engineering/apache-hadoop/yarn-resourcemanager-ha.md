---
id: computing-software.data-engineering.apache-hadoop.yarn-resourcemanager-ha
name: yarn-resourcemanager-ha
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, resourcemanager, high-availability, failover, zookeeper]
level: advanced
status: docs-checked
description: "YARN ResourceManager HA: the minimal yarn-site keys, embedded automatic failover, client failover proxy, rmadmin state commands, and the /isActive health probe."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/ResourceManagerHA.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ResourceManager HA

An Active/Standby setup: one RM is active and one or more standbys wait to take over. The transition to active is triggered by the admin CLI or, with automatic failover, the integrated failover controller.

Minimal config (the page's sample):
- `yarn.resourcemanager.ha.enabled` = true
- `yarn.resourcemanager.cluster-id`: lets the elector ensure an RM does not take over as Active for another cluster
- `yarn.resourcemanager.ha.rm-ids`: e.g. `rm1,rm2`
- `yarn.resourcemanager.hostname.<rm-id>` (or each service address)
- `yarn.resourcemanager.webapp.address.<rm-id>` (not needed with `yarn.http.policy` HTTPS_ONLY; with HTTP_ONLY the https variant is not needed)
- `yarn.resourcemanager.zk-address`: ZooKeeper quorum, used for both the state store and embedded leader election

Automatic failover (`yarn.resourcemanager.ha.automatic-failover.enabled`) and the embedded elector (`...automatic-failover.embedded`) are by default enabled only when HA is enabled. The embedded ZooKeeper ActiveStandbyElector acts as failure detector and leader elector, so no separate ZKFC daemon is needed (unlike HDFS).

Clients, ApplicationMasters and NodeManagers list all RMs in yarn-site.xml and try them round-robin until they reach the Active; the default is `ConfiguredRMFailoverProxyProvider`, overridable with `yarn.client.failover-proxy-provider` (non-HA mode uses `yarn.client.failover-no-ha-proxy-provider`). Retry tuning: `yarn.client.failover-max-attempts`, `failover-sleep-base-ms`, `failover-sleep-max-ms`, `failover-retries`, `failover-retries-on-socket-timeouts`.

Admin:

```
yarn rmadmin -getServiceState rm1        # prints active or standby
yarn rmadmin -transitionToStandby rm1    # refused with automatic failover unless --forcemanual
```

The page warns that forcing manual transitions risks split-brain or incorrect state.

Standby RMs redirect web UI requests (except the About page) and REST web service calls to the Active. Behind a load balancer use `http://RM_HOSTNAME/isActive` as a health probe: 200 if the RM is Active, 405 otherwise.

State recovery needs ResourceManager Restart enabled; the state store must be visible to both RMs. FileSystemRMStateStore and ZKRMStateStore exist; ZKRMStateStore is recommended because it permits writes from only one RM at a time, so no separate fencing is needed. With it, the page advises not setting `zookeeper.DigestAuthenticationProvider.superDigest`.

## Checked

Method: 2026-11-08 compared against the ResourceManager HA page (apache/hadoop trunk markdown, read in full). The draft's `hadoop.zk.address` is corrected to `yarn.resourcemanager.zk-address` as the page lists; the state-store, fencing and forcemanual details added and the invented "Verify" step removed.
