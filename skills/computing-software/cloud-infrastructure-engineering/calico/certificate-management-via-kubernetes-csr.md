---
id: computing-software.cloud-infrastructure-engineering.calico.certificate-management-via-kubernetes-csr
name: certificate-management-via-kubernetes-csr
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [certificates, certificatemanagement, csr, signername, installation, tls, typha, tigerastatus]
level: advanced
status: docs-checked
description: "Let Calico components get TLS certificates from your own signer via Kubernetes CSRs: the Installation block, algorithms and monitoring."
sources:
  - https://docs.tigera.io/calico/latest/operations/certificate-management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use this when you must limit access to private keys or control which certificates are trusted. It relies on the Kubernetes Certificates API.

**Supported.** Key pairs: RSA (2048, 4096, 8192) or ECDSA (curve 256, 384, 521). Signatures: RSA or ECDSA with SHA 256, 384 or 512.

**Enable** by adding `certificateManagement` to the Installation:

```yaml
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  certificateManagement:
    caCert: <Your CA Cert in Pem format>
    signerName: <your-domain>/<signer-name>
    signatureAlgorithm: SHA512WithRSA
    keyAlgorithm: RSAWithSize4096
```

With an automatic signer and approver nothing more is needed.

**What happens.** An init container in each pod (calico-node, calico-typha) creates a CSR and the pod stays in `Init` until the CSR is approved and signed. CSR names are `<namespace>:<pod>:<first 6 chars of pod UID>`.

**Watch it:**
- `kubectl get pod -n calico-system -w`
- `kubectl get csr -w` (Pending, then Issued and Approved)
- `kubectl get tigerastatus`

**Your own signer** must watch Pending CSRs with `spec.signerName` equal to yours (skippable before Kubernetes 1.18), run security checks, put the certificate in the status, then approve and update the conditions. The page names `certificates.k8s.io/v1beta1`, so check the API version your cluster serves before building one.

## Checked

Read in full on 2026-11-08: the Manage TLS certificates used by Calico page, including the signer steps and the security requirements that follow them. The YAML, algorithm list, monitoring commands and signer steps match it.

Method: documentation only; no commands were run.
