---
id: computing-software.devops-ci-cd.helm.provenance-and-signing
name: provenance-and-signing
category: computing-software
field: devops-ci-cd
product: helm
tags: [provenance, signing, verify, pgp, prov-file, keyring, integrity]
level: advanced
status: docs-checked
description: "Sign charts with helm package --sign and verify them with helm verify or --verify using PGP keys and .prov files."
sources:
  - "https://helm.sh/docs/topics/provenance/"
  - "https://helm.sh/docs/helm/helm_verify/"
  - "https://helm.sh/docs/helm/helm_package/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Helm provenance lets users verify the integrity and origin of a chart. A provenance file sits beside the archive: `myapp-1.2.3.tgz` has `myapp-1.2.3.tgz.prov`.

Signing needs a valid PGP keypair in binary (not ASCII-armored) format for signing:

```bash
helm package --sign --key 'John Smith' --keyring /path/to/secring.gpg mychart
```

- `--key` must be a substring of the key's uid (name or email); the fingerprint cannot be used.
- If the private key has a passphrase you are prompted, or use `--passphrase-file`.
- GnuPG 2.1+ no longer keeps secret keys in a legacy secring file, so export one first: `gpg --export-secret-keys > /path/to/secring.gpg`.

Verification:

- `helm verify mychart-0.1.0.tgz` checks the chart against its `.prov`.
- `helm install --verify`, `helm pull --verify`, `helm dependency update --verify` run the same check; a failure aborts the install before rendering.
- `--keyring` points at public keys (default `~/.gnupg/pubring.gpg`). Since Helm 4.3.0, verification can also read GnuPG keybox files and ASCII-armored keyrings.

A failure looks like `Error: sha256 sum does not match`. Common causes: missing or corrupt `.prov`, or the signer's key not in your keyring.

For charts in OCI-based registries, the guide says the helm-sigstore plugin can publish provenance to an immutable transparency log (`helm sigstore upload`); creating provenance and signing with a GPG key is the same process. Repositories must serve the `.prov` at the same URI path as the chart plus `.prov`.

## Checked

2026-11-08. Read the Provenance page (v3 docs and current docs source), helm package, helm verify, helm pull and helm dependency update options. Confirmed --sign/--key/--keyring/--passphrase-file, --verify on install, pull and dependency update, and the Helm 4.3.0 keybox note. Replaced an unsupported OCI extra-layer claim with the documented helm-sigstore text.

Method: documentation only; no commands were run.
