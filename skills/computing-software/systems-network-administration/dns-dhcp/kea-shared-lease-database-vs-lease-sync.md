---
id: computing-software.systems-network-administration.dns-dhcp.kea-shared-lease-database-vs-lease-sync
name: kea-shared-lease-database-vs-lease-sync
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, lease-database-replication, high-availability, mysql, postgresql]
level: practitioner
status: verified
description: "Choose between Kea HA lease synchronisation and a shared replicated lease database, with trade-offs, configs and failure modes for each."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#libdhcp-ha-so-high-availability-outage-resilience-for-kea-servers
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#lease-storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared lease database vs lease sync

## Option 1: HA hook with lease updates (most common)
Each server has its own lease store (memfile or DB); the HA hook sends every lease change to the
partner and syncs the full table after startup or recovery. This is the default
(`send-lease-updates` and `sync-leases` both default to true).
- Pros: no database dependency, simple, works with memfile (fast).
- Cons: two copies; syncing is synchronous (the syncing server does nothing else meanwhile) and
  takes longer with large tables; page size is tuned with `sync-page-limit`.

## Option 2: Database replication, HA without lease updates
The ARM describes this case: MySQL and PostgreSQL have their own replication, which administrators
often already use for redundancy, so the HA hook can rely on it instead of control-channel lease
updates. The servers use databases kept in step by that replication (the ARM does not name a
product or topology; Galera or PostgreSQL streaming replication are examples you would have to
validate). The HA hook still handles state and scope ownership, but:
```json
"high-availability": [{ ..., "send-lease-updates": false, "sync-leases": false }]
```
The ARM says that in the usual case both parameters are set to the same value: both false when
database replication is in use, both true otherwise. Mixed settings are for special cases (for
example syncing by copying a lease file) that Kea does not support natively.
- Pros: no HA lease traffic or startup sync; IPAM/reporting can read the database.
- Cons (reasoning, not from the ARM): the database becomes a dependency and its latency adds to every
  DHCP transaction, and a replication split-brain could allow duplicate allocations.

## Option 3: Shared lease database without HA hook
Several kea-dhcp4 instances can use one lease store; the ARM mentions that case only for
`offer-lifetime`: with it set (default 0, off), a lease is allocated and persisted at DHCPOFFER, so a
server that loses the race for an address stays silent on DHCPDISCOVER instead of NAKing at
DHCPREQUEST, and the client simply retries. With separate pools per server the servers do not
contend. The ARM does not present this as an HA design; without the HA hook nothing coordinates
which server answers, so treat it as an unsupported design and test failure behaviour.

## Choosing
| Need | Pick |
|------|------|
| Branch / simple pair | HA lease updates + memfile |
| Very large deployments, central reporting | HA lease updates with a database per server, or database replication with both HA flags false |
| Strict RPO on leases across sites | replicated database with synchronous replication (a database-side property; Kea docs do not cover it) |

## Gotchas
- With `send-lease-updates: false` and separate, unreplicated databases the partners diverge: never
  combine them.
- Database schema upgrades (`kea-admin db-upgrade`) must happen before starting new Kea versions
  (kea-admin man page: `db-init`, `db-version`, `db-upgrade`).

## Verify
- [ ] Killing one server (or the DB primary in option 2) leaves clients able to obtain and renew leases with no duplicate addresses.
