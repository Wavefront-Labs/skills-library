---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-lock-semaphore
name: consul-lock-semaphore
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, consul-lock, distributed-lock, semaphore]
level: practitioner
status: docs-checked
description: "Use consul lock to run a child command only while holding a KV lock or semaphore, and handle session lifetime and shutdown behaviour."
sources: ["https://developer.hashicorp.com/consul/commands/lock"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`consul lock [options] prefix child...` acquires a lock under a KV prefix (which must be writable) and runs the child only while the lock is held, setting `CONSUL_LOCK_HELD=true` in its environment. With `-n` above 1 it becomes a semaphore, which the docs say is less efficient than a simple lock.

```sh
consul lock -n 1 locks/nightly-job /usr/local/bin/nightly-job.sh
consul lock -n 3 locks/workers /usr/local/bin/worker.sh   # semaphore with 3 holders
consul lock -timeout=30s locks/nightly-job /usr/local/bin/nightly-job.sh   # give up acquiring after 30s
```

If the lock is lost, communication is disrupted or the parent is interrupted, the child receives `SIGTERM`, then `SIGKILL` after a 5 second grace period. On Windows the child is always killed with `SIGKILL`.

Other options: `-name` (session name), `-shell` (default true), `-pass-stdin`, `-child-exit-code` (exit 2 if the child failed), `-monitor-retry` (default 3 retries with 1s wait on a 500 while monitoring), `-verbose`.

Gotchas:
- All locks on a prefix must use the same `-n`, otherwise an error is returned.
- The ephemeral session `consul lock` creates attaches node checks such as `serfHealth`, so the lock is not lost while the local agent is healthy; sessions run indefinitely while the node stays healthy. To enforce a TTL, create your own session through the HTTP API without node checks, acquire the KV key with `?acquire=<sessionID>`, and renew it yourself.
- To lock in a remote WAN-federated datacenter, run with `-datacenter=<name>` on a server agent; client agents cannot do this.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source (commands/lock): all flags, `CONSUL_LOCK_HELD`, signals and 5 second grace, Windows behaviour, `-n` agreement, session and `serfHealth` behaviour, `-datacenter` on servers. Removed: the `-try` flag in the Verify step (not an option on the page; `-timeout` is), and the advice to wrap the child in `timeout`, which the page does not give.
Method: documentation only; no commands were run.
