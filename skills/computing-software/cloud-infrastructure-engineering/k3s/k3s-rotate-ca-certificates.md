---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-rotate-ca-certificates
name: k3s-rotate-ca-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, certificate-rotate-ca, cross-signed-ca, rotate-default-ca-certs]
level: sme
status: docs-checked
description: "Rotate custom or self-signed K3s CA certificates with k3s certificate rotate-ca, non-disruptively when the root is unchanged."
sources:
  - https://docs.k3s.io/cli/certificate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rule: never overwrite the in-use /var/lib/rancher/k3s/server/tls. Stage new files in a separate directory, load them with rotate-ca, then restart K3s on all nodes, servers first, then agents. The command runs integrity checks; on failure it logs an error and changes nothing.

Custom CAs: rotation is non-disruptive if the same root CA is used. Using a new root is disruptive and needs `k3s certificate rotate-ca --force`; nodes joined with a secure token need the new token and pods must restart to trust the new root.

```
mkdir -p /opt/k3s/server/tls
cp /var/lib/rancher/k3s/server/tls/root-ca.* /var/lib/rancher/k3s/server/tls/intermediate-ca.* /opt/k3s/server/tls
cp /var/lib/rancher/k3s/server/tls/service.key /opt/k3s/server/tls
curl -sL https://github.com/k3s-io/k3s/raw/main/contrib/util/generate-custom-ca-certs.sh | DATA_DIR=/opt/k3s bash -
k3s certificate rotate-ca --path=/opt/k3s/server
```

Copying service.key keeps existing service-account tokens valid.

Default self-signed CAs: rotation is disruptive; nodes joined with a secure token must be reconfigured with the new CA hash. If the new CAs are not cross-signed by the old, use --force and restart pods. The script contrib/util/rotate-default-ca-certs.sh builds CAs cross-signed by the existing ones and prints the new token values:

```
curl -sL https://github.com/k3s-io/k3s/raw/main/contrib/util/rotate-default-ca-certs.sh | bash -
k3s certificate rotate-ca --path=/var/lib/rancher/k3s/server/rotate-ca
```

Update the token in the .env file, systemd unit or config.yaml before restarting.

## Checked

2026-11-08: read the whole k3s certificate page (raw markdown from the k3s-io/docs repo, which backs docs.k3s.io/cli/certificate). Confirmed the staging rule, integrity-check behaviour, non-disruptive same-root rotation, --force for a new root, both example command sequences and the token update locations. The scripts themselves were not read.

Method: documentation only; no commands were run.
