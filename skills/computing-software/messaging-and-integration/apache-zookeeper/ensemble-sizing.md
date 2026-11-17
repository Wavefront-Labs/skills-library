---
id: computing-software.messaging-and-integration.apache-zookeeper.ensemble-sizing
name: ensemble-sizing
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, ensemble, quorum, fault-tolerance, deployment, odd-servers]
level: practitioner
status: docs-checked
description: "Choose a ZooKeeper ensemble size: at least three servers on separate machines, odd counts, failures tolerated per size, and failure-domain placement."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
  - https://zookeeper.apache.org/doc/current/zookeeperStarted.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ensemble sizing

- Production needs at least three servers, each on its own machine; an odd number is recommended.
- The service stays up while a majority of servers is up.
- Tolerated failures: 3 servers tolerate 1; 5 tolerate 2; 6 still tolerate only 2 (an extra server to maintain for no gain).
- Five servers let you take one down for maintenance and still survive one unexpected failure.
- Two servers are worse than one in practice: one failure leaves no majority, and you have two single points of failure.
- Place members so one switch, power circuit or cooling failure cannot remove a majority.
- Running several servers on one machine (localhost with unique ports) is for testing only and gives no redundancy.

Verify: with N servers, shutting down floor((N-1)/2) of them still leaves the ensemble serving requests.

## Checked

Method: docs-checked 2026-11-09 against zookeeperAdmin.html (System Requirements and Cross Machine Requirements sections) and zookeeperStarted.html (full page read)
