---
id: computing-software.database-administration.elasticsearch.enrollment-tokens-and-adding-nodes
name: enrollment-tokens-and-adding-nodes
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, enrollment-token, elasticsearch-security, adding-nodes, auto-configuration]
level: practitioner
status: docs-checked
description: "Add nodes and Kibana to a secured Elasticsearch 8.x cluster with enrollment tokens, understand what auto-configuration writes, and do it manually when tokens do not fit."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/_snippets/enroll-nodes.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/command-line-tools/create-enrollment-token.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/command-line-tools/reconfigure-node.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enrollment tokens and adding nodes securely

**Goal:** new nodes join with TLS and trusted certificates without hand-copying keystores.

## How 8.x auto-configuration works
On the first start of a new node, Elasticsearch enables and configures security, generates TLS keys and certificates for the transport and HTTP layers under `config/certs`, sets a password for the `elastic` user, and prints an enrollment token for Kibana (the first node starts as a single-node cluster).

## Add a node
On an existing node:
```bash
bin/elasticsearch-create-enrollment-token -s node      # valid 30 minutes
```
On the new node (before its first start, empty data dir):
```bash
bin/elasticsearch --enrollment-token <token>
# package installs:
bin/elasticsearch-reconfigure-node --enrollment-token <token>   # DEB/RPM installs only (under /usr/share/elasticsearch)
systemctl start elasticsearch
```
The enrollment process adds the existing nodes to the new node's `discovery.seed_hosts`. In a multi-node cluster you must then edit the nodes so each lists the others in `discovery.seed_hosts`; the first node has none configured and needs it added manually.

## Enroll Kibana
```bash
bin/elasticsearch-create-enrollment-token -s kibana
bin/kibana-setup --enrollment-token <token>       # or paste in Kibana's first-run UI
```

## Requirements and pitfalls
- Tokens last 30 minutes; create a new token for each node you add. Treat tokens as secrets.
- `elasticsearch-create-enrollment-token` only works on clusters that were auto-configured for security; scopes are `node` and `kibana`.
- Auto-generated certs come from a CA created on the first node; production with a corporate PKI should replace them deliberately.

## Manual path
1. `elasticsearch-certutil ca`, then `cert --ca elastic-stack-ca.p12` for transport.
2. Copy `elastic-certificates.p12` to each node, configure `xpack.security.transport.ssl.*`, store passwords in the keystore.

## Verify
`GET _cat/nodes?v` lists the new node; `GET _ssl/certificates` on it shows the same CA as other nodes.

## Checked

Checked 2026-10-25 against elastic/docs-content and elastic/elasticsearch `main` (Stack 9.x docs). Confirmed: token lifespan 30 minutes, `-s node|kibana`, `bin/elasticsearch --enrollment-token`, `bin/kibana-setup --enrollment-token`, `elasticsearch-reconfigure-node` is for DEB/RPM only, certificates under `config/certs`, `discovery.seed_hosts` behaviour. Removed unconfirmed claims about token contents, non-loopback binding requirements and the skip-auto-configuration conditions. The Manual path and Verify sections were not rechecked beyond certutil defaults (see the TLS skill).

Method: documentation only; no commands were run.
