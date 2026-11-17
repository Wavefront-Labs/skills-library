---
id: computing-software.devops-ci-cd.turborepo.remote-caching-artifact-signatures-hmac
name: remote-caching-artifact-signatures-hmac
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, remote-cache, artifact-signing, hmac-sha256, remotecache-signature, turbo-remote-cache-signature-key, integrity, authenticity, cache-miss]
level: advanced
status: docs-checked
description: "Enable HMAC-SHA256 signing of remote cache artifacts with remoteCache.signature and TURBO_REMOTE_CACHE_SIGNATURE_KEY; failed verification is a cache miss."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/core-concepts/remote-caching.mdx
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo can sign artifacts with a secret key before uploading them to the Remote Cache, using `HMAC-SHA256` signatures with a key you provide. When artifacts are downloaded it verifies their integrity and authenticity; any artifact that fails to verify is **ignored and treated as a cache miss**.

Enable in `turbo.json`:

```jsonc
{
  "remoteCache": {
    "signature": true
  }
}
```

then declare the secret in the environment variable `TURBO_REMOTE_CACHE_SIGNATURE_KEY`.

The configuration reference adds detail. With `remoteCache.signature` set to true, Turborepo signs every uploaded artifact with the value of `TURBO_REMOTE_CACHE_SIGNATURE_KEY` and rejects any downloaded artifact that has an invalid or missing signature. The docs state this is not a security feature; it verifies the integrity of a cached artifact, as a defence-in-depth measure against events like partial uploads or downloads, or issues in the Remote Cache server itself. Turborepo tries to handle those situations natively where it can. The `futureFlags.longerSignatureKey` flag enforces a minimum key length of 32 bytes, because short keys weaken the HMAC-SHA256 signature and make brute-force tag collision feasible; short keys will be rejected in a future major version. When that flag is on and the key is too short, Turborepo fails at the start of the run with an error giving the key length and the minimum.

## Checked

2026-11-04. Read the Artifact Integrity section of the Remote Caching page and the `signature` and `futureFlags.longerSignatureKey` entries of the configuration reference. Signing, `HMAC-SHA256`, miss-on-failure, the env var, defaults and the 32-byte flag match. Removed the invented Verify step.

Method: documentation only; no commands were run.
