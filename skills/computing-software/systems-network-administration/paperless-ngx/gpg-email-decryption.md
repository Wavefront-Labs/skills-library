---
id: computing-software.systems-network-administration.paperless-ngx.gpg-email-decryption
name: gpg-email-decryption
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, gpg, encrypted-email, gpg-agent, paperless-enable-gpg-decryptor, gnupg]
level: advanced
status: docs-checked
description: "Decrypt GPG-encrypted emails before Paperless-ngx consumes them by mounting the gpg-agent socket and public keyring into the container."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decrypting GPG-encrypted email

## Requirements
`gpg-agent` 2.1.1 or newer on the host, already set up to decrypt your mail. Prove it works first:
```bash
gpg --encrypt --armor -r person@example.com name_of_file
gpg --decrypt name_of_file.asc
```

## Enable
Set `PAPERLESS_ENABLE_GPG_DECRYPTOR=true`.

## Docker
Find the agent socket and keyring on the host:
```bash
gpgconf --list-dir agent-socket
```
Mount both into the container:
```yaml
webserver:
  volumes:
    - /path/to/.gnupg/pubring.gpg:/usr/src/paperless/.gnupg/pubring.gpg
    - <path to gpg-agent socket>:/usr/src/paperless/.gnupg/S.gpg-agent
```

## Bare metal
No further configuration is needed. To use a separate keyring directory, set `PAPERLESS_EMAIL_GNUPG_HOME`.

## Troubleshooting
- Confirm `gpg-agent` is running on the host.
- Confirm the `gpg` encrypt and decrypt commands work from inside the container.
- Check permissions in `/usr/src/paperless/.gnupg`. The directory should be `drwx------` and the socket and keyring `-rw-------` or `srw-------`, owned by the paperless user.

## Checked
2026-11-04. Compared with Decryption of encrypted emails before consumption in advanced usage and the GPG settings in configuration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: requirements and test commands, enabling variable, socket lookup, Docker mounts, bare metal note and GNUPG_HOME variable, troubleshooting and permissions. Removed: closing paragraph about mail rules, PDFs and the Password Removal action (not on the page).

Method: documentation only; no commands were run.
