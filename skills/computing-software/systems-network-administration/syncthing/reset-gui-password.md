---
id: computing-software.systems-network-administration.syncthing.reset-gui-password
name: reset-gui-password
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, gui-password, generate, authentication]
level: intro
status: docs-checked
description: "Reset a lost Syncthing GUI password with syncthing generate --gui-user and --gui-password while the service is stopped."
sources: ["https://docs.syncthing.net/users/faq.html", "https://docs.syncthing.net/users/syncthing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resetting the GUI password

## Steps
1. Stop Syncthing; the FAQ says this should be done while Syncthing is not running.
2. Run:

```sh
syncthing generate --gui-user=newUserName --gui-password=newPassword
```
3. Start Syncthing again.

## Details
- A plaintext password is hashed before writing to the config file; an already bcrypt-hashed input is stored verbatim. Giving the existing password hash leaves it untouched.
- `--gui-password=-` reads the password from the standard input stream.
- `generate` takes the common options `--home`, or `--config` together with `--data`, to select the configuration.
- `generate` leaves an existing device certificate untouched and, if the config file exists, validates it and updates it to the latest schema, adding defaults for new options.

```sh
printf '%s' "$NEW_PW" | syncthing generate --gui-password=-
```

## Related settings
In the config's gui element, `user` is set to require authentication and `password` holds the bcrypt hash. If `authMode` is not present, the authentication mode (static) is controlled by the presence of the user/password fields. LDAP is enabled by setting the authentication mode to `ldap` (see the ldap-authentication skill).

## Checked
2026-11-04. Read the FAQ entry on resetting the GUI password and Command Line Operation (generate options, subcommand description) plus the config page gui element: command, offline requirement, hashing behaviour, stdin form, certificate and schema behaviour, and `authMode`. Removed the `syncthing cli operations shutdown` stop command and the shell-history claim, which the pages do not state.
Method: documentation only; no commands were run.
