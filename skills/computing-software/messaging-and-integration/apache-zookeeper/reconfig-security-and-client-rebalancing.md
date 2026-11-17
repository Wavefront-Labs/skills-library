---
id: computing-software.messaging-and-integration.apache-zookeeper.reconfig-security-and-client-rebalancing
name: reconfig-security-and-client-rebalancing
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, reconfig-security, zookeeper-config, skipacl, client-rebalancing, updateserverlist]
level: sme
status: docs-checked
description: "Who may reconfigure ZooKeeper (/zookeeper/config ACL, superuser, skipACL) and how clients follow membership changes with a watch, getConfig and updateServerList."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperReconfig.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reconfig security and client rebalancing

Security:
- Before 3.5.3 there was no enforced security over reconfig: any client able to connect could change the cluster, for example add a compromised server or remove legitimate ones.
- From 3.5.3 reconfig is disabled by default (`reconfigEnabled`), and using it needs ACL setup and authentication. The reconfig Java APIs moved into the `ZooKeeperAdmin` class.
- The dynamic configuration lives in `/zookeeper/config` (`ZooDefs.CONFIG_NODE`). It is read-only for all users except the super user and users explicitly granted write access. By default only the super user has full control including write; the super user can grant others write through an ACL.
- The ensemble must enable authentication so clients can be authenticated.
- `skipACL=yes` skips the ACL check completely, so any unauthenticated user can reconfigure. The page offers it for users in a secured environment (for example behind a company firewall) and leaves the decision to the user.

Rebalancing clients:
- All clients must watch `/zookeeper/config`, directly or via `getConfig`.
- When the watch fires, read the new configuration with `sync` then `getConfig`; if it is really new, call `updateServerList`.
- To avoid mass migration, have each client sleep a short random period before `updateServerList`.
- The method keeps the expected number of connections per server equal after membership changes (paper sections 4 and 5.1). Examples: StaticHostProviderTest.java and TestReconfig.cc.

Upgrading to 3.5.0 in a rolling fashion requires going through 3.4.6 first; a full shutdown does not.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Dynamic Reconfiguration page (Security and Rebalancing Client Connections sections). Removed: the claim to add client ports to every server line before upgrading, and the "Verify" line (neither is stated on the page).
