---
id: computing-software.networking-hardware-and-wireless.haproxy.config-sections-and-structure
name: config-sections-and-structure
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, global, defaults, frontend, backend, listen, config-sections]
level: practitioner
status: docs-checked
description: "Lay out haproxy.cfg sections (global, defaults, frontend, backend, listen), named defaults with from, and how settings are inherited."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# config sections and structure
A haproxy.cfg is a list of sections. `global` holds process-wide settings, `defaults` presets values for the proxy sections after it, `frontend` describes listening sockets accepting client connections, `backend` describes the servers connections are forwarded to, and `listen` is a complete proxy with frontend and backend in one section (generally useful for TCP-only traffic).

```
global
    log /dev/log local0
    maxconn 20000
defaults http_base
    mode http
    option httplog
    timeout connect 5s
    timeout client  30s
    timeout server  30s
frontend fe_web from http_base
    bind :80
    default_backend be_app
backend be_app from http_base
    server app1 10.0.0.11:8080 check
```
Rules worth knowing: `frontend`, `backend` and `listen` take their initial settings from the latest `defaults` section before them, unless the section line names one with `from <defaults_name>`. A `defaults` section resets all settings to the documented ones before presetting new ones, and it can itself take settings from another defaults with `from`. A defaults section referenced by name must have a unique name that follows proxy-name syntax; mixing explicit `from` use with implicit "latest defaults" use of the same section draws a warning. Options marked `(*)` in the keyword matrix can be inverted with `no`, for example `no option contstats`, and prefixed with `default` to restore the default regardless of earlier `defaults`. Proxy names may use letters, digits, `-`, `_`, `.` and `:`; a frontend and a backend may share a name.

Gotcha: a second `defaults` section resets everything for the proxies below it, so a proxy that "lost" its timeouts is usually under the wrong defaults.

Verify: `haproxy -c -V -f /etc/haproxy/haproxy.cfg` prints `Configuration file is valid` and lists any warnings.

## Checked
2026-11-03. Confirmed against configuration.html section 4 (Proxies: `from`, defaults reset and inheritance, naming rules) and section 4.1 (`no` prefix), and management.html for `-c -V`. Removed: the "2.4+ confirm" marker, the claim that a mode mismatch is rejected at check time, "warns about missing timeouts or modes", and the indentation/comment style remarks.
Method: documentation only; no commands were run.
