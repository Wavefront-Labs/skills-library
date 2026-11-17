---
id: computing-software.cloud-infrastructure-engineering.keda.trust-custom-ca-in-keda-operator
name: trust-custom-ca-in-keda-operator
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [ca-dir, custom-ca, unsafessl, trusted-ca, self-signed-ca, helm-cadirs]
level: advanced
status: docs-checked
description: "Register private or self-signed CAs in the KEDA operator trust store with --ca-dir instead of using the insecure unsafeSsl scaler parameter."
sources:
  - https://keda.sh/docs/2.17/operate/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some environments need KEDA to talk to endpoints signed by a CA that is not publicly trusted; the page cites a case on AWS where the CA is not registered as trusted. Several scalers let you skip validation with the `unsafeSsl` parameter, but the page calls that not ideal because it accepts any certificate, which is not secure.

The supported fix is to register custom CAs for SDKs that can use them:
1. Place the CA certificates in a directory.
2. Pass the directory to the KEDA operator with `--ca-dir=<directory>`. The default location the operator checks is `/custom/ca`.
3. To use several directories, repeat the flag: `--ca-dir=` can be given multiple times.

KEDA tries to register every certificate found in these directories as a trusted CA.

With kustomize or Helm:
- list directories under the value `certificates.operator.caDirs`;
- mount the certificate volumes with `volumes.keda.extraVolumes` and `volumes.keda.extraVolumeMounts`.


This setting concerns outbound trust from the operator. It is separate from the internal certificates in `kedaorg-certs`, which secure traffic between KEDA's own components.

## Checked

2026-11-03. Confirmed on the 2.17 Operate Security page: --ca-dir, /custom/ca default, repeated flag, unsafeSsl note, Helm values.

Method: documentation only; no commands were run.
