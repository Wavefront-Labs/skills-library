---
id: computing-software.data-engineering.apache-hadoop.yarn-federation-state-store-policies
name: yarn-federation-state-store-policies
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, federation, state-store, zookeeper, sql, policy-manager]
level: sme
status: docs-checked
description: "YARN Federation state store choices (ZooKeeper or SQL), sub-cluster registration keys including yarn.resourcemanager.epoch, and routing policy manager settings."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/Federation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federation state store and policies

On every machine (yarn-site.xml): `yarn.federation.enabled` = true; `yarn.resourcemanager.cluster-id` = unique sub-cluster id (same one used for HA).

State store: ZooKeeper and SQL implementations are supported, and the state-store class must always be overridden with one of them via `yarn.federation.state-store.class`:
- ZooKeeper: `org.apache.hadoop.yarn.server.federation.store.impl.ZookeeperFederationStateStore` with `hadoop.zk.address` (host:port of the ensemble).
- SQL: `org.apache.hadoop.yarn.server.federation.store.impl.SQLFederationStateStore` with `yarn.federation.state-store.sql.url` (example `jdbc:mysql://<host>:<port>/FederationStateStore`), `.sql.jdbc-class` (example `com.mysql.jdbc.jdbc2.optional.MysqlDataSource`), `.sql.username`, `.sql.password`.
- Scripts for MySQL and Microsoft SQL Server are provided. For MySQL download the latest 5.x jar and add it to the CLASSPATH, then run in the database `sbin/FederationStateStore/MySQL/` `FederationStateStoreDatabase.sql`, `FederationStateStoreUser.sql`, `FederationStateStoreTables.sql`, `FederationStateStoreStoredProcs.sql`; matching drop scripts are in the same directory. `FederationStateStoreUser.sql` defines a default user and password, which should be replaced with a strong password. For SQL Server the process is similar, the jdbc driver is already included, and scripts are in `sbin/FederationStateStore/SQLServer/`.

Registration: member RMs heartbeat to the state store to stay alive and publish capability and load; `yarn.federation.state-store.heartbeat-interval-secs` (example 60). On RMs only, `yarn.resourcemanager.epoch` seeds container-ID uniqueness: it must be unique among sub-clusters and well spaced to allow for failures that increment the epoch; increments of 1000 are suggested.

Optional (example values from the page):
- `yarn.federation.failover.enabled` = true: retry considering RM failover within each sub-cluster
- `yarn.federation.blacklist-subclusters`: list of sub-clusters to disable
- `yarn.federation.policy-manager` (example `org.apache.hadoop.yarn.server.federation.policies.manager.WeightedLocalityPolicyManager`) decides how applications and resource requests are routed; `yarn.federation.policy-manager-params` is the binary payload that configures it, typically made by serialising a programmatically configured policy manager or by putting its JSON form in the state store
- `yarn.federation.subcluster-resolver.class` (example `DefaultSubClusterResolverImpl`) with `yarn.federation.machine-list`, a file with one line per node: `node1, subcluster1, rack1`

The Policy Store is logically separate from the State Store though it may share the same physical component. Policies range from random, hashing, round-robin and priority to ones that account for sub-cluster load and request locality.

## Checked
2026-11-08. Read in full: the YARN Federation page (the stable URL served Hadoop 3.3.5, published 2023-03-15). Confirmed: all property names, classes, script names and the epoch guidance. Removed: the verification claim about the first heartbeat interval (not stated), which the page does not support.
Method: documentation only; no commands were run.
