---
id: computing-software.systems-network-administration.rclone.rclone-global-flags-in-remote-config
name: rclone-global-flags-in-remote-config
category: computing-software
field: systems-network-administration
product: rclone
tags: [override-var, global-var, remote-config, no-check-certificate]
level: advanced
status: docs-checked
description: "Use override.var and global.var in a remote section or connection string to scope or set global flags per remote."
sources: ["https://rclone.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A remote section or connection string can carry global flags that are applied just before the remote is created.

## override.var

`override.var` changes a global setting only for the creation of that remote. The flag name loses its `--`, has `-` replaced by `_` and gains the `override.` prefix.

```ini
[remote]
type = XXX
override.no_check_certificate = true
```

The same works in a connection string: `remote,override.no_check_certificate=true:` or the shorthand `remote,override.no_check_certificate:`. This is how to relax certificate checking for one test server without affecting every other remote in the command. The docs list globals that make sense as overrides: `bind_addr`, `ca_cert`, `client_cert`, `client_key`, `connect_timeout`, `disable_http2`, `disable_http_keep_alives`, `dump`, `expect_continue_timeout`, `headers`, `http_proxy`, `low_level_retries`, `max_connections`, `no_check_certificate`, `no_gzip`, `timeout`, `traffic_class`, `use_cookies`, `use_server_modtime` and `user_agent`. It overrides every other config method but only while the remote is built.

## global.var

`global.var` sets a global variable for everything, exactly like the command-line flag, and is used for settings such as sync options that cannot be overrides.

```ini
[remote]
type = XXX
global.checksum = true
```

This is equivalent to passing `--checksum` on every command that instantiates the remote. If two remotes set the same global, the later one instantiated wins. Because it affects all uses of rclone, reserve it for flags you truly always want with that remote.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
