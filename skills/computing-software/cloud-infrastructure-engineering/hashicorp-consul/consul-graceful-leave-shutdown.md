---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-graceful-leave-shutdown
name: consul-graceful-leave-shutdown
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, graceful-leave, consul-leave, leave-on-terminate]
level: practitioner
status: docs-checked
description: "Stop Consul agents with consul leave versus signals, set leave_on_terminate and skip_leave_on_interrupt deliberately, and protect server quorum."
sources: ["https://developer.hashicorp.com/consul/commands/leave", "https://developer.hashicorp.com/consul/commands/force-leave", "https://developer.hashicorp.com/consul/docs/reference/agent/configuration-file/general"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A graceful leave makes other nodes see the agent as `left` rather than `failed`. For a server, it is removed from the Raft peer set gracefully, which changes the quorum size.

```sh
consul leave        # graceful leave and shutdown of the local agent (ACL agent:write)
```

```hcl
leave_on_terminate      = false   # SIGTERM does not leave
skip_leave_on_interrupt = true    # Ctrl-C does not leave
```

Defaults depend on agent mode:
- `leave_on_terminate`: `true` on clients, `false` on servers. When true, a TERM signal sends a Leave message and gracefully leaves.
- `skip_leave_on_interrupt`: `false` on clients, `true` on servers. On a server, Ctrl-C keeps the server in the cluster and therefore in quorum; on a client it gracefully leaves.

Gotchas:
- Running `consul leave` on a server reduces the quorum size even if the cluster was started with `bootstrap_expect`. You can end up with one server able to commit writes whose data is lost if it fails before more servers are added.
- A node that left gracefully does not try to rejoin when it restarts with a snapshot.
- If an agent died or shut down without leaving, use `consul force-leave <node>` to move it from `failed` to `left` (see `consul-raft-remove-peer`).

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: commands/leave, commands/force-leave, reference/agent/configuration-file/general (`leave_on_terminate`, `skip_leave_on_interrupt` and their client/server defaults). Fixed: the old text said clients and servers behave differently on SIGTERM but did not cover interrupt defaults, and told readers to "confirm defaults"; the defaults are now stated. Removed: the "two servers leave at once" example and the Verify step.
Method: documentation only; no commands were run.
