---
id: computing-software.devops-ci-cd.argo-workflows.cli-mutual-tls
name: cli-mutual-tls
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [mutual-tls, client-certificate, certificate-authority, argo-cli, kubeconfig-server-mode]
level: advanced
status: docs-checked
description: "Connect the argo CLI to a server or proxy that requires client certificates with --client-certificate, --client-key and --certificate-authority."
sources: ["https://argo-workflows.readthedocs.io/en/latest/tls/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CLI mutual TLS to Argo Server
When the Argo Server or its proxy needs mutual TLS, pass `--client-certificate` and `--client-key` together, and `--certificate-authority` to trust the CA that signed the server certificate:

```bash
argo --argo-server argo.example.com:443 \
  --secure \
  --certificate-authority ca.crt \
  --client-certificate client.crt \
  --client-key client.key \
  list
```

The flags work with both the gRPC and HTTP/1 clients, including artifact downloads with `argo cp`.

Gotchas:
- Client certificates and certificate authorities from a kubeconfig context are used for direct Kubernetes connections, but not automatically in server mode. Pass the three flags explicitly when going through Argo Server.
- Unlike `--secure` and `--insecure-skip-verify`, these flags have no `ARGO_*` environment variable equivalents, so scripts and CI must pass them on the command line.

## Checked

2026-11-08. Read the Argo Workflows TLS page in full (raw markdown) and confirmed the mutual TLS flags, example, gRPC and HTTP/1 support, kubeconfig caveat, and lack of ARGO_* environment equivalents. Removed: advice that mutual TLS implies --secure and the proxy host remark, which the page does not state.

Method: documentation only; no commands were run.
