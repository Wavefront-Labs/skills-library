---
id: computing-software.systems-network-administration.headscale.migrate-ip-prefixes
name: migrate-ip-prefixes
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, migration, sql, ip-address, default-prefixes]
level: advanced
status: docs-checked
description: "Move a Headscale tailnet back to the recommended IP prefixes: stop, restore defaults, reassign every node address from its ID in SQL, fix policy."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrate back to the recommended prefixes

This updates the IP addresses of all nodes and might have a severe impact on your environment. At a minimum, create a backup of your database and test the steps in a representative demo environment first.

1. Stop Headscale.
2. Restore the defaults in the config file:

```yaml
prefixes:
  v4: 100.64.0.0/10
  v6: fd7a:115c:a1e0::/48
```

3. Update the `nodes.ipv4` and `nodes.ipv6` columns in the database and assign each node a unique IPv4 and IPv6 address. The FAQ's SQL statement assigns addresses based on the node ID:

```sql
UPDATE nodes
SET ipv4=concat('100.64.', id/256, '.', id%256),
    ipv6=concat('fd7a:115c:a1e0::', format('%x', id));
```

4. Update the policy for any changed IP addresses.
5. Start Headscale. Nodes should reconnect within a few seconds and receive their new addresses.

## Gotchas

- Tailscale only supports the prefixes `100.64.0.0/10` and `fd7a:115c:a1e0::/48` or smaller subnets thereof.
- The default SQLite database path in the example config is `/var/lib/headscale/db.sqlite`.

## Checked

2026-11-04. Confirmed against the Headscale FAQ (How can I migrate back to the recommended IP prefixes: warning, steps, SQL statement) and config-example.yaml (database path). Removed the Gotchas about other hard-coded addresses and the verification commands, which the FAQ does not state.

Method: documentation only; no commands were run.
