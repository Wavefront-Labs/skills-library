---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-status-monitoring
name: mod-status-monitoring
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-status, server-status, extendedstatus, monitoring, balancer-manager]
level: practitioner
status: docs-checked
description: "Expose the server-status page with SetHandler, restrict it, use ?auto and ?refresh, ExtendedStatus, and troubleshoot busy processes."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_status.html
  - https://httpd.apache.org/docs/2.4/programs/apachectl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_status
```apache
<Location "/server-status">
    SetHandler server-status
    Require host example.com
</Location>
```
Restrict access to trusted hosts. Browse to `/server-status`.

- `?refresh=N` reloads every N seconds.
- `?auto` gives plain text for scripts such as `log_server_status` in `/support`.
- `ExtendedStatus On` enables the lines marked `(*)` on the page (bytes, CPU, current hosts and requests); loading mod_status toggles it on by default as of 2.3.6.

It shows busy and idle workers, per-worker requests and bytes, uptime, requests per second and CPU.

## Troubleshooting load
1. Enable `ExtendedStatus`.
2. Use `top` to find heavy processes.
3. Reload server-status and match their PIDs to requests and clients (requests are transient; retry).

## Security
Once loaded, the handler is available in all configuration files including `.htaccess`.

## Related
- `apachectl fullstatus` shows a full report from mod_status (needs a text browser such as lynx; the URL is set by `STATUSURL` in the script); `apachectl status` is the same without the list of current requests.

## Checked

2026-11-08. Handler config, refresh and auto query strings, ExtendedStatus behaviour, troubleshooting steps and the .htaccess warning confirmed on the full mod_status page; apachectl status and fullstatus confirmed on the apachectl page. Removed balancer manager, MDServerStatus and event-MPM column claims that no cited page supports.

Method: documentation only; no commands were run.
