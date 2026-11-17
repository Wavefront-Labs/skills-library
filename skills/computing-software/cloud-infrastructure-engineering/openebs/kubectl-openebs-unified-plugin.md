---
id: computing-software.cloud-infrastructure-engineering.openebs.kubectl-openebs-unified-plugin
name: kubectl-openebs-unified-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [kubectl-plugin, kubectl-openebs, mayastor, localpv-lvm, localpv-zfs, localpv-hostpath, namespace]
level: practitioner
status: docs-checked
description: "Install and use the unified kubectl openebs plugin: localpv-hostpath, localpv-lvm, localpv-zfs and mayastor subcommands, namespace from the kubeconfig context, output flags."
sources:
  - https://openebs.io/docs/user-guides/kubectl-openebs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `kubectl openebs` plugin is one CLI for Local PV Hostpath, LVM, ZFS and Replicated PV Mayastor, especially when you installed through the OpenEBS Helm chart. It folds in the existing `kubectl-mayastor` commands and adds new ones for the local engines. Binaries for Linux are on the OpenEBS GitHub releases page; put one on your `$PATH` and check it with `kubectl openebs -V`.

Subcommands: `mayastor`, `localpv-lvm`, `localpv-zfs`, `localpv-hostpath` and `help`. The three Local PV commands each offer `get` (and `-o yaml` or `-o json` output). The `mayastor` command offers `drain`, `label`, `get`, `scale`, `set`, `cordon`, `uncordon`, `dump`, `upgrade` and `delete`. For example, `kubectl-openebs mayastor get pools` lists each pool with disks, node, status, capacity, allocated, available and committed.

**Namespace behaviour changed.** The old `kubectl-mayastor` assumed the `mayastor` namespace. Now, if you do not give `-n`, the plugin takes the namespace from the current kubeconfig context, which is `default` unless you set it. Set it with `kubectl config set-context --namespace=<namespace> --current`; for an install in `storage`, use `--namespace=storage`. Changing the context namespace also affects other kubectl plugins that do not set a namespace explicitly. Use `-k` to select a kubeconfig file, and for Mayastor `-r` for a REST endpoint and `-t` for the REST timeout (default 10s).

## Checked

2026-11-04. Confirmed against the Kubectl OpenEBS Plugin page: install and `-V`, the subcommand lists, `get` and `-o yaml|json` on the local engines, namespace resolution from the kubeconfig context, `-k`, `-r` and `-t`, and the pools example. Nothing removed.

Method: documentation only; no commands were run.
