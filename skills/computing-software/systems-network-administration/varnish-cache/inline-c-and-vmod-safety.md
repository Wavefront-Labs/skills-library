---
id: computing-software.systems-network-administration.varnish-cache.inline-c-and-vmod-safety
name: inline-c-and-vmod-safety
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [inline-c, vcc-feature, vmod-path, unsafe-path]
level: advanced
status: docs-checked
description: "Limit what VCL authors can do: inline C is off by default, restrict VMOD and VCL load paths, and protect PURGE and other admin requests with ACLs."
sources:
  - https://www.varnish.org/docs/users-guide/vcl-inline-c/
  - https://www.varnish.org/docs/users-guide/run_security/
  - https://www.varnish.org/docs/reference/varnishd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# inline c and vmod safety

Two VCL mechanisms can run arbitrary code with the child process privileges: VMODs and inline C.

- Inline C (`C{ ... }C`) is disabled by default since Varnish 4. Enabling it allows any C in VCL, and a segfault in that code crashes the cache. It is enabled with `vcc_feature` (`allow_inline_c`).
- `vcc_feature` flags include `err_unref` (unreferenced VCL objects are errors) and `unsafe_path` (allow loading VCL/VMODs outside `vcl_path` and `vmod_path`).
- `vmod_path` is the directory (or colon-separated list) searched for modules; restrict it to a pre-approved set.
- `cc_command` runs the compiler: arbitrary program execution if changed, so lock it with `-r`.

HTTP-level admin requests such as PURGE should be restricted by ACL:

```vcl
acl purge { "localhost"; "192.0.2.0"/24; }
sub vcl_recv {
    if (req.method == "PURGE" && client.ip !~ purge) { return (synth(405)); }
}
```

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the 'not recommended' judgement, the unsupported advice to disable unsafe_path, and the Verify tip.

Method: documentation only; no commands were run.
