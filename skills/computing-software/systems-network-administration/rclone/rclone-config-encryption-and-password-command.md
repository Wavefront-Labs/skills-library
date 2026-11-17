---
id: computing-software.systems-network-administration.rclone.rclone-config-encryption-and-password-command
name: rclone-config-encryption-and-password-command
category: computing-software
field: systems-network-administration
product: rclone
tags: [config-encryption, rclone-config-pass, password-command, secretbox]
level: practitioner
status: draft
description: "Encrypt rclone.conf with a configuration password and supply it non-interactively via environment or a password command."
sources: ["https://rclone.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
The config file holds cloud credentials, so keep it in a protected location. If you cannot, set a configuration password from `rclone config` (option `s`, Set configuration password), or with `rclone config encryption set`, `remove` and `check`. Every rclone start then needs the password. The config is encrypted with NaCl secretbox (XSalsa20 plus Poly1305); the password is SHA-256 hashed to make the key and the hash is not stored. There is no way to recover the configuration if the password is lost, and the docs advise against publishing an encrypted config unless the password is very strong.

## Supplying the password

- `RCLONE_CONFIG_PASS` in the environment. For interactive sessions, source a small script that does `read -s RCLONE_CONFIG_PASS; export RCLONE_CONFIG_PASS`.
- `--password-command` (or `RCLONE_PASSWORD_COMMAND`), a program that prints the password on standard output. Give it a fully specified path and do not rely on environment variables inside it.

```console
export RCLONE_PASSWORD_COMMAND="pass rclone/config"
```

The value is a space-separated command parsed as CSV: quote an argument containing spaces with `"`, double a literal `"`, and quote the executable path too if it has spaces, as in `'"/path with a space/get-password.sh"'`. When you change the config password rclone sets `RCLONE_PASSWORD_CHANGE=1` for the command, so a script can tell initial decryption from setting a new password.

Because the file is rewritten when OAuth tokens refresh, the process needs write access and the password at every refresh. A crypt remote's own password is only lightly obscured in the file, so config encryption is what actually protects it.
