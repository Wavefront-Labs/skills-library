---
id: computing-software.cloud-infrastructure-engineering.cert-manager.cmctl-cli
name: cmctl-cli
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [cmctl, cli, renew, approve, deny, status-certificate, create-certificaterequest, convert]
level: practitioner
status: docs-checked
description: "Use cmctl: install it, then renew, approve or deny, check status, create a CertificateRequest, convert manifests, migrate API versions and the experimental x commands."
sources:
  - https://cert-manager.io/docs/reference/cmctl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install: `brew install cmctl`, a release binary on your `$PATH`, or `go install github.com/cert-manager/cmctl/v2@latest`. The legacy kubectl plugin is not recommended. cert-manager 1.14 is the last release shipping a `cert-manager-ctl` image or binary. Global flag: `--log-flush-frequency` (default 5s).

Subcommands documented on the page:
- `approve` / `deny`: act on a CertificateRequest; flags `-n`, `--reason`, `--message`. The internal approver may auto-approve first unless the controller runs with `--controllers=*,-certificaterequests-approver`.
- `renew`: trigger renewal by name, `-l/--selector`, `--all` (one namespace) or `-A/--all-namespaces`; supports `--namespace` and `--context`.
- `status certificate <name> -n <ns>`: shows the Certificate with its CertificateRequest, Secret, Issuer, and for ACME the Order and Challenges, plus conditions and events.
- `create certificaterequest --from-certificate-file <file>`: generates a local key (`<name>.key`, `--output-key-file`); `--fetch-certificate` waits and writes `<name>.crt` (`--output-certificate-file`); `--timeout` defaults to 5 minutes. Output goes to local files, not Kubernetes.
- `convert`: file, directory or URL, YAML or JSON; `--output-version` (default latest); `-o` destination (default stdout YAML).
- `upgrade migrate-api-version`: migrates stored resources to `v1` for pre-v1 installs moving to 1.6+; example flags `--qps 5 --burst 10`.
- `check` and `inspect` appear in the command list but are not detailed on this page; the kubectl install page shows `cmctl check api --wait=2m`.
- `x` (experimental, may change): `x create csr` (`-f`, `-k`, `-w`, `-c`), `x install` (`--set`, `--dry-run`), `x uninstall` (`--namespace`, `--dry-run`; CRDs kept by default from v2.0.0).

## Checked

2026-11-03: Confirmed against the cmctl reference page: install via Homebrew, release binary or `go install github.com/cert-manager/cmctl/v2@latest`, legacy kubectl plugin not recommended, 1.14 as last release with `cert-manager-ctl` artifacts, `--log-flush-frequency` default 5s, approve/deny flags and the `--controllers=*,-certificaterequests-approver` note, renew selectors (`-l`, `--all`, `-A`, `--namespace`, `--context`), `status certificate`, `create certificaterequest` flags and 5 minute default, convert behaviour, `upgrade migrate-api-version --qps 5 --burst 10`, and the experimental `x create csr`, `x install` and `x uninstall` behaviour including CRDs kept from v2.0.0. Removed: the claim that `check api` and `inspect secret` flags exist beyond the command list (this page only lists `check` and `inspect`).

Method: documentation only; no commands were run.
