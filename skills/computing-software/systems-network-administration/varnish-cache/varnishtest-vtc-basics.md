---
id: computing-software.systems-network-administration.varnish-cache.varnishtest-vtc-basics
name: varnishtest-vtc-basics
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [varnishtest, vtc, test-case, regression-testing]
level: practitioner
status: docs-checked
description: "Test VCL with varnishtest: the vtc file layout of varnish, server and client agents, expect assertions, and options like -j -n -k -D -p."
sources:
  - https://www.varnish.org/docs/tutorials/testing-varnish-varnishtest/
  - https://www.varnish.org/docs/tutorials/hands-on-varnishtest/
  - https://www.varnish.org/docs/reference/varnishtest/
  - https://www.varnish.org/docs/reference/vtc/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# varnishtest vtc basics

A VTC file starts with `varnishtest "description"`, one command per line, `#` comments, double-quoted or `{...}` multi-line strings, and macros like `${s1_sock}`. Agent names start with the agent letter: `s1`, `c1`, `v1`.

```
varnishtest "cache a response"
server s1 {
    rxreq
    expect req.url == "/foo"
    txresp -body "hello"
} -start
varnish v1 -vcl+backend {
    sub vcl_backend_response { set beresp.ttl = 10m; }
} -start
client c1 {
    txreq -url "/foo"
    rxresp
    expect resp.status == 200
} -run
```

`-start` launches, `-wait` waits, `-run` is start plus wait. `shell { ... }` runs a multi-line shell script and the test fails if any command in it exits non-zero. `-vcl+backend` adds the backend definition to the VCL you give. Macros such as `${s1_sock}` (the address of server s1, which clients connect to by default) and `${pwd}` are replaced before the shell runs.

```bash
varnishtest test.vtc
varnishtest -j 3 -n 5 -k -q test1.vtc test2.vtc
varnishtest -D name=Varnish test.vtc       # ${name} macro
```

Other options: `-b` internal buffer size (default 1 MB), `-i` overrides the PATH and vmod_path used to find binaries and VMODs, `-p name=val` passes varnishd parameters to every varnishd started (for example `-p vmod_path=...` to test a VMOD build), `-t` timeout of the test run (default 60 seconds), `-v` verbose, `-q` shows only failures. A failing test prints verbose output explaining what happened. Temporary `vtc.*` directories go in TMPDIR if set, otherwise in /tmp. The Varnish source tree keeps its regression tests under `bin/varnishtest/tests/`; their names look like `b00012.vtc` (basic functionality) and `v00032.vtc` (VCL).

## Checked
2026-11-08: Read in full the varnishtest manual page. Read the options, file-naming and shell sections of the varnishtest tutorial, the macros/shell/multi-line sections of the hands-on tutorial and the shell entry of the VTC reference; the rest of those pages was not read. Confirmed the layout, `-start`/`-wait`/`-run`, options `-b -D -i -j -k -n -p -q -t -v`, the 60 s default, 1 MB buffer, shell behaviour and macros. Removed: the Docker command (not on any cited page) and the claim that tests use names like `b00001.vtc` (the documented examples are `b00012.vtc` and `v00032.vtc`).
Method: documentation only; no commands were run.
