---
id: computing-software.database-administration.cockroachdb.rotate-certificates
name: rotate-certificates
category: computing-software
field: database-administration
product: cockroachdb
tags: [rotate-certificates, certificate-rotation, combined-ca, create-node, tls]
level: advanced
status: docs-checked
description: "Rotate CockroachDB client, node and CA certificates safely, including the combined CA certificate approach and when rotation is needed."
sources:
  - https://www.cockroachlabs.com/docs/stable/rotate-certificates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replace certificates before expiry or after compromise without cluster downtime.

When to rotate: certificates expiring soon, compliance policy, a compromised key, or a certificate content change such as adding a DNS name or load balancer IP (then only node certificates need rotation).

Client certificates:
```shell
cockroach cert create-client <username> --certs-dir=certs --ca-key=my-safe-directory/ca.key
```
Upload to the client and make the application use it (this can require restarting the client).

Node certificates: recreate in the same directory, listing every address the node can be reached at, with `--overwrite`:
```shell
cockroach cert create-node <node hostname> <other hostname> --certs-dir=certs --ca-key=my-safe-directory/ca.key --overwrite
```
Then upload (the page uses `scp`) the new `node.crt` and key to the node and reload without restart by sending `SIGHUP` to the process (`pkill -SIGHUP -x cockroach`), as the same user running it or one with sudo.

CA certificate: create a new CA key and a combined CA certificate. Rename the old key (`mv my-safe-directory/ca.key my-safe-directory/ca.old.key`), run `cockroach cert create-ca` with the new key, which yields `ca.crt` holding the new certificate followed by the old one. Distribute that combined `ca.crt` to all nodes and clients first (nodes pick it up when the certs directory is rescanned, clients when restarted), then create new node and client certificates signed with the new CA and reload them. The combined file lets nodes and clients verify certificates signed by either CA during the transition. Rotate the CA on a different schedule from node and client certificates, ideally months before changing them.

Failure mode: until node and client certificates are rotated they are still signed by the old CA, so with only the new CA nodes and clients cannot verify each other.

In the DB Console certificate details, confirm the **Valid Until** field shows the new expiry (the page's check).

## Checked

2026-11-03. Confirmed against the rotate certificates page: reasons to rotate, client and node certificate commands, `--overwrite`, `SIGHUP`, combined CA procedure and rationale. Removed: the `cockroach cert list` verification (not on the page).
Method: documentation only; no commands were run.
