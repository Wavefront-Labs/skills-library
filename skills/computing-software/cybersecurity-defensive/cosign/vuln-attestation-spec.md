---
id: computing-software.cybersecurity-defensive.cosign.vuln-attestation-spec
name: vuln-attestation-spec
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, vuln-attestation, vulnerability-scan, scanner, in-toto]
level: advanced
status: docs-checked
description: "The cosign vulnerability scan record predicate: invocation, scanner (uri, version, db, result) and scan start and finish timestamps, inside an in-toto Statement."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/specs/COSIGN_VULN_ATTESTATION_SPEC.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_attest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulnerability scan record

predicateType: `https://cosign.sigstore.dev/attestation/vuln/v1`, inside an in-toto Statement (`_type` `https://in-toto.io/Statement/v0.1`). It is one of the predicates cosign defines itself, alongside the generic predicate.

Predicate fields:
- `invocation`: `parameters` (for example `--format=json`), `uri` (for example a CI run URL), `event_id`, `builder.id`
- `scanner`: `uri` (optional), `version` (optional), `db` (`uri` and `version`, both optional) and `result` (object)
- `metadata`: `scanStartedOn` and `scanFinishedOn`, both required timestamps

The spec calls `scanner.result` "the most important part": it stores the scan result as a whole, so people can use policy engine tooling to allow or deny images based on it.

The spec's example scanner is Trivy (`trivy image -f json alpine:3.12`), with the full JSON output embedded in `scanner.result`, a `scanner.uri` of the form `pkg:github/aquasecurity/trivy@...`, and the db version given as a string such as `v1-2021080612`. The spec's template JSON uses `//` comments for illustration, so it is not valid JSON verbatim.

Attaching: the `cosign attest` docs list `vuln` among the `--type` values, so a scan record can be attached with `cosign attest --type vuln --predicate <FILE> <IMAGE>`. Neither page says whether `--predicate` should hold the whole predicate or only the scanner result.

## Checked

2026-11-04. Confirmed against the cosign specs page COSIGN_VULN_ATTESTATION_SPEC and the cosign_attest docs page: predicateType, field list, optional and required markers, statement on `scanner.result`, Trivy example, `vuln` as a `--type` value. Removed: the `cosign verify-attestation --type vuln --policy` command (not on either page), and three operational tips (include versions to reject stale data, check `scanFinishedOn` in policy, download an attestation to inspect it), none of which the pages state.
Method: documentation only; no commands were run.
