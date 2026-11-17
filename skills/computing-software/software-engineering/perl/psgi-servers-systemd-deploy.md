---
id: computing-software.software-engineering.perl.psgi-servers-systemd-deploy
name: psgi-servers-systemd-deploy
category: computing-software
field: software-engineering
product: perl
tags: [perl, starman, psgi, preforking, reverse-proxy, graceful-restart, psgi-servers-systemd-deploy]
level: practitioner
status: docs-checked
description: "Run a PSGI app under Starman: preforking workers, signals for graceful restart and worker count, sockets, Server::Starter and the reverse-proxy advice."
sources: ["https://metacpan.org/pod/Starman"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running a PSGI app with Starman

**Goal:** a managed preforking production server behind a front-end proxy.

```bash
starman                                       # run app.psgi with defaults
starman --workers 32 myapp.psgi
starman --listen /tmp/starman.sock            # UNIX domain socket
start_server --port 127.0.0.1:80 -- starman --workers 32 myapp.psgi   # under Server::Starter
starman --preload-app myapp.psgi              # preload for copy-on-write friendly memory
```
Full option list: `perldoc starman` (lower-case s); not read.

## Facts from the docs
- Preforking: spawns workers, reaps dead children and restarts the worker pool automatically.
- Signals: `HUP` graceful worker restart; `TTIN` / `TTOU` increase / decrease the worker count dynamically; `QUIT` graceful shutdown of workers.
- Server::Starter support gives hot deploy and graceful restarts. Can listen on multiple interfaces including UNIX sockets.
- HTTP/1.1 with chunked requests and responses, keep-alive and pipelining. UNIX only (no Win32).
- Memory: the page says the master needs a minimum of about 7MB and workers under 3MB; `--preload-app` enables copy-on-write friendly memory management.
- `psgix.informational` callback in the PSGI env sends an informational response such as 103 Early Hints: `$env->{'psgix.informational'}->(103, ["Link" => "</style.css>; rel=preload"])`.

## Deployment advice from the page
Because it is preforking, do not serve requests directly from the internet, especially with slow clients. Put Starman workers behind a frontend server such as nginx using an HTTP proxy over TCP or UNIX sockets.

## Self-check
- [ ] `kill -HUP` on the master restarts workers without dropping the listener, and the proxy still reaches the app.

## Checked
Method: 2026-11-08 read the full plain-text POD of Starman. The systemd unit file, Mojolicious (hypnotoad, morbo, prefork, MOJO_REVERSE_PROXY) and systemd documentation URLs were not read, so those parts of v1, plus the nginx header snippet, limits, logrotate, cron and perlpolicy advice, were removed. The page's benchmark numbers (a 2009 laptop) are deliberately not repeated.
