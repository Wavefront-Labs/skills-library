---
id: computing-software.devops-ci-cd.turborepo.turbo-json-future-flags-hashing-logs-and-prune
name: turbo-json-future-flags-hashing-logs-and-prune
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, futureflags, hashfilepermissions, errorsonlyshowhash, longersignaturekey, pruneincludesglobalfiles, github-base-ref-fallback]
level: advanced
status: docs-checked
description: "Future flags for hashing executable bits, showing hashes with errors-only logs, 32-byte signature keys, prune copying globalDependencies, and GitHub base ref fallback."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Future flags (root `turbo.json` only, default `false`):

- **`hashFilePermissions`**: include executable permission in file hashes for task inputs and global dependencies. On Unix a regular file is executable if any owner, group or other executable bit is set; on Windows regular files are non-executable; symlink permissions and read or write bits do not matter. Enabling it changes all task hashes, so existing cache entries are not reused.
- **`errorsOnlyShowHash`**: with `outputLogs: "errors-only"`, show hashes at start and completion. Messages: `cache miss, executing <hash> (only logging errors)` and `cache hit, replaying logs (no errors) <hash>`.
- **`longerSignatureKey`**: with `remoteCache.signature` enabled, require `TURBO_REMOTE_CACHE_SIGNATURE_KEY` of at least 32 bytes. HMAC-SHA256 accepts any length but keys shorter than 32 bytes weaken the signature and make brute-force tag collision feasible. Turborepo fails at the start of the run with the key length and the minimum when the key is too short.
- **`pruneIncludesGlobalFiles`**: copy files matching `globalDependencies` globs into the `turbo prune` output. Without it the entries remain in the pruned `turbo.json` but the files (for example a root `tsconfig.json`) are not copied, so tasks may behave differently. Both inclusion and `!` exclusion globs work; `turbo prune frontend` then includes `tsconfig.json`.
- **`githubActionsRemoteBaseRefFallback`**: when GitHub Actions reports a PR base branch not present as a local ref, fall back to `origin/<branch>`, supporting detached `actions/checkout` checkouts. Local refs still win, and `TURBO_SCM_BASE` and default `main` or `master` resolution are unchanged.

## Checked

2026-11-04. Read the `futureFlags` section of the configuration reference for `hashFilePermissions`, `errorsOnlyShowHash`, `longerSignatureKey`, `pruneIncludesGlobalFiles` and `githubActionsRemoteBaseRefFallback` in full; defaults, messages and behaviours match. Removed the invented Verify step.

Method: documentation only; no commands were run.
