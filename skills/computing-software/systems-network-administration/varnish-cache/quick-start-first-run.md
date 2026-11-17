---
id: computing-software.systems-network-administration.varnish-cache.quick-start-first-run
name: quick-start-first-run
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [quick-start, backend-flag, default-vcl, first-vcl]
level: intro
status: docs-checked
description: "Start Varnish for the first time: start the service, point the default backend at your origin, use -b or -f and -a, and reload the VCL without restarting."
sources:
  - https://www.varnish.org/docs/tutorials/starting-varnish/
  - https://www.varnish.org/docs/users-guide/command-line/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# quick start first run

On a properly installed Linux system, `sudo systemctl start varnish` starts it. Browse to `http://127.0.0.1/` (or the server's address) to check. The default configuration forwards to a web application on the same machine, expected over HTTP on port 8080; if none is there Varnish gives the same generic Error 503 Service Unavailable whenever something is amiss.

Edit `/etc/varnish/default.vcl` (mostly comments); the live part is:

```vcl
vcl 4.1;
backend default {
    .host = "127.0.0.1";
    .port = "8080";
}
```

Change `.host` and `.port` to your origin (the page uses example.com port 80), then reload. The page writes the command as `systemctl varnish reload`, which is a typo; the form used elsewhere in the docs is `sudo systemctl reload varnish`. A reload loads the VCL without restarting the varnishd process; browsing again should show the origin's content.

Running varnishd directly, the only required argument is the backend:

- `-b host:port` is a quick start (e.g. `-b localhost:81`). A name may resolve to at most one IPv4 and one IPv6 address. It is exactly equivalent to a VCL containing `backend default { .host = "localhost:81"; }`.
- `-f file` is for your own VCL; the page presents `-b` and `-f` as alternatives.
- `-a [name=]address[,PROTO|,option=value,...]` defines one endpoint to serve HTTP on; repeat for several. Default `:80,http`. If a web server already uses port 80, move it to another port or a loopback address first. Addresses can be IPv4/IPv6 with port, a unix socket path or an abstract socket (`@name`); `name` is the `local.socket` name for VCL.

Packaged startup options live in `/etc/default/varnish` (Debian, Ubuntu), `/etc/sysconfig/varnish` (Red Hat, CentOS) or `/etc/rc.conf` (FreeBSD) per the command-line page, although the systemd tutorial says newer Varnish Software packages keep them in the service file instead.

## Checked

Method: 2026-11-08 docs-only read of both cited pages. Removed the earlier "use -b or -f, not both" wording (the page only says either); added the 503 behaviour and the reload command typo on the page; noted that option files are for older packaging.
