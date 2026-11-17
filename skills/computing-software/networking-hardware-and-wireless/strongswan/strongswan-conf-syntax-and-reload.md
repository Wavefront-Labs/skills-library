---
id: computing-software.networking-hardware-and-wireless.strongswan.strongswan-conf-syntax-and-reload
name: strongswan-conf-syntax-and-reload
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, strongswan-conf, section-references, reload, strongswan-d]
level: practitioner
status: docs-checked
description: "strongswan.conf and swanctl.conf file syntax including section references for inheritance, the strongswan.d split, STRONGSWAN_CONF override and reloading via SIGHUP or swanctl."
sources:
  - https://docs.strongswan.org/docs/latest/config/strongswanConf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# strongswan conf syntax and reload
`strongswan.conf` (usually `/etc/strongswan.conf`) is the shared configuration file for all strongSwan components; `swanctl.conf` uses the same format. The default file may be split into `strongswan.d` in the sysconfdir. Set `STRONGSWAN_CONF` to read another location.

Grammar:

```
settings := (section|keyvalue)*
section  := name { settings }
keyvalue := key = value\n
```

Values end at a newline; `#` starts a comment; indentation is optional. Names and keys may not contain `. , : { } = " #`, newline, tab or space.

**Section references.** A section may inherit another's settings and subsections:

```
section    := name : references { settings }
references := absname[, absname]*
```

```
connections {
  conn-a : conn-defaults, eap-defaults {
    children { child-a : child-defaults { } }
  }
  conn-c : connections.conn-a { }
}
```

Values may be overridden in the section (an empty assignment clears a value so its default applies). Inherited settings follow those defined locally, and multiple references enumerate left to right. References are evaluated at runtime, so forward references and included files work. The page says this is available since 5.7.0.

**Reloading.** charon reloads strongswan.conf on SIGHUP (sent manually), the vici `reload-settings` call, or `swanctl --reload-settings`. This reloads the logger settings and plugins that support it (attr, pkcs11, eap-radius); many settings are read live. Consult the strongswan.conf(5) man page of your release for the options it actually has.

## Checked
2026-11-04. Confirmed against the strongSwan strongswan.conf page: location and strongswan.d, STRONGSWAN_CONF, grammar, forbidden characters, section references since 5.7.0, SIGHUP, reload-settings and swanctl --reload-settings. Nothing removed.

Method: documentation only; no commands were run.
