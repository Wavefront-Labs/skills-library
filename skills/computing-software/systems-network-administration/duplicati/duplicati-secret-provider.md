---
id: computing-software.systems-network-administration.duplicati.duplicati-secret-provider
name: duplicati-secret-provider
category: computing-software
field: systems-network-administration
product: duplicati
tags: [secret-provider, secret-provider-pattern, default-secret-provider, wincred, keychain, libsecret]
level: advanced
status: docs-checked
description: "Keep passwords out of Duplicati's configuration by using placeholders resolved from a secret provider, including the OS default providers and custom placeholder patterns."
sources: ["https://docs.duplicati.com/security-and-secrets/using-the-secret-provider"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Using the Duplicati secret provider

The secret provider (since Duplicati 2.0.9.109) reduces password leaks by not storing passwords inside Duplicati. One option enables it: `--secret-provider=<url>`. Then write placeholders where secrets belong, in the destination URL or in options:

`duplicati backup s3://example-bucket?auth-username=$s3-user&password=$s3-pass --passphrase=$passphrase`

Duplicati finds the `$`-prefixed keys, asks the provider for the real values and substitutes them in memory only, never writing the keys to disk. Every requested key must exist in the provider or the operation fails with a message naming the missing key, so you never run with a placeholder or empty string by accident.

For the TrayIcon, Agent or Server add `--secret-provider=url` to their command lines, or set it in the UI settings (remember to click Save settings).

Default provider: from Duplicati 2.3 the Server, TrayIcon and Agent use an operating system provider even when `--secret-provider` is not set: Windows Credential Manager (`wincred://`), macOS Keychain (`keychain://`), and on Linux `libsecret://` if installed and a default collection exists, otherwise none. It stores secrets Duplicati creates itself, most importantly the key that encrypts the server database. If `--secret-provider` points at a provider that can store secrets, that one is used instead.

Placeholder pattern: if legitimate values start with `$`, set `--secret-provider-pattern`. The pattern is a prefix, optionally with braces around the key, so `--secret-provider-pattern=!secret{}` makes `!secret{backup-passphrase}` resolve to the secret `backup-passphrase`.

## Checked

2026-11-04. Confirmed against the Using the secret provider page (now at /security-and-secrets/using-the-secret-provider). Replaced the dead source URL (404) with the current page.

Method: documentation only; no commands were run.
