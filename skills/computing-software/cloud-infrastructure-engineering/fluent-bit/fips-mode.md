---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.fips-mode
name: fips-mode
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, fips, openssl, security, s3, azure-blob, md5]
level: sme
status: docs-checked
description: "Require the OpenSSL FIPS provider in Fluent Bit and understand its effect on hot reload, S3 and Azure Blob."
sources: ["https://docs.fluentbit.io/manual/administration/configuring-fluent-bit/yaml/service-section"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# FIPS mode

FIPS mode is available in Fluent Bit version 5.1 and greater. Set `security.fips_mode: on` in the service section (default `off`), or pass `--enable-fips` on the command line, to require the OpenSSL FIPS provider. It needs OpenSSL 3.0 or later with the FIPS provider installed on the host.

At startup Fluent Bit activates the provider and checks that a FIPS-approved algorithm can be fetched. If the provider is unavailable or cannot be activated, it logs the OpenSSL errors and exits rather than run with non-compliant cryptography.

```yaml
service:
  security.fips_mode: on
```

**Constraints**
- It cannot be changed by hot reload. If a reloaded configuration changes `security.fips_mode`, Fluent Bit halts the reload and keeps running with the previous configuration.
- Plugins that rely on MD5 change behaviour. The Amazon S3 output rejects `send_content_md5` at startup because that header requires MD5. The Azure Blob output derives block IDs with SHA-256 instead of MD5.

## Checked

2026-11-03. Confirmed on the Fluent Bit YAML Service section page (FIPS mode): 5.1 availability, OpenSSL 3.0 plus FIPS provider requirement, startup behaviour, `--enable-fips`, no change by hot reload, S3 `send_content_md5` rejection, Azure Blob SHA-256 block IDs. Removed: an unsourced rollout plan and verification step.

Method: documentation only; no commands were run.
