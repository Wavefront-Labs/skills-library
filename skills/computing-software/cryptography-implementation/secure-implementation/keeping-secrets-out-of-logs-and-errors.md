---
id: computing-software.cryptography-implementation.secure-implementation.keeping-secrets-out-of-logs-and-errors
name: keeping-secrets-out-of-logs-and-errors
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, error-oracle, secret-logging, redaction, cwe-532]
level: practitioner
status: docs-checked
description: "Keep keys, tokens and passwords out of logs and error messages: what OWASP says to exclude, redacting secret types, and protecting log files."
sources: ["https://cwe.mitre.org/data/definitions/532.html", "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html", "https://docs.pydantic.dev/latest/api/types/", "https://docs.rs/secrecy/latest/secrecy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keeping secrets out of logs and errors

Logs are copied to more places, kept longer and read by more people than any key store.
CWE-532 describes the weakness as the product writing sensitive information to a log file,
and notes that logs give attackers a less-protected path to the data.

## What not to log

The OWASP Logging Cheat Sheet says these should usually not be recorded directly, but
removed, masked, sanitized, hashed or encrypted:

- session identification values (consider a hashed value if needed to track session events)
- access tokens
- sensitive personal data and some PII
- authentication passwords
- encryption keys and other primary secrets
- commercially sensitive information

Also from the cheat sheet: sanitize event data against log injection (CR, LF and delimiter
characters), protect logs from tampering and unauthorized access, and consider excluding,
masking or hashing parts of data during examination or extraction.

## Make leaking hard by type

- Python: pydantic `SecretStr` (and the generic `Secret` types) display as masked asterisks
  when printed or serialized and expose the real value only through `get_secret_value()`.
- Rust: `secrecy::SecretBox` aims to prevent accidental leakage through channels such as debug
  logging, makes access explicit via `ExposeSecret`, and does not implement `Serialize` by default.

## CWE-532 mitigations

- Consider seriously the sensitivity of what is written to log files; do not write secrets.
- Remove debug log files before deploying to production.
- Protect log files against unauthorized read and write.
- Error messages that echo query or system details also leak (the CWE-532 example shows an
  SQL error exposing table and column names).

## Verify

- [ ] Secret-holding types redact in print, logging and JSON output (unit test).
- [ ] Production log configuration has no debug output that prints keys, tokens or request secrets.
- [ ] Log files have access controls.

## Checked

Method: docs-checked 2026-11-09 against CWE-532 (description, mitigations, examples), OWASP Logging Cheat Sheet (data to exclude, sanitization and protection sections), pydantic types API page (Secret/SecretStr masking and get_secret_value), docs.rs/secrecy. Removed: Java, Kotlin and Go redaction patterns, field-name and regex scrubbing lists, Sentry, APM and tracing advice, SSLKEYLOGFILE, javax.net.debug and other debug switch claims, and the secret-scanner canary steps, none of which the read sources state.
