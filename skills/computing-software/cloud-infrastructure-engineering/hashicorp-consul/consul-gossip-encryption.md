---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-gossip-encryption
name: consul-gossip-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, gossip-encryption, consul-keygen, serf-encryption]
level: practitioner
status: docs-checked
description: "Generate a gossip key with consul keygen, enable it with encrypt in agent config, and roll it out to a running cluster in three restarts."
sources: ["https://developer.hashicorp.com/consul/commands/keygen", "https://developer.hashicorp.com/consul/docs/reference/agent/configuration-file/encryption", "https://developer.hashicorp.com/consul/docs/secure/encryption/gossip/enable/existing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Gossip encryption secures communication between agents in the gossip pool using a shared key that is 32 bytes, base64 encoded.

```sh
consul keygen
```

```hcl
encrypt = "<key from keygen>"
```

`encrypt_verify_incoming` and `encrypt_verify_outgoing` both default to `true`. All nodes in a cluster must share the same key. The key is persisted to the data directory on first start; if `encrypt` is provided after the agent was initialised with a key, the new value is ignored with a warning.

Enabling on an existing datacenter (rolling restart of every server and client each time):
1. Set `encrypt` with `encrypt_verify_incoming = false` and `encrypt_verify_outgoing = false`.
2. Set `encrypt_verify_outgoing = true` (agents send encrypted gossip but still accept unencrypted).
3. Set both `encrypt_verify_incoming = true` and `encrypt_verify_outgoing = true`.

Gotchas:
- `consul reload` and `kill -HUP` do not change gossip configuration; restart the agents.
- To change the key later, use `consul keyring` (see `consul-keyring-rotation`).
- LAN gossip uses port 8301 and WAN gossip 8302, both TCP and UDP, per the ports reference.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: commands/keygen, reference/agent/configuration-file/encryption (`encrypt`, verify flags, defaults, persistence), secure/encryption/gossip/enable/existing (three-step rollout, restart not reload), reference/architecture/ports (8301, 8302). Fixed: the old text said to stage with both verify settings false then switch both to true (it omitted the intermediate outgoing-only step). Removed: unsupported remarks about silent drops, TLS/ACL pairing, and the Verify step.
Method: documentation only; no commands were run.
