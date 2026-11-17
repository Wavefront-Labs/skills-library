---
id: computing-software.systems-network-administration.varnish-cache.runtime-parameters
name: runtime-parameters
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [param-set, param-show, read-only-params, varnishd-p]
level: practitioner
status: docs-checked
description: "Inspect and change varnishd runtime parameters with -p, param.show, param.set and param.reset, lock them with -r, and read the unit and flag conventions."
sources:
  - https://www.varnish.org/docs/reference/varnishd/
  - https://www.varnish.org/docs/users-guide/params/
  - https://www.varnish.org/docs/users-guide/run_cli/
  - https://www.varnish.org/docs/reference/varnish-cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# runtime parameters

Set at startup with `-p param=value` (repeatable), for example `varnishd -p default_ttl=3600 -p thread_pool_min=200 ...` (`-t TTL` is a shortcut for `default_ttl`; `-l` is shorthand for `vsl_space`). Change live through the CLI:

```bash
varnishadm param.show default_ttl
varnishadm param.show -l changed
varnishadm param.set prefer_ipv6 true
varnishadm param.reset default_ttl
```

- `param.show [-l|-j] [<param>|changed]`: `-l` adds documentation and minimum, maximum and default values, `-j` is JSON (only one of the two), `changed` lists only parameters whose value differs from the default. `param.set` and `param.reset` with `-j` return the same JSON as `param.show -j`.
- Most parameters take effect instantly or after a short delay, but a few need the child process restarted; each parameter's description says so. Flags in the reference: `delayed` (changes on the fly but not immediately), `restart` (worker must be stopped and restarted), `reload` (VCL must be reloaded), `experimental`, `wizard` (do not touch unless you really know what you are doing), `only_root`.
- Units: bool accepts `on`/`off`, `yes`/`no`, `true`/`false`, `enable`/`disable`. Bytes need a suffix `b`, `k`, `m`, `g`, `t`, `p` (1024-based, case-insensitive, an extra `b` is allowed: `32k` equals `32kb`). Durations take `ms`, `s`, `m`, `h`, `d`, `w`, `y`; timeouts and deadlines may accept `never` to disable.
- Lock parameters with `-r name[,name]` so the CLI cannot change them. The manual suggests considering `cc_command`, `vcc_allow_inline_c` and `vmod_path`, which can be used to escalate privileges from the CLI (`vcc_allow_inline_c` is now a deprecated alias for a `vcc_feature` setting).
- List parameters take `+`/`-` items, for example `feature` (default `none,+validate_headers,+vcl_req_reset`): `varnishadm param.set feature +http2`. `vcc_feature` defaults to `none,+err_unref,+unsafe_path`.
- On 32-bit systems some defaults and maximums are reduced (for example `workspace_client` 24k).
- `-x parameter` prints the parameter documentation.
- The project advises not to tweak parameters unless you are sure of what you are doing; the defaults suit most workloads. Reasons to change them include performance tuning and security configuration.

## Checked
2026-11-08. Read in full: the varnishd manual and parameter list, the Users Guide parameters page, the CLI guide and the varnish-cli reference. Confirmed: set methods, units, flags, `-r`, feature defaults and the notes above. Removed: nothing substantive was wrong; the `-r` list is expanded with the manual's own wording.
Method: documentation only; no commands were run.
