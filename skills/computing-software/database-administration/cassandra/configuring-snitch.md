---
id: computing-software.database-administration.cassandra.configuring-snitch
name: configuring-snitch
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, endpoint-snitch, cassandra-rackdc-properties, ec2-snitch, snitch, gossipingpropertyfilesnitch, rack-awareness, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "GossipingPropertyFileSnitch and cloud snitches"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/snitch.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/configuration/cass_rackdc_file.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a snitch

Goal: configure rack/DC topology.
- `GossipingPropertyFileSnitch` is the production recommendation and the default; it reads the local node's `dc` and `rack` (defaults DC1 and RAC1, case-sensitive) from `cassandra-rackdc.properties` and spreads them by gossip.
- Other snitches: `SimpleSnitch` (single DC only), `PropertyFileSnitch` (`cassandra-topology.properties`), `Ec2Snitch` (region = datacenter, availability zone = rack), `Ec2MultiRegionSnitch`, `RackInferringSnitch`.
- The snitch groups machines into datacenters and racks so replicas avoid the same rack.
- `dynamic_snitch` routes reads away from slow hosts.
Verify: `nodetool status` lists the intended datacenters and racks.

## Checked

2026-11-02. Checked against Snitch and cassandra-rackdc.properties (snitch classes, GossipingPropertyFileSnitch recommendation and default, dc and rack defaults, EC2 mapping, dynamic snitch). Removed: the 'topology change moves replicas, rolling restart plus repair' and 'RF <= racks' advice (not stated).

Method: documentation only; no commands were run.
