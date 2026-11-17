---
id: computing-software.messaging-and-integration.mosquitto.mosquitto-passwd-usage
name: mosquitto-passwd-usage
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [mosquitto-passwd, password-file, user-management]
level: intro
status: docs-checked
description: "Create, update and delete users in a Mosquitto password file with mosquitto_passwd, including batch mode."
sources:
  - https://mosquitto.org/man/mosquitto_passwd-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage a password file from the command line.

Synopsis:
```
mosquitto_passwd [ -H hash ] [ -c | -D ] passwordfile username
mosquitto_passwd [ -H hash ] -b passwordfile username password
mosquitto_passwd -U passwordfile
```

Options:
- `-c` creates a new file. If the file exists it is overwritten. A filename of `-` writes to stdout, which only really makes sense with `-b`.
- `-D` deletes the named user.
- `-b` batch mode: the password is given on the command line. The page warns it will be visible on the command line and in command history.
- Without `-c`, the user is added to the file or the password is updated.

Examples from the page:
```
mosquitto_passwd -c /path/to/passwd ral
mosquitto_passwd /path/to/passwd ral
mosquitto_passwd -b /path/to/passwd ral PASSWORD
mosquitto_passwd -D /path/to/passwd ral
```

Usernames must not contain `:`. Passwords are stored in a format similar to crypt(3). The tool returns zero on success, non-zero on error.

Environment: `MOSQUITTO_UNSAFE_ALLOW_SYMLINKS`. By default sensitive files whose path includes a symbolic link are refused; setting this variable to any value allows loading through symlinks, which the page says could expose you to symlink attacks.

## Checked

2026-11-08. Confirmed against the mosquitto_passwd man page: synopsis, -b/-c/-D behaviour and warnings, the colon restriction, crypt(3)-like storage, exit status and MOSQUITTO_UNSAFE_ALLOW_SYMLINKS. Claims unchanged; the page examples use /etc/mosquitto/passwd where the skill uses a placeholder path.

Method: documentation only; no commands were run.
