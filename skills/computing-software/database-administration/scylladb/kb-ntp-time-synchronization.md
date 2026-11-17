---
id: computing-software.database-administration.scylladb.kb-ntp-time-synchronization
name: kb-ntp-time-synchronization
category: computing-software
field: database-administration
product: scylladb
tags: [ntp, clock-sync, timestamps, time-synchronization, write-ordering]
level: practitioner
status: docs-checked
description: "Time synchronization for ScyllaDB: write timestamps order data, NTP pool pitfalls, use your own data center NTP servers in ntp.conf, same config for app servers."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/ntp.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NTP and time synchronization

ScyllaDB (like Cassandra) orders writes with wall-clock timestamps from the server or optionally the client. Quorum read-after-write guarantees depend on those timestamps, so nodes must keep their clocks in agreement.

The default NTP configuration that ships with Linux uses public pools (`0.debian.pool.ntp.org`, `0.fedora.pool.ntp.org`) via DNS round robin. Each node then talks to different random servers, so two nodes can drift apart: in a 10-node cluster, half the time some pair differs by more than 10.9 ms, and it gets worse as nodes are added.

Fix: replace the pool lines in `ntp.conf` with your own data center NTP servers, and deploy that same file to all servers, including application servers (keeping app and database clocks aligned also simplifies matching logs):

```
driftfile /var/lib/ntp/drift
restrict default nomodify notrap nopeer noquery
restrict 127.0.0.1
restrict ::1
restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap
server 0.ntp.example.com iburst
server 1.ntp.example.com iburst
server 2.ntp.example.com iburst
```
Being in sync with each other matters more than matching some random machine on the Internet. Dedicated NTP appliances suit large sites; any standard Linux host can act as an NTP server. If you have no known good time source, the upstream pool lines can be used on the NTP servers only.

## Checked

2026-11-04: timestamp ordering, the pool pitfall and 10.9 ms figure, the ntp.conf example and deployment advice confirmed against the ScyllaDB NTP knowledge-base page. Removed the unsupported ntpq and chronyc advice.

Method: documentation only; no commands were run.
