---
id: computing-software.database-administration.mongodb.connection-storms-and-driver-pool-sizing
name: connection-storms-and-driver-pool-sizing
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, connection-pool-mongodb, maxpoolsize, connection-storm, mongodb-operations, drivers]
level: practitioner
status: docs-checked
description: "Prevent and diagnose MongoDB connection storms: size driver pools (maxPoolSize, minPoolSize, maxConnecting), read connection metrics, and set server limits."
sources:
  - https://www.mongodb.com/docs/manual/administration/connection-pool-overview/
  - https://www.mongodb.com/docs/manual/reference/connection-string-options/
  - https://www.mongodb.com/docs/manual/reference/command/serverStatus/#connections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection storms and driver pool sizing

**Goal:** stop the pattern where latency rises, apps open more connections, each connection costs memory and a thread on mongod, and latency rises further.

## Driver pool settings (connection string)
```
mongodb://app:...@db1,db2,db3/?replicaSet=rs0&maxPoolSize=50&minPoolSize=5&maxConnecting=2&waitQueueTimeoutMS=2000&maxIdleTimeMS=300000
```
- `maxPoolSize`: maximum connections in the pool (default 100; each `MongoClient` manages its own pool). Estimate worst-case server load as client instances × pool size.
- `maxConnecting` (default 2) caps connections a pool establishes concurrently, which damps storms (supported by all drivers except the Rust driver).
- `minPoolSize` (default 0; not supported by all drivers) keeps warm connections; too high multiplies idle connections across many pods.
- Create one `MongoClient` per process and reuse it; per-request clients are the most common storm cause (serverless functions especially).

## Server-side numbers
```javascript
db.serverStatus().connections   // current, available, totalCreated, active
```
- `totalCreated` climbing quickly = churn (clients reconnecting).
- `connections.current` includes clients, replica set members and mongos; compare it with `connections.available` and the ulimit settings.
- `net.maxIncomingConnections` caps incoming connections (on Linux the default and maximum are (RLIMIT_NOFILE / 2) * 0.8 in current releases).

## Sizing rule
Target in-flight operations, not pool size: concurrency ≈ throughput × latency (Little's law). 2000 ops/s at 5 ms needs ~10 concurrent operations, so a pool of 20-50 per process is ample; the manual's tuning page covers lowering `maxPoolSize` when too many connections are opened and raising it when operations wait for a connection.

## Through a proxy
Serverless/large fleets: keep the client global so warm invocations reuse its pool, and cap the number of concurrent instances.

## Diagnose a storm
```javascript
db.currentOp({ "$all": true }).inprog.reduce((m, o) => (m[o.client?.split(":")[0]] = (m[o.client?.split(":")[0]] || 0) + 1, m), {})
```
Counts connections per client IP; find the deployment with the runaway count.

## Verify
After changes, `connections.current` stays flat across deploys and `totalCreated` grows slowly; p99 latency during failover recovers without a connection spike.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: maxPoolSize default 100, minPoolSize default 0 (not supported by all drivers), maxConnecting default 2 (all drivers except Rust), waitQueueTimeoutMS and maxIdleTimeMS options, one MongoClient per application with its own pool, serverStatus connections.current/available/totalCreated/active, net.maxIncomingConnections default on Linux. Removed unconfirmed 1 MB per connection, log message and Data API claims.

Method: documentation only; no commands were run.
