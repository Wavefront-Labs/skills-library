---
id: computing-software.networking-hardware-and-wireless.bind9.rndc-conf-and-keys
name: rndc-conf-and-keys
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, rndc-conf, rndc-confgen, hmac]
level: practitioner
status: docs-checked
description: "Set up rndc.conf and rndc.key for BIND 9: options, key and server blocks, rndc-confgen -a, and rndc command-line flags."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter4.html
  - https://bind9.readthedocs.io/en/latest/manpages.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rndc conf and keys
`rndc` reads `/etc/rndc.conf`, falling back to `/etc/rndc.key`. `rndc-confgen -a` writes `rndc.key`.

`rndc.conf` holds `options` (`default-server`, `default-key`, `default-port`, source addresses), `key` blocks and `server` blocks.

```
key rndc_key {
    algorithm hmac-sha256;
    secret "base64-secret";
};
```

Key algorithms: hmac-md5, hmac-sha1, hmac-sha224, hmac-sha256, hmac-sha384, hmac-sha512.

Command-line overrides: `-c` config file, `-k` key file, `-s` server, `-p` port, `-y` key name, `-q` quiet, `-r`, `-t`, `-V` verbose.

The same secret must appear in `named.conf` as a `key` block referenced from `controls`.

## Checked

2026-11-04. Read the rndc.conf section of the Administrator Reference Manual and the rndc and rndc-confgen man pages: default files, options and key/server blocks, algorithm names and the command-line flags confirmed. Removed an unconfirmed truncated-algorithm clause.

Method: documentation only; no commands were run.
