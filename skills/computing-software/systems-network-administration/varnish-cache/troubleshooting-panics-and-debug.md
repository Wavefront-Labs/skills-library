---
id: computing-software.systems-network-administration.varnish-cache.troubleshooting-panics-and-debug
name: troubleshooting-panics-and-debug
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [panic-show, troubleshooting, debug-mode, stack-overflow]
level: advanced
status: docs-checked
description: "Diagnose Varnish problems: restart versus reload, panic.show for child crashes, varnishd -d, varnishlog queries for errors and passes, and backend health."
sources:
  - https://www.varnish.org/docs/tutorials/troubleshooting-varnish/
  - https://www.varnish.org/docs/tutorials/varnish-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# troubleshooting panics and debug

- Restart (`systemctl restart varnish`) kills varnishd and starts it again; runtime parameters not persisted in the systemd unit file are reset. Reload (`systemctl reload varnish`) runs the `varnishreload` script, which adds a new VCL and discards older ones; it does not touch the main or child processes.
- A child crash is a panic and the child is restarted. `varnishadm panic.show` returns only the last panic, so a later panic overwrites the one under investigation. The message, file, line number and backtrace are the clues.
- Debug mode: `varnishd -f default.vcl -d` runs the parent in the foreground with a CLI on stdin/stdout. The child is not started automatically; type `start` (without a child Varnish cannot serve requests). Stopping the parent also stops the child. Use it to keep a panic from being overwritten and to run `param.show`, `param.set`, `param.reset`, `stop`, `start`, `vcl.load`, `vcl.use`, `vcl.discard`. Not for production.
- Stack overflow: the panic text says `THIS PROBABLY IS A STACK OVERFLOW - check thread_pool_stack parameter`. Add 128k to `thread_pool_stack` and restart; if crashes stop, it is probably not a bug.

Guru Meditation pages come from the built-in `vcl_synth` (client side) and `vcl_backend_error` (backend side), and usually do not mean a Varnish fault. Find them in the log:

```bash
varnishlog -g request -q "VCL_call eq 'SYNTH'"
varnishlog -d -g request -q "VCL_call eq 'SYNTH' and RespStatus >= 400 and RespStatus < 500"
varnishlog -g request -q "VCL_call eq 'BACKEND_ERROR'"
varnishlog -g request -q "RespStatus == 503"
varnishlog -g raw -i Backend_health
```

`-d` dumps what is already in the VSL buffer (circular, 80 MB by default, set by `vsl_space`) and exits. In a backend error transaction the `FetchError` tag gives the reason, for example `Connection refused`.

Why a request was not cached:
- Pass: `varnishlog -q "VCL_call eq 'PASS'"`. The built-in VCL passes non-GET/HEAD methods, requests with a `Cookie` header and requests with an `Authorization` header.
- Unknown request method: piped (`VCL_return pipe`), find with `-q "VCL_return eq 'pipe'"`.
- Hit-For-Miss: `-q "HitMiss"`, or backend transactions with `-b -i TTL -q "TTL[6] eq 'uncacheable'"`. Causes the tutorial lists: zero TTL (`max-age=0`, `s-maxage=0`, past `Expires`), `Cache-Control` with private, no-cache or no-store, `Surrogate-Control: no-store`, a `Set-Cookie` response header, and `Vary: *`.

Probes from the monitoring tutorial:

```bash
varnishadm param.show                        # runtime parameters
varnishadm ban.list                          # ban expressions
varnishadm -- backend.list -p                # backend health
varnishlog -d -g request -q "Timestamp:Resp[2] > 1.0"       # slow client responses
varnishlog -d -g request -q "Timestamp:Beresp[2] > 1.0"     # slow backend responses
varnishlog -d -g request -q "Timestamp:Waitinglist[2] > 0.0"
varnishlog -d -g request -q "RespStatus ~ '^5' or Timestamp:Resp[3] > 10.0 or Error" -R 100/1m
varnishstat -1 -f 'MAIN.*'
```

`backend.list` shows only backends of the active VCL; use `varnishadm backend.list '*.*'` (quoted) for all.

## Checked
2026-11-08. Read in full: the troubleshooting tutorial and the monitoring tutorial. Confirmed: restart and reload, panic.show, debug mode, stack overflow advice, the log queries and the cacheability causes. Changed: removed `panic.clear` (not in these sources), corrected the 5xx query to the monitoring tutorial form, and added the Guru Meditation, pass and Hit-For-Miss queries.
Method: documentation only; no commands were run.
