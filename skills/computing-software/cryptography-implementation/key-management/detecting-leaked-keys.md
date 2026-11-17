---
id: computing-software.cryptography-implementation.key-management.detecting-leaked-keys
name: detecting-leaked-keys
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, key-leak-detection, secret-scanning, gitleaks, trufflehog, github-secret-scanning, push-protection, key-compromise, canary-tokens]
level: practitioner
status: docs-checked
description: "Find leaked private keys and secrets in git history, images, logs and public sources with gitleaks, trufflehog and secret scanning, and spot anomalous key use."
sources: ["https://github.com/gitleaks/gitleaks", "https://github.com/trufflesecurity/trufflehog", "https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting leaked keys

## Scan repositories (including history)
```
gitleaks git -v                                  # git history of the current repo
gitleaks dir -v <path>                           # files and directories, not history
trufflehog git file://. --results=verified       # only credentials confirmed live
trufflehog github --org=example --results=verified
```
Current gitleaks uses the `git` and `dir` commands, and trufflehog uses `--results` (`verified`, `unknown`) to
filter output. Run gitleaks as a pre-commit hook too (see its README). Also look for keystore files and base64
blobs in config.

## Platform features
- GitHub secret scanning and push protection; for partner patterns GitHub notifies the provider, who can take
  action such as revoking the credential.
- Other hosts offer equivalent scanning; enable it.

## Other leak locations
- Container images: trufflehog can scan them (`trufflehog docker --image <image> --results=verified`).
- CI logs and artifacts, crash dumps, support bundles, shared drives, paste sites.
- Mobile apps: decompile release builds and grep for keys.

## Detect use, not just presence
- Cloud audit logs: KMS Decrypt from unknown principals or regions, IAM keys used from unfamiliar networks.
- Canary tokens: plant fake credentials in repos and configs; any use alerts you.
- Certificate Transparency monitoring for unexpected certificates on your domains (sign of key or account misuse).

## Response order
1. Revoke/rotate the credential first (history rewriting does not un-leak it).
2. Investigate use in the window it was exposed.
3. Then clean history if needed and add prevention (pre-commit hook, push protection).

## Verify
- [ ] CI runs gitleaks on every PR; push protection enabled.
- [ ] Canary credential use generates an alert in a test.

## Checked

2026-11-01. Confirmed in the gitleaks and trufflehog READMEs: `gitleaks git`/`gitleaks dir`, trufflehog
`git`, `github`, `docker` sources and `--results=verified|unknown`; GitHub secret scanning page: push protection and
partner notification. Fixed: removed deprecated `detect`/`protect` and `--only-verified` forms. Removed: private key
regex, file extension list, trivy, git filter-repo, AWS quarantine, GuardDuty/Defender/SCC, canarytokens.org.
Method: documentation only; no commands were run.
