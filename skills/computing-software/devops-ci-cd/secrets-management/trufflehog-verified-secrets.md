---
id: computing-software.devops-ci-cd.secrets-management.trufflehog-verified-secrets
name: trufflehog-verified-secrets
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, secret-scanning, trufflehog, trufflehog-verify, verified-secrets, results-filter, only-verified, detectors, trufflehog-github-action, scan-s3, scan-docker-images, false-positive-reduction]
level: practitioner
status: gated
description: "Use TruffleHog's live verification to triage leaked secrets: --results=verified, unknown vs unverified, scanning git, GitHub orgs, images and S3, CI action setup and privacy caveats."
sources: ["https://github.com/trufflesecurity/trufflehog/blob/main/README.md", "https://docs.trufflesecurity.com/", "https://github.com/marketplace/actions/trufflehog-oss"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TruffleHog verified secrets

TruffleHog's detectors (the README says it classifies over 800 secret types, over 700 with active verification) not only pattern-match but **call the provider's API** with a
candidate credential to see if it works (e.g. AWS `sts:GetCallerIdentity`, Slack
`auth.test`). That turns thousands of regex hits into a short list of *live* keys.

## Result classes
- **verified**: the credential authenticated just now. Treat as an incident.
- **unverified**: matched the pattern, verification failed (revoked, fake, or wrong
  scope). Usually lower priority, but still review in your own code.
- **unknown**: verification couldn't complete (network error, rate limit, detector
  without verifier). Re-run or investigate manually.

## Commands
```bash
trufflehog git file://. --results=verified,unknown          # local repo, full history
trufflehog git https://github.com/acme/api.git --since-commit main --branch feature-x --results=verified
trufflehog github --org=acme --token="$GH_TOKEN" --results=verified --include-members
trufflehog docker --image ghcr.io/acme/api:1.4.0 --results=verified
trufflehog s3 --bucket=acme-artifacts --results=verified
trufflehog filesystem ./dist --results=verified
trufflehog git file://. --json --no-update > findings.json
```
`--results` takes `verified`, `unknown`, `unverified`, `filtered_unverified` and defaults to `verified,unverified,unknown`.
The older `--only-verified` is still accepted (3.99.2). `--fail` returns exit 183 when any result of the
selected classes is reported (run: fake token, 183 by default, 0 with `--results=verified`); the README wording "valid credentials" only holds
if you also pass `--results=verified`. `--no-verification` turns verification off.

## CI (GitHub Actions)
```yaml
- uses: actions/checkout@v6
  with: { fetch-depth: 0 }
- uses: trufflesecurity/trufflehog@main     # pin to a release tag/SHA in practice
  with:
    extra_args: --results=verified,unknown
```
The action takes `base` and `head` inputs; see its README for the push versus pull_request depth handling.

## Privacy and safety
- Verification sends the candidate secret to the provider's real API endpoint from the
  scanning host. That's the provider that issued it, but it's still outbound traffic
  with a credential: run verification from a controlled network, not a random laptop.
- Some detectors verify by calling endpoints that log access (it will appear in the
  victim account's audit log, which is useful evidence).
- Air-gapped scanning: `--no-verification` and accept more noise.
- Custom detectors (config YAML with regex + optional webhook verifier) cover internal
  token formats.

## Workflow
1. Verified finding -> revoke/rotate immediately (see
   `computing-software.devops-ci-cd.secrets-management.remediating-a-leaked-secret`), then
   clean up.
2. Unknown -> rerun; if still unknown, test manually in a sandbox.
3. Unverified in your own repos -> confirm it's dead or a fixture, then allowlist via
   `--exclude-paths` file or `trufflehog:ignore` comments.

## Verify
Commit a fake `ghp_` + 36 random alphanumerics token to a scratch repo: `trufflehog git file://. --fail` exits 183 and reports
"unverified result" (Detector Type: Github); with `--results=verified` it exits 0. Live-verified output was not exercised here
(needs a real credential: use a provider canary token and expect `Verified: true`) (gated: unconfirmed, no live credential tested).
