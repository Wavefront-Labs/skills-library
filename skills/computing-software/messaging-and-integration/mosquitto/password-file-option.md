---
id: computing-software.messaging-and-integration.mosquitto.password-file-option
name: password-file-option
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [password-file, authentication, username-password]
level: practitioner
status: docs-checked
description: "Configure password_file for username and password authentication, including reload behaviour and the plugin recommendation."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: require valid MQTT usernames and passwords from a file.

`password_file file path` points at a file whose contents control client access. Create it with the mosquitto_passwd tool. If Mosquitto is compiled without TLS support, the file is plain text with lines `username:password` (the colon and password are optional but recommended).

```
password_file /path/to/passwd
allow_anonymous false
```

With `allow_anonymous false` only users in the file can connect. With `allow_anonymous true` and a password file, anonymous clients are allowed too, which with an `acl_file` can give read-only guest accounts.

Reload: the file is reloaded on the reload signal; the loaded username and password data is freed and re-read, and already connected clients are not affected.

The page suggests using the `mosquitto_password_file` plugin instead of this option, since plugins give more control over which listeners they apply to without the deprecated `per_listener_settings`. If `per_listener_settings` is true, the option applies to the current listener only; if false, to all listeners.

When certificate identity is used as the username (`use_identity_as_username` or `use_subject_as_username`), the password file is not used for that listener.

The docs warn to use network encryption with this option, otherwise the username and password are vulnerable to interception.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Claims unchanged; all match the page.
