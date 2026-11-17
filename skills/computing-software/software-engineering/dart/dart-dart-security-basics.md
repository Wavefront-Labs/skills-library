---
id: computing-software.software-engineering.dart.dart-dart-security-basics
name: dart-dart-security-basics
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-security, dart-security-basics]
level: practitioner
status: docs-checked
description: "Dart security basics: keep SDK and dependencies current, use Random.secure for tokens, report vulnerabilities."
sources: ["https://dart.dev/security", "https://dart.dev/libraries/dart-math", "https://dart.dev/tools/pub/security-advisories"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure Dart projects
- Keep current with the latest Dart SDK releases and check the changelog for security fixes.
- Keep dependencies up to date; avoid pinning exact versions, and if you pin, check periodically for security updates. `dart pub outdated` lists upgradable packages.
- The default `Random` is not cryptographically secure; use `Random.secure()` for tokens and keys.
- Report a vulnerability in Dart itself at the address given on the security page (g.co/vulnz); the page states the project has no bug bounty program.
- Pub security advisories: `ignored_advisories` in a pubspec only affects the root package.
Verify: `dart pub outdated` shows no stale dependencies.

## Checked
2026-11-03. Confirmed against dart.dev security (best practices, reporting, no bug bounty), libraries/dart-math (`Random.secure()`) and tools/pub/security-advisories (`ignored_advisories` root only). Removed: TLS default certificate and `badCertificateCallback` claims, password hashing advice, pub points review advice, compile-time secrets claim (not on the pages read).
Method: documentation only; no commands were run.
