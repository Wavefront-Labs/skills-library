---
id: computing-software.database-administration.cockroachdb.cockroach-init
name: cockroach-init
category: computing-software
field: database-administration
product: cockroachdb
tags: [cockroach-init, cluster-initialization, join, cluster-name, bootstrap]
level: intro
status: docs-checked
description: "Initialize a new multi-node CockroachDB cluster once with cockroach init, targeting a node listed in --join, with certs-dir and cluster-name rules."
sources:
  - https://www.cockroachlabs.com/docs/stable/cockroach-init
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: perform the one-time bootstrap of a new multi-node cluster after its nodes have been started with `cockroach start`.

Rules from the page:
- Required only for multi-node clusters; a single node started with `cockroach start-single-node` needs no init.
- Run it exactly once against a node that appears in the `--join` list of the started nodes, otherwise the cluster is not initialized correctly.
- After init, all nodes complete startup and print the CockroachDB version, the DB Console URL and the SQL URL.

Secure cluster (run on the node's machine, with the root client cert files `client.root.crt` and `client.root.key` plus `ca.crt` present in the certs dir):
```shell
cockroach init --certs-dir=certs --host=<address of this node>
```
Insecure test cluster: `cockroach init --insecure --host=<address of this node>`.

Flags specific to init: `--cluster-name` (required if the cluster was started with a cluster name, to verify identity) and `--disable-cluster-name-verification` (must be paired with `--cluster-name`). Client connection flags and logging flags are shared with other client commands. `cockroach init --help` lists them.

Verify: after init, the started nodes print the version, DB Console URL and SQL URL.

## Checked
2026-11-03. Confirmed on the cockroach init page: one-time initialization of multi-node clusters, no init for a single-node cluster, target must be a node listed in `--join`, secure and insecure command forms, `--cluster-name` and `--disable-cluster-name-verification` (must be paired with `--cluster-name`), and the startup output. Removed: the uncited failure-mode paragraph and the `SHOW CLUSTER SETTING version` verify step.
Method: documentation only; no commands were run.
