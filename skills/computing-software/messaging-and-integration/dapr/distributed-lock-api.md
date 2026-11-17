---
id: computing-software.messaging-and-integration.dapr.distributed-lock-api
name: distributed-lock-api
category: computing-software
field: messaging-and-integration
product: dapr
tags: [lock, distributed-lock, lease, redis, alpha, mutual-exclusion, resourceid, lockowner]
level: practitioner
status: docs-checked
description: "Use the alpha Dapr distributed lock API: a lock.redis component, then lock and unlock calls with resourceId, lockOwner and expiryInSeconds; leases free stuck locks."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/distributed-lock/distributed-lock-api-overview.md
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/distributed-lock/howto-use-distributed-lock.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Locks give mutually exclusive access to a shared resource that gets updated, for example a database row or a queue read by competing consumers. Each lock has a name chosen by the application; at any moment one instance holds it, and locks are scoped to a Dapr app ID. The API is in Alpha state.

Deadlock protection comes from leases: if the holder crashes without unlocking, the lock is released automatically when the lease expires. It is also released explicitly with the unlock API.

Component (Redis):

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: lockstore
spec:
  type: lock.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: <PASSWORD>
```

Acquire a lock on a resource:

```bash
curl -X POST http://localhost:3500/v1.0-alpha1/lock/lockstore
   -H 'Content-Type: application/json'
   -d '{"resourceId":"my_file_name", "lockOwner":"random_id_abc123", "expiryInSeconds": 60}'
```

The SDK examples expose a success flag on the result (.NET `fileLock.Success`, Go `resp.Success`). Release it:

```bash
curl -X POST http://localhost:3500/v1.0-alpha1/unlock/lockstore
   -H 'Content-Type: application/json'
   -d '{"resourceId":"my_file_name", "lockOwner":"random_id_abc123"}'
```

The page's examples use a random `lockOwner` value. Its third diagram shows instances of different applications acquiring different locks on the same resource.

## Checked

2026-11-08. Alpha status, named locks scoped to an app ID, lease-based release, the lock.redis component, and the lock and unlock calls confirmed on both distributed lock pages. Changed: removed advice about denied instances and unique lockOwner values, and an inferred reason for cross-app locks, none of which the pages state.

Method: documentation only; every cited page read in full; no commands were run.
