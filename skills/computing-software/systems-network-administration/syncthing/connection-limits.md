---
id: computing-software.systems-network-administration.syncthing.connection-limits
name: connection-limits
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, connection-limits, connectionlimitenough, connectionlimitmax]
level: advanced
status: docs-checked
description: "Cap Syncthing connections with connectionLimitEnough and connectionLimitMax for large server-and-client deployments."
sources: ["https://docs.syncthing.net/advanced/option-connection-limits.html", "https://docs.syncthing.net/users/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection limits

Added in version 1.13.0. The default is `0`, meaning unlimited. The docs say to usually leave these unset: limits are for specific large-deployment scenarios.

## Two limits
- `enough` (`connectionLimitEnough`): once this many connections exist, Syncthing stops trying to connect to other devices. It does not affect incoming connections.
- `max` (`connectionLimitMax`): when reached, Syncthing also refuses incoming connections.

Either can be set individually, leaving the other at zero. When both are set, `enough` should be smaller than `max` or it has no effect (Syncthing also stops connecting outwards once `max` is reached).

## Load balancing scenario
A few equivalent servers are fully connected, and many clients should each use one server. Two options:
- Split clients into static groups pointed at specific servers.
- Configure every client identically for all servers and set the `max` limit to `1`. If a server becomes unavailable, clients migrate to the others.

When establishing new connections Syncthing preferentially connects to devices it was recently connected to, so clients usually stay on the same server over a restart.

```xml
<options>
  <connectionLimitMax>1</connectionLimitMax>
</options>
```

## Checked
2026-11-04. Read the Connection Limits page and the config page entries for `connectionLimitEnough` and `connectionLimitMax`: version 1.13.0, default zero, the two limits, the enough/max relationship, the load-balancing scenario and the restart behaviour. Removed the closing caution, which restated the page's recommendation more strongly than it is worded.
Method: documentation only; no commands were run.
