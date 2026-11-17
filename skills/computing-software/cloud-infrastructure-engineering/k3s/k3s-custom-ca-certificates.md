---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-custom-ca-certificates
name: k3s-custom-ca-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, custom-ca, generate-custom-ca-certs, server-tls-dir]
level: sme
status: docs-checked
description: "Start K3s with your own root and intermediate CA by pre-creating the files in /var/lib/rancher/k3s/server/tls."
sources:
  - https://docs.k3s.io/cli/certificate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default K3s creates self-signed CAs valid 10 years on the first server; they are not auto-renewed. Authoritative CA data is stored in the datastore bootstrap key, encrypted with the server token (PBKDF2, AES256-GCM, HMAC-SHA1).

Caution: do not share root or intermediate CAs across clusters or reuse an existing private CA as the cluster CA. A client cert or kubeconfig from one cluster would then authenticate to the others, and Kubernetes has no CRL support, so revoking a leaked admin kubeconfig means fully replacing the CA.

If CA files exist at the first server start, generation is bypassed. Required files in /var/lib/rancher/k3s/server/tls:

- server-ca.crt/.key, client-ca.crt/.key, request-header-ca.crt/.key
- etcd/peer-ca.crt/.key and etcd/server-ca.crt/.key (required even without embedded etcd)
- service.key (service-account signing key, no certificate)

The repo script contrib/util/generate-custom-ca-certs.sh creates them. Run it before first start:

```
mkdir -p /var/lib/rancher/k3s/server/tls
cp /path/to/root-ca.pem /path/to/intermediate-ca.pem /path/to/intermediate-ca.key /var/lib/rancher/k3s/server/tls
curl -sL https://github.com/k3s-io/k3s/raw/main/contrib/util/generate-custom-ca-certs.sh | bash -
```

To use only a root, provide root-ca.pem and root-ca.key; with root and intermediate, root-ca.pem, intermediate-ca.pem and intermediate-ca.key. Without files the script generates them, and you should back them up for later rotation.

## Checked

2026-11-08: read the whole k3s certificate page (raw markdown from the k3s-io/docs repo, which backs docs.k3s.io/cli/certificate). Confirmed the 10-year default CA, bootstrap key encryption, CA reuse cautions, required file list, script usage and the root-only and root-plus-intermediate inputs. The script itself was not read.

Method: documentation only; no commands were run.
