---
id: computing-software.messaging-and-integration.apache-zookeeper.connection-and-request-throttling
name: connection-and-request-throttling
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, throttling, connectionmaxtokens, requestthrottlelimit, globaloutstandinglimit, largerequestthreshold]
level: advanced
status: docs-checked
description: "ZooKeeper overload protection: connection token bucket, request throttle, globalOutstandingLimit, large request limits and multiRead caps with defaults."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Throttling settings (defaults)

Connection token bucket (all new in 3.6.0):
- `connectionMaxTokens` (`zookeeper.connection_throttle_tokens`): bucket size; 0 disables throttling (default 0).
- `connectionTokenFillTime` (ms between refills) default 1; `connectionTokenFillCount` (tokens added per refill) default 1.
- `connectionFreezeTime`: interval in ms at which the drop probability is adjusted; -1 disables probabilistic dropping (default -1).
- `connectionDropIncrease` 0.02 (probability added when the bucket is empty); `connectionDropDecrease` 0.002; `connectionDecreaseRatio` 0 (the decrease threshold is `connectionMaxTokens * connectionDecreaseRatio`).

Requests:
- `globalOutstandingLimit` (`zookeeper.globalOutstandingLimit`): default 1,000 outstanding requests across the whole ensemble, divided between members.
- `requestThrottleLimit` (`zookeeper.request_throttle_max_requests`, 3.6.0): outstanding requests allowed before the RequestThrottler stalls; 0 disables (default 0). `requestThrottleStallTime` default 100 ms.
- `requestThrottleDropStale` default true: drop stale requests (from a closed connection, or with latency above the session timeout). `requestStaleConnectionCheck` default true; `requestStaleLatencyCheck` default false.
- `largeRequestMaxBytes` default 100 * 1024 * 1024 (the connection closes if a large request would exceed it); `largeRequestThreshold` default -1, which turns large request throttling off.
- `multiRead.maxOps` (3.9.7) default 1000 and `multiRead.maxResponseBytes` (3.9.7) default 67108864 (64 MB); 0 or negative disables each; an over-limit multiRead is rejected with BadArguments.
- `maxConcurrentSnapSyncs` default 10 and `maxConcurrentDiffSyncs` default 100: syncs a leader or follower serves at once.
- `throttledOpWaitTime` (`zookeeper.throttled_op_wait_time`): time in the RequestThrottler queue after which a request is marked throttled and answered with error ZTHROTTLEDOP; 0 means no throttling (default 0).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Administrator's Guide (Advanced Configuration throttling options). Removed: the "Verify" step about metrics or logs under synthetic load (not documented).
