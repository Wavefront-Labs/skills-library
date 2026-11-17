---
id: computing-software.collaboration-platform-administration.matrix-synapse.workers-redis-and-shared-config
name: workers-redis-and-shared-config
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, workers, redis, replication, instance-map, worker-replication-secret, scaling]
level: advanced
status: docs-checked
description: "Prepare Synapse for workers: Redis, the main-process replication listener, instance_map, worker_replication_secret, and keeping the port private."
sources:
  - https://element-hq.github.io/synapse/latest/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Small instances should stay in the default monolith mode. For larger ones, Synapse can split work into separate Python processes called workers. They share one database, so workers require PostgreSQL; SQLite is for demos only. Processes keep in sync through the Synapse-specific replication protocol, carried over a Redis pub/sub channel, and may also make HTTP requests to each other for operations that need a reply, such as sending an event. With Redis enabled Synapse also uses it as a shared cache.

Setup steps from the docs:

1. Install Redis (for example `apt install redis-server`; an existing deployment is fine) and check it with `echo PING | nc -q1 localhost 6379`, expecting `+PONG`.
2. Install the dependencies with `pip install "matrix-synapse[redis]"`. They are already in `matrix-synapse[all]`, the Debian packages and the Docker images.
3. Put a reverse proxy such as nginx or haproxy in front to direct requests to the right worker or the main process.

Workers normally read a shared config plus their own file. The main process usually needs no file of its own. To adapt the shared file you add an HTTP replication listener on the main process, enable Redis, and define `instance_map` with `main`:

```yaml
listeners:
  - port: 9093
    bind_address: '127.0.0.1'
    type: http
    resources:
     - names: [replication]

worker_replication_secret: ""

redis:
    enabled: true

instance_map:
    main:
        host: 'localhost'
        port: 9093
```

The `host` in `instance_map` is where workers find the main process, not necessarily the bind address. For a Unix socket replication listener, use `path` instead of `port`. Put a random value in `worker_replication_secret` to authenticate worker HTTP traffic.

Never expose the replication listener to the public internet: its traffic is always unencrypted, and unauthenticated unless the secret is set.

## Checked

Method: docs-checked 2026-11-09 against docs/workers.md (Synapse develop branch, raw markdown, read in full).
