---
id: computing-software.search-and-information-retrieval.apache-solr.zookeeper-ensemble-setup
name: zookeeper-ensemble-setup
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [zookeeper, zookeeper-ensemble, quorum, zoo-cfg, zk-host]
level: advanced
status: docs-checked
description: "Set up an external ZooKeeper ensemble for SolrCloud: odd node counts and quorum, zoo.cfg tickTime, dataDir, initLimit, syncLimit, autopurge, 4lw whitelist, and chroot."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/zookeeper-ensemble.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zookeeper-ensemble-setup

Quorum is a majority of non-failing servers. Use an odd number: with three nodes one can fail and 66% remain, so ZooKeeper keeps serving while you repair it.

Create `<ZOOKEEPER_HOME>/conf/zoo.cfg`. Settings in the guide:
- `tickTime=2000` (ms per tick)
- `dataDir=/var/lib/zookeeper`
- `4lw.commands.whitelist=mntr,conf,ruok` (enables the Solr Admin UI ZooKeeper view; `*` enables all four-letter words)
- `initLimit=5`, `syncLimit=2`
- `autopurge.snapRetainCount=3`, `autopurge.purgeInterval=1`
- one `server.N=host:port:port` line per member, with a `myid` file in each `dataDir` holding that member's number.

Point Solr at the ensemble with `-z host1:2181,host2:2181,host3:2181`, optionally followed by a chroot such as `/solr`. Create the chroot with `bin/solr zk mkroot /solr -z <zkHost>` before first start.

Set `ZK_HOST` in `solr.in.sh` so every node gets the same value.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide ZooKeeper Ensemble Configuration page: quorum and the odd-number rule with the 66% example, the `zoo.cfg` values (`tickTime`, `dataDir`, `4lw.commands.whitelist`, `initLimit`, `syncLimit`, `autopurge.*`), `myid` files, `-z` with a chroot, `bin/solr zk mkroot`, and `ZK_HOST` in `solr.in.sh`. Nothing removed.

Method: documentation only; no commands were run.
