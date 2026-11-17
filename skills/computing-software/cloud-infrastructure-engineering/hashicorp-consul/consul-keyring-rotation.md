---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-keyring-rotation
name: consul-keyring-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, keyring-rotation, consul-keyring, key-rotation]
level: practitioner
status: docs-checked
description: "Install a new gossip key, promote it as primary, and remove the old key with consul keyring, checking all nodes agree at each step."
sources: ["https://developer.hashicorp.com/consul/commands/keyring", "https://developer.hashicorp.com/consul/docs/secure/encryption/gossip/rotate/vm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rotation is centralised: run it from a single node of the datacenter.

```sh
NEW=$(consul keygen)
consul keyring -install "$NEW"      # broadcast to all members
consul keyring -list                # every node must report the new key
consul keyring -use "$NEW"          # make it primary
consul keyring -remove "<old key>"  # then list again: one key, all nodes
```

Do not proceed to `-use` until the `-list` count for the new key equals the number of agents; server agents show in the `WAN` section.

Rules from the command page:
- Only one actionable argument (`-list`, `-list-primary`, `-install`, `-remove`, `-use`) per run.
- Operations run only against server nodes and affect the LAN and WAN keyrings together; `-list` can use `-local-only` to skip WAN.
- `-remove` works only on a key that is not the primary.
- `-relay-factor` (non-zero, maximum 5) makes nodes relay their response through that many other nodes.
- Exit code 0 if all nodes reply without error, 1 if any node fails to reply or reports failure.
- ACLs: `keyring:read` for list, `keyring:write` for the others.
- Several keys may coexist during the transition; removing unneeded keys is up to the operator, and the docs call unused keys a security risk.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: commands/keyring (options, exit codes, ACLs, LAN and WAN behaviour) and secure/encryption/gossip/rotate/vm (the five-step procedure and the "do not proceed" rule). Removed: the claim that `encrypt` must be updated in agent config files after rotation (the encrypt page says the provided key is ignored once the agent is initialised), and the invented Verify step.
Method: documentation only; no commands were run.
