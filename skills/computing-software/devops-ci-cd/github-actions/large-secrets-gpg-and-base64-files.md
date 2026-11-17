---
id: computing-software.devops-ci-cd.github-actions.large-secrets-gpg-and-base64-files
name: large-secrets-gpg-and-base64-files
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, large-secrets, secret-size-limit, gpg-encrypted-secrets, base64-secrets, binary-secrets]
level: practitioner
status: verified
description: "Handle secrets over the 48 KB limit or binary files (keystores, p12 certs, provisioning profiles) with gpg-encrypted files in the repo or base64 secrets decoded at runtime."
sources: ["https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets#storing-large-secrets", "https://docs.github.com/en/actions/reference/security/secrets#limits-for-secrets"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Large and binary secrets

Secrets are limited to **48 KB**. The documented workaround for larger secrets is a gpg-encrypted file in the repository
with the passphrase stored as a secret; base64 is a common way to keep small binaries as text.

## 1. Base64 for small binaries (under about 36 KB raw)
```bash
base64 release.keystore | gh secret set ANDROID_KEYSTORE_B64
```
```yaml
- name: Restore keystore
  env: { KEYSTORE_B64: "${{ secrets.ANDROID_KEYSTORE_B64 }}" }
  run: echo "$KEYSTORE_B64" | base64 --decode > "$RUNNER_TEMP/release.keystore"
```
Base64 expands data by about one third, so the 48 KB cap leaves roughly 36 KB of binary. GNU `base64` also wraps lines at 76 columns (30000 bytes became 40527 characters), so use `base64 -w0` when sizing against the cap (40000 characters).

## 2. GPG-encrypted file committed to the repo (any size)
```bash
gpg --symmetric --cipher-algo AES256 service-account.json     # writes service-account.json.gpg
gh secret set LARGE_SECRET_PASSPHRASE                         # the passphrase only
git add service-account.json.gpg                              # never the plaintext
```
```yaml
- name: Decrypt
  env: { PASSPHRASE: "${{ secrets.LARGE_SECRET_PASSPHRASE }}" }
  run: |
    gpg --quiet --batch --yes --decrypt --passphrase="$PASSPHRASE" \
      --output "$RUNNER_TEMP/service-account.json" service-account.json.gpg
```
GitHub's example comments: `--batch` prevents interactive prompts and `--yes` assumes yes for questions. The docs example
writes the decrypted file under `$HOME/secrets`.

## 3. Hygiene
- When using the gpg workaround, GitHub does not redact secrets that your workflow prints, so never print the
  decrypted material. Avoid structured data as secret values so redaction works for normal secrets.
- Write decrypted files outside the workspace so artifacts and caches do not pick them up.
- Rotating means re-encrypting and committing; the old `.gpg` file stays in git history, so rotate the underlying
  credential, not just the passphrase.
- Consider a secret manager fetched through OIDC for large material.

## Verify
- [ ] No plaintext version of the file was ever committed.
- [ ] Decrypt step works on a clean runner; output file is outside `$GITHUB_WORKSPACE`.

## Checked

Date: 2026-10-25. Documentation release: github/docs commit of 2026-10-23.
- 48 KB secret limit; the gpg --symmetric --cipher-algo AES256 workflow, passphrase stored as a secret, gpg --quiet --batch --yes --decrypt --passphrase --output decrypt step, and the warning that secrets printed under this workaround are not redacted: confirmed in the secrets reference and the use-secrets page (Storing large secrets).
- Removed unconfirmed claims: base64 wrapping and platform flags, pinentry-mode advice, runner temp directory lifetime and the masking-of-derived-values statement.
- The 36 KB figure is arithmetic from the 48 KB limit and Base64's one-third expansion.

Run 2026-11-01 with GnuPG 2.4.5 and GNU coreutils base64 on Windows (Git Bash), throwaway GNUPGHOME: `gpg --symmetric --cipher-algo AES256` writing `service-account.json.gpg`, `gpg --quiet --batch --yes --decrypt --passphrase=... --output` round trip (identical file back), base64 encode and `--decode` round trip, `base64 -w0` size. Not run: `gh secret set` and the GitHub Actions steps (documentation only).

Method: documentation plus commands run (GnuPG 2.4.5).
