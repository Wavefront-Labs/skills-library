---
id: computing-software.cybersecurity-defensive.application-security.software-and-data-integrity-failures
name: software-and-data-integrity-failures
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [integrity-failures, owasp-a08, insecure-deserialization, code-signing, auto-update-security, ci-cd-integrity]
level: practitioner
status: gated
description: "Address OWASP A08 software and data integrity failures: insecure deserialisation, unsigned updates, untrusted CDNs and plugins, and CI/CD pipelines that can be tampered with."
sources: ["https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/", "https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html", "https://slsa.dev/spec/v1.0/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Software and data integrity failures (OWASP A08:2021) (gated: unconfirmed, source is paywalled or blocked)

Code and data are trusted without verifying they came from where you think and were not modified. Examples:
SolarWinds-style build compromise, auto-updaters fetching unsigned packages, apps deserialising attacker-
controlled objects.

## Insecure deserialisation
- Never deserialise untrusted data with native object serialisers: Java `ObjectInputStream`, .NET
  `BinaryFormatter` (Microsoft states it is dangerous and cannot be secured), Python `pickle`, PHP `unserialize`, and YAML
  loaders that construct objects (PyYAML `yaml.load` with an unsafe Loader: use `yaml.safe_load`; SnakeYAML cannot be used safely unless `SafeConstructor` is used).
- Use data-only formats (JSON) with schema validation (OWASP Deserialization Cheat Sheet recommends a safe, standard data interchange format).
- Signed blobs (HMAC) for data that must round-trip through the client (view state, cookies).

## Software updates and plugins
- Updates must be signed and verified before install.
- Plugins/extensions only from trusted, verified sources.
- Third-party scripts loaded from CDNs should be pinned and integrity-checked.

## CI/CD integrity
- Protected branches with required review; build only from reviewed commits.
- Least-privilege pipeline credentials; isolated, ephemeral runners.
- Sign build artefacts and generate provenance; verify signatures at deploy
  time (admission controller or deploy script).
- Dependency integrity: lockfiles with hashes, private registry proxy.

## Verify
Grep shows no native deserialisation of request data; deployment rejects an unsigned image; update client
refuses a package with a broken signature; pipeline config changes require review.

## Checked

2026-10-28. Confirmed in the OWASP Deserialization Cheat Sheet: `ObjectInputStream`, `BinaryFormatter` (Microsoft's statement), `pickle`, `unserialize`, PyYAML `yaml.safe_load`, SnakeYAML `SafeConstructor`. Removed: Ruby `Marshal`, the ".NET 9 removal" claim, JEP 290 / `jdk.serialFilter`, Jackson default typing, TUF, Sigstore cosign, SLSA and Subresource Integrity named claims (not found in the fetched pages; the SLSA page returned a stub). The A08:2021 category name could not be confirmed (OWASP Top 10 page stub), so it is gated.
Method: documentation only; no commands were run.
