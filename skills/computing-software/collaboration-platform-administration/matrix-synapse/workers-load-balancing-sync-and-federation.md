---
id: computing-software.collaboration-platform-administration.matrix-synapse.workers-load-balancing-sync-and-federation
name: workers-load-balancing-sync-and-federation
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, workers, load-balancing, nginx, sync, initial-sync, federation, hash, access-token]
level: advanced
status: docs-checked
description: "Load balance Synapse workers: hash /sync by user from the access token, isolate initial sync, balance inbound federation by source IP, and split event sending by room ID in nginx."
sources:
  - https://element-hq.github.io/synapse/latest/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Multiple generic workers can run behind a reverse proxy, but different endpoints need different balancing.

**Sync.** `/sync` and `/initialSync` are more efficient when all requests from one user hit the same instance, which the proxy can do by extracting the username from the access token (tokens look like `syt_<username>_...`). Separately, requests without a `since` parameter, plus `/initialSync`, are initial syncs that happen when a user logs in on a new device. They can be very resource intensive, so isolating them keeps ongoing syncs unaffected. The docs' nginx example (which they note probably needs changes for your setup) selects the upstream with `map $arg_since $sync`, and builds a hash key from the bearer token with maps such as:

```nginx
map $arg_since $sync {
    default synapse_sync;
    '' synapse_initial_sync;
}
```

Each upstream then uses `hash $mxid_localpart consistent;` over its server list, and the `location` blocks for `/sync`, `/events` and `initialSync` pass to `http://$sync` or the matching upstream.

**Other traffic.**

- Federation and client requests can use simple round robin.
- Inbound federation transactions (`^/_matrix/federation/v1/send/`) should be balanced by source IP, so transactions from one remote server go to the same process.
- Registration and login can be handled by their own workers so unexpected load does not affect new logins and sign ups.
- Event sending can be balanced by the room ID (the path component after `/rooms/`), by the full URI, or round robin. If a large bridge sends many events, give it a dedicated set of workers to limit the effect of bursts on normal users.

Pagination is the exception noted elsewhere: keep every `/messages` request for a room on one instance. See the generic worker routing skill for the endpoint lists.

## Checked

Method: docs-checked 2026-11-09 against docs/workers.md (Synapse develop branch, raw markdown, read in full).
