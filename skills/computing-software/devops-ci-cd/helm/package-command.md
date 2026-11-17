---
id: computing-software.devops-ci-cd.helm.package-command
name: package-command
category: computing-software
field: devops-ci-cd
product: helm
tags: [package, chart-archive, sign, app-version, dependency-update, destination]
level: practitioner
status: docs-checked
description: "Package a chart directory into a versioned .tgz with helm package, overriding version and appVersion and signing."
sources:
  - "https://helm.sh/docs/helm/helm_package/"
  - "https://helm.sh/docs/topics/charts/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helm package [CHART_PATH] [...]` packages a chart directory (it must contain `Chart.yaml`) into a versioned chart archive, as used by Helm package repositories.

```bash
helm package ./mychart -d dist --version 1.4.0 --app-version 2.1.0 -u
```

Flags from the reference:

- `--version` sets the chart version to a semver version at package time.
- `--app-version` sets `appVersion`.
- `-d, --destination` is where the archive is written (default `.`).
- `-u, --dependency-update` runs a dependency update into `charts/` first.
- `--sign` signs with a PGP private key, used with `--key` (a substring of the key's uid) and `--keyring`; `--passphrase-file` reads the passphrase from a file or stdin with `-`.
- `--username`, `--password`, `--ca-file`, `--cert-file`, `--key-file`, `--insecure-skip-tls-verify` and `--plain-http` apply when dependencies are fetched.

If `--keyring` is not specified, Helm usually defaults to the public keyring unless your environment is otherwise configured.

The environment variable `SOURCE_DATE_EPOCH` (a non-negative integer of whole seconds since 1970-01-01 UTC) stamps every file in the archive with that modification time so repackaging gives reproducible archives.

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/helm/helm_package/ (synopsis, flags, defaults, signing flags, keyring default) and https://helm.sh/docs/howto/charts_tips_and_tricks/ (SOURCE_DATE_EPOCH). Removed: the archive file-name rule and the `.tgz.prov` and upload sentence (not on the pages).
Method: documentation only; no commands were run.

