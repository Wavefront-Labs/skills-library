---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-custom-receptor-ca-secret
name: awx-operator-custom-receptor-ca-secret
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, receptor, mtls, ca, execution-nodes, receptor-ca, openssl]
level: advanced
status: docs-checked
description: "Supply your own Receptor CA for control-to-execution node mutual TLS and understand that changing it breaks existing execution nodes."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/custom-receptor-certs.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator custom receptor ca secret

Control nodes on the cluster talk to execution nodes over mutual TLS TCP connections run by Receptor. Execution nodes verify incoming connections by checking that the x509 certificate was issued by a trusted CA. If you provide no CA, the operator generates one using OpenSSL.

To use your own, create a TLS secret from your local `ca.crt` and `ca.key`, named `{AWX Custom Resource name}-receptor-ca` (here the CR name is `awx-demo`):

```bash
kubectl create secret tls awx-demo-receptor-ca \
   --cert=/path/to/ca.crt --key=/path/to/ca.key
```

If the secret is created after AWX is deployed, restart the deployment: `kubectl rollout restart deployment awx-demo`.

Warning: changing the receptor CA breaks connections to existing execution nodes. They enter an unavailable state and jobs cannot run on them. Users must download and re-run the install bundle for each execution node, which replaces the TLS certificate files with ones signed by the new CA. The nodes should then appear in a ready state after a few minutes.

## Checked

2026-11-04. Confirmed against the AWX Operator "Custom Receptor CA" page: mutual TLS description, OpenSSL default, secret name pattern and command, restart command, and the warning. Removed the mesh-ingress `external_hostname` aside and the secret-type paragraph, which are not on this page.
Method: documentation only; no commands were run.
