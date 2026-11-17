---
id: computing-software.cryptography-implementation.key-management.keeping-keys-out-of-code-and-logs
name: keeping-keys-out-of-code-and-logs
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-storage, secret-storage, hardcoded-keys, secret-scanning, gitleaks, trufflehog, environment-variables, cwe-321, secret-rotation]
level: practitioner
status: draft
description: "Find and remove hardcoded keys (CWE-321), choose between env vars, mounted files and secret managers, keep keys out of logs and dumps, and respond when one leaks."
sources: ["https://cwe.mitre.org/data/definitions/321.html", "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html", "https://github.com/gitleaks/gitleaks", "https://docs.github.com/en/code-security/secret-scanning"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Keeping keys out of code, config and logs

Hardcoded keys (CWE-321) are the most common key compromise: a constant in
source, a key in a sample config, a private key committed "temporarily".
Once in git history, assume it is public.

## Find them

```bash
gitleaks detect --source . --log-opts="--all"          # whole history
trufflehog git file://. --only-verified                # verifies live creds
rg -n -i '(BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY|aes_?key\s*=|secret_?key\s*=|SecretKeySpec\(".+"\.getBytes)' .
```

Enable push protection (GitHub secret scanning, GitLab secret detection) and a
pre-commit hook (`gitleaks protect --staged`).

## Where keys should live, in order of preference

1. **Never in the app at all**: KMS/HSM does the crypto (`Encrypt`, `Sign`),
   the app holds only an IAM identity.
2. **Secret manager fetched at runtime** (AWS Secrets Manager, GCP Secret
   Manager, Vault) via workload identity; cached in memory.
3. **Mounted file** from the orchestrator (Kubernetes Secret volume, systemd
   `LoadCredential=`), mode 0400, tmpfs.
4. **Environment variable**: acceptable for low-value secrets; leaks via
   `/proc/<pid>/environ` to same-user processes, crash reporters, child
   processes, `docker inspect`, and debug pages that dump env.

Never: source code, container image layers (`docker history` shows them),
client-side code (mobile apps, JS bundles - assume extracted), CI logs.

## Keep them out of logs and dumps

- Wrap secrets in types that redact on print (`SecretStr` in pydantic,
  `secrecy::Secret` in Rust, custom `toString()` returning `***`).
- Scrub request/response logging of `Authorization`, cookies, key fields.
- Disable core dumps for key-holding processes (`prctl(PR_SET_DUMPABLE,0)`,
  `LimitCORE=0`) and exclude them from crash reporters.
- Error messages must not include key material or decrypted data.

## When one leaks

1. Rotate first (new key live), then revoke/disable the old one. Removing the
   commit does not un-leak it.
2. Re-encrypt or re-sign anything that matters under the new key.
3. Check access logs for use of the old key.
4. Purge history (`git filter-repo`) only to reduce future exposure.

## Verify

- [ ] Secret scanner runs in CI and pre-commit; history scan clean or leaks rotated.
- [ ] Image layers (`docker history --no-trunc`, `dive`) contain no keys.
- [ ] Log sample after a failing request shows no secrets.
