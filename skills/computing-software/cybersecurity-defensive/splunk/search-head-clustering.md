---
id: computing-software.cybersecurity-defensive.splunk.search-head-clustering
name: search-head-clustering
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-architecture, search-head-clustering, shc, deployer, captain, kvstore-replication, shcluster-bundle, knowledge-object-replication]
level: advanced
status: draft
description: "Deploy and maintain a Splunk search head cluster: deployer bundles, captain election, KV store health, member add/remove and the classic replication traps."
sources: ["Splunk Docs - Distributed Search manual (Deploy and configure search head clustering)", "Splunk Docs - Use the deployer to distribute apps", "Splunk Validated Architectures"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Splunk search head clustering (SHC)

**Goal:** a highly available search tier where scheduled searches, knowledge objects and
KV store data survive a member failure, with apps deployed consistently.

## Topology
- Minimum 3 members (captain election needs a majority), plus one **deployer** that is
  NOT a member. Put a load balancer with sticky sessions in front for users.
- Members of a cluster must run the same Splunk version on similar hardware.

## Build
On each member:
```
splunk init shcluster-config -auth admin:<pw> -mgmt_uri https://sh1.example.internal:8089 \
  -replication_port 9777 -replication_factor 3 -conf_deploy_fetch_url https://deployer.example.internal:8089 \
  -secret <shc_secret> -shcluster_label prod_shc
splunk restart
```
Then on one member: `splunk bootstrap shcluster-captain -servers_list "https://sh1:8089,https://sh2:8089,https://sh3:8089"`.
Attach to an indexer cluster with `splunk edit cluster-config -mode searchhead -manager_uri ...`.

## Deploying apps
Put apps in `$SPLUNK_HOME/etc/shcluster/apps/` on the deployer and run:
```
splunk apply shcluster-bundle -target https://sh1.example.internal:8089 -auth admin:<pw>
```
- Default `deployer_push_mode = merge_to_default` merges local into default. Changes users
  make in the UI live in the members' `local` directories and replicate between members, not via the deployer.
- Never install apps directly on a member: it is not replicated.

## Operations
- Status: `splunk show shcluster-status --verbose` (captain, members, `out_of_sync_node`).
- KV store: `splunk show kvstore-status`; all members should report `ready`.
- Remove a member: `splunk remove shcluster-member` from that member, then stop it.
- Rolling restart: `splunk rolling-restart shcluster-members -searchable true`.
- Out-of-sync member (replication log gap): `splunk resync shcluster-replicated-config` on
  that member; KV store out of sync: `splunk resync kvstore`.

## Gotchas
- Scheduled searches run once per cluster on a member the captain chooses; letting the
  captain also run ad-hoc and scheduled load (`captain_is_adhoc_searchhead = false` default) is fine, but watch its CPU.
- Static captain is for disaster recovery only; return to dynamic election afterwards.
- Lookups larger than the replication size limits stop replicating silently; use KV store or
  shrink them.
- Losing majority (2 of 3 down) means no captain and no scheduled searches.

## Verify
- [ ] shcluster-status shows one captain and all members `Up`, none out of sync.
- [ ] KV store `ready` on every member.
- [ ] An app pushed from the deployer appears on all members after one bundle push.
