---
id: computing-software.systems-network-administration.varnish-cache.varnishncsa-access-logs
name: varnishncsa-access-logs
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [varnishncsa, access-log, log-format, log-rate-limit]
level: practitioner
status: docs-checked
description: "Produce NCSA access logs from Varnish shared memory: combined format, -F formats, client and backend modes, the varnishncsa service, logrotate, -q filters and -R rate limit."
sources:
  - https://www.varnish.org/docs/tutorials/varnish-access-logs-varnishncsa/
  - https://www.varnish.org/docs/reference/varnishncsa/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# varnishncsa access logs

Web server logs show only misses and bypassed requests once Varnish caches in front. varnishncsa reads the shared memory log (VSL, a circular buffer in tmpfs, default 80MB, set by `vsl_space` or `varnishd -l`) and prints Apache/NCSA combined format, one line per Request transaction. Default format: `%h %l %u %t "%r" %s %b "%{Referer}i" "%{User-agent}i"`.

Modes:

- Client mode is default (`-c`), like a web server log. `-b` is backend mode (requests Varnish makes; client requests ignored unless `-c` is also given). With both, include `%{Varnish:side}x` (`b` or `c`) to tell them apart. In backend mode some fields change meaning (e.g. byte counters treat Varnish as the client).
- Piped requests (`return(pipe)`) are not logged in backend mode; in client mode `%{Varnish:handling}x` is `pipe`.
- Two instances can run, one per mode, logging to different files.

Format fields beyond the defaults: `-F` sets a format and `-f` reads it from a file. Useful items: `%D` (microseconds), `%T`, `%{X}t` strftime-style time, `%U` URL without query, `%q`, `%m`, `%{X}i` / `%{X}o` headers (optional `:first` or `:last` to account for VCL changes), and extended `%{X}x`: `Varnish:default_format`, `Varnish:hitmiss`, `Varnish:handling` (hit, hitmiss, hitpass, miss, pass, pipe, synth), `Varnish:time_firstbyte`, `Varnish:side`, `Varnish:vxid`, `VCL_Log:key` (set by `std.log("key:value")`) and `VSL:tag:prefix[field]`. `-j` makes output valid JSON, e.g. `varnishncsa -j -F '{"size": %b, "time": "%t", "ua": "%{User-Agent}i"}'`. Since 7.7, `%{X}i`/`%{X}o` no longer include header values set in VCL; use `VCL_Log`.

Hit/miss: on 7.5 or newer `varnishncsa -F "%{Varnish:default_format}x %{Varnish:handling}x"`; older versions need the full format spelled out.

Filters use VSL queries with `-q`: `-q "RespStatus >= 400 or BerespStatus >= 400"`; `-q "Timestamp:Resp[3] > 2.0 or RespStatus != 200"`; `-q "ReqHeader ~ '^Host: .*\.example.com'"`.

Service: official packages create `varnishncsa.service`, not enabled by default because the volume of log lines could overwhelm the system; enable only if the disk can keep up:

```bash
sudo systemctl enable varnishncsa
sudo systemctl start varnishncsa
```

It runs `/usr/bin/varnishncsa -a -w /var/log/varnish/varnishncsa.log -D` as user varnishlog and reloads with SIGHUP (which rotates the log in daemon mode). In unit files double every percent sign (`%%h`) in a `-F` format, or use `-f`. Packages also install `/etc/logrotate.d/varnish`: daily, rotate 7, compress, delaycompress, missingok, reloading the service after rotation.

Rate limiting: `-R limit[/duration]` suppresses transactions over the limit, e.g. `-R 1/10s` logs one line per ten seconds. Add it to ExecStart via `sudo systemctl edit --full varnishncsa`, then `sudo systemctl restart varnishncsa`.

## Checked

Method: 2026-11-08 docs-only read of the tutorial and the varnishncsa reference. The earlier flag list (-d "backlog", -w, -D) was only partly explained by the pages and has been dropped to the usage the pages show; added the hit/miss version split, query examples, JSON and the 7.7 header change. The tutorial's older-version format example has unescaped quotes; escape them yourself.
