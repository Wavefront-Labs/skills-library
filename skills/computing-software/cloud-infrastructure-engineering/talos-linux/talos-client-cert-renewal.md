---
id: computing-software.cloud-infrastructure-engineering.talos-linux.talos-client-cert-renewal
name: talos-client-cert-renewal
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [pki, talosconfig, kubeconfig, certificates, client-certificate, secrets-bundle, rbac]
level: practitioner
status: docs-checked
description: "Talos certificate lifetimes: server certs auto-rotate, client talosconfig and kubeconfig are yours to renew yearly; three ways to regenerate a talosconfig."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/security/cert-management.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos automatically manages and rotates all server-side certificates for etcd, Kubernetes and the Talos API. One caveat: the kubelet must be restarted at least once a year for its certificates to rotate; any upgrade or reboot of the node does it. Inspect Kubernetes certs on a control plane with `talosctl get KubernetesDynamicCerts -o yaml`.

Client certificates are the user's responsibility. Each download of a `kubeconfig` regenerates the client certificate, valid for a year. The `talosconfig` should be renewed at least yearly.

**From a control plane node** (needs a valid `talosconfig` with the `os:admin` role):

```shell
talosctl -n CP1 config new talosconfig-reader --roles os:reader --crt-ttl 24h
```

**From the secrets bundle** (`secrets.yaml` from `talosctl gen secrets`); the cluster name and endpoint arguments do not matter for a talosconfig:

```shell
talosctl gen config --with-secrets secrets.yaml --output-types talosconfig -o talosconfig <cluster-name> https://<cluster-endpoint>
```

**From the control plane machine configuration**, extract the root CA and mint a certificate:

```shell
yq eval .machine.ca.crt controlplane.yaml | base64 -d > ca.crt
yq eval .machine.ca.key controlplane.yaml | base64 -d > ca.key
talosctl gen key --name admin
talosctl gen csr --key admin.key --ip 127.0.0.1
talosctl gen crt --ca ca --csr admin.csr --name admin
```

Then place the base64 `ca`, `crt` and `key` values under the context in `talosconfig`.

## Checked

2026-11-04. Rotation behaviour, the one-year client lifetime and all three regeneration methods confirmed on the PKI and certificate lifetimes page.

Method: documentation only; no commands were run.
