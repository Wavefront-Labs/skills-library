---
id: computing-software.messaging-and-integration.apache-zookeeper.use-cases-service-discovery-and-config
name: use-cases-service-discovery-and-config
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, use-cases, service-discovery, configuration-management, sharding, locking]
level: intro
status: docs-checked
description: "ZooKeeper in production at companies and free projects: service discovery, dynamic configuration, sharding, leader election and locking examples."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperUseCases.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service discovery and configuration use cases

- Pinterest: service discovery and dynamic configuration so clients see only active hosts.
- Box: service discovery and coordination. Twitter: service registry, cluster topology metadata, EventBus leader election.
- Wealthfront: discovery, election and locking in deployment infrastructure.
- Yahoo!, Zynga, TubeMogul: configuration, election, sharding, locking, group membership.
- Facebook: Zeus configuration system, a scaled and forked ZooKeeper with cross-region consensus.
- spring-cloud-zookeeper: discovery and distributed configuration for Spring Boot.
- Neo4j HA: write-master election; Katta: node, master and index management.
- Dubbo: service registration, discovery and configuration.

Verify: for a candidate system, name which role ZooKeeper plays (discovery, configuration, election, sharding or locking), as in the examples above.

## Checked

Method: docs-checked 2026-11-09 against zookeeperUseCases.html (full page read)
