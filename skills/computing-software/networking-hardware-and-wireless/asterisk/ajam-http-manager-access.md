---
id: computing-software.networking-hardware-and-wireless.asterisk.ajam-http-manager-access
name: ajam-http-manager-access
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, ajam, ami, http, manager-conf, rawman, mxml, web-access]
level: intro
status: docs-checked
description: "Reach AMI over HTTP with AJAM: enabled and webenabled in manager.conf, the built-in HTTP server in http.conf, and the manager, rawman and mxml URIs. Marked unsupported."
sources:
  - https://docs.asterisk.org/Configuration/Interfaces/Asterisk-Manager-Interface-AMI/Asynchronous-Javascript-Asterisk-Manager-AJAM/Allow-Manager-Access-via-HTTP/
  - https://docs.asterisk.org/Configuration/Interfaces/Asterisk-Manager-Interface-AMI/Asynchronous-Javascript-Asterisk-Manager-AJAM/Setting-up-the-Asterisk-HTTP-server/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AJAM (AMI over HTTP)
AJAM lets browsers and HTTP applications use the Asterisk Manager Interface. The docs warn it is **unsupported**, may be removed, and say to use standard TCP AMI instead.

`manager.conf`: set `enabled = yes` and `webenabled = yes`, optionally `httptimeout` (default HTTP timeout), and have a manager username and secret.

`http.conf` (the built-in mini HTTP server): `enabled=yes`; `enablestatic=yes` to serve static pages and scripts; adjust `bindaddr` and `bindport`; `prefix` must begin every URI (default blank).

Reload or restart, then `http show status` at the CLI lists the available URIs. Examples from the page, on port 8088:
- `/manager?action=login&username=foo&secret=bar` logs in to the HTML view and sets a cookie valid for `httptimeout`.
- `/rawman?action=status` returns raw manager output once logged in.
- `/mxml?action=status` returns the same as AJAX-style XML data.
- `/static/ajamdemo.html` is a demo page needing static content support and a `make install`; no external web server is needed.

A sample library, `astman.js`, helps build manager HTML interfaces.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Allow-Manager-Access-via-HTTP, Setting-up-the-Asterisk-HTTP-server) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
