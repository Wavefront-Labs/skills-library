---
id: computing-software.messaging-and-integration.mosquitto.acl-file-syntax
name: acl-file-syntax
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [acl-file, acl, topic-access, read-write-deny]
level: practitioner
status: docs-checked
description: "Write a Mosquitto acl_file with topic, user and deny lines to control per-client topic access."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restrict which topics each client can read or write using a static file.

`acl_file file path` sets the access control list file. If defined, only the topics listed have access. Lines have the form:

```
topic [read|write|readwrite|deny] <topic>
user <username>
```

The access type is optional (unless the topic contains a space); if omitted, access is read/write. Topics may contain the `+` and `#` wildcards as in subscriptions. `deny` explicitly denies a topic that a broader grant would allow, and all `deny` topics are handled before topics that grant read/write access.

The first set of topics, before any `user` line, applies to anonymous clients, assuming `allow_anonymous` is true. After a `user <username>` line, the following topic lines are specific to that user. The username is the same as in the password file, not the client id. Lines starting with `#` are comments.

Write access to the `$SYS` tree is generally not possible; the exception is `$SYS/broker/connection/+/state`.

Reload: on the reload signal the loaded ACLs are freed and reloaded, and existing subscriptions are affected after the reload.

The page suggests the `mosquitto_acl_file` plugin instead of this option. With `per_listener_settings` true the file applies to the current listener only.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Claims unchanged; all match the page.
