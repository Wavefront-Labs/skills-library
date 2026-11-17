---
id: computing-software.cloud-infrastructure-engineering.talos-linux.talos-support-bundle
name: talos-support-bundle
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [support-bundle, talosctl-support, age, encryption, logs, diagnostics]
level: practitioner
status: docs-checked
description: "Collect, encrypt and decrypt a talosctl support bundle: what it contains, default age recipients, adding your own recipients, opting out, and attaching it to issues safely."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/troubleshooting/support-bundle.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`talosctl support` gathers logs, resources and diagnostics from the nodes you name into one archive. Include all control plane nodes plus the affected workers:

```bash
talosctl -n <IP1>,<IP2>,<IP3> support
```

Output is `support-<cluster>.zip.age` (or `support.zip.age` if the cluster name is unknown); change with `--output` (`-O`) and parallelism with `--num-workers` (`-w`). Per node it holds kernel logs, logs of all Talos services and `kube-system` pods, Talos COSI resources without secrets, the COSI runtime state graph, a process snapshot, IO pressure snapshot, mounts, PCI info and the Talos version; cluster-wide it adds Kubernetes nodes and `kube-system` pod manifests. Secrets are excluded, but hostnames, IPs and workload names can leak, hence encryption.

Encryption (introduced in Talos 1.14) uses age. Default recipients are the SSH keys of public `siderolabs` GitHub organization members, so only Sidero Labs can decrypt, making the file safe to attach to a public GitHub issue.

Add yourself as a recipient (flag repeatable; values are `age1...` or SSH public keys):

```bash
talosctl -n <IP1>,<IP2>,<IP3> support \
    --encryption-recipients "$(cat <ssh-public-key-file>)" \
    --encryption-recipients age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
```

Internal use only (needs at least one recipient):

```bash
talosctl -n <IP1>,<IP2>,<IP3> support \
    --encryption-no-default-recipients \
    --encryption-recipients "$(cat <ssh-public-key-file>)"
```

Plain archive: `--no-encryption -O support.zip`; it cannot be combined with the recipient flags and must be treated as sensitive, never attached publicly.

Decrypt with the age CLI:

```bash
age --decrypt --identity <ssh-private-key-file> --output support.zip support-<cluster>.zip.age
```

## Checked

2026-11-04. Contents, file naming, flags and decrypt command confirmed on the Support Bundle page.

Method: documentation only; no commands were run.
