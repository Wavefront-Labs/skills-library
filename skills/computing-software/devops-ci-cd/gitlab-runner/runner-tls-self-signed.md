---
id: computing-software.devops-ci-cd.gitlab-runner.runner-tls-self-signed
name: runner-tls-self-signed
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [tls, self-signed, ca-certificate, tls-ca-file, x509]
level: practitioner
status: docs-checked
description: "Make the runner trust a private CA when talking to GitLab."
sources: ["https://docs.gitlab.com/runner/configuration/tls-self-signed/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Self-signed and private CA certificates

`x509: certificate signed by unknown authority` on register, or in a POST to `/api/v4/jobs/request`, means the runner does not trust the GitLab certificate.

Options:
1. Default: the runner reads the system certificate store.
2. `--tls-ca-file=/path/to/ca.crt` at registration, or `tls-ca-file` in `[[runners]]`; the file is read every time the runner accesses GitLab.
3. A PEM file at a predefined path named after the host: `/etc/gitlab-runner/certs/gitlab.example.com.crt` as root, `~/.gitlab-runner/certs/gitlab.example.com.crt` as non-root, or `./certs/` on other systems. DER format is not supported. For `https://gitlab.example.com:8443/` the file is still `gitlab.example.com.crt`.

If the server certificate is signed by your CA, supply the CA certificate, with intermediates in the same file. Download a certificate with `openssl s_client -showcerts -connect gitlab.example.com:443 -servername gitlab.example.com` and check it with `openssl s_client -CAfile`.

## Checked

2026-11-03. Confirmed against the three trust options, the PEM-only rule, certificate paths, port handling and intermediates on Self-signed certificates.

Method: documentation only; no commands were run.
