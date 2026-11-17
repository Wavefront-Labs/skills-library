---
id: computing-software.systems-network-administration.varnish-cache.varnishadm-cli-basics
name: varnishadm-cli-basics
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [varnishadm, cli-status, vcl-load-use, management-cli]
level: intro
status: docs-checked
description: "Use varnishadm to control a running Varnish: connection options, status codes, VCL load and use, bans, parameters, and starting or stopping the child process."
sources:
  - https://www.varnish.org/docs/users-guide/run_cli/
  - https://www.varnish.org/docs/reference/varnishadm/
  - https://www.varnish.org/docs/reference/varnish-cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# varnishadm cli basics

`varnishadm [-h] [-n workdir] [-p] [-S secretfile] [-T [address]:port] [-t timeout] [command ...]`. It connects either with `-n workdir` (secret file and address:port are looked up in shared memory) or with `-T` and `-S`; with neither it uses the `-n` defaults documented for varnishd. The CLI is available when varnishd runs with `-T`, `-M` or `-d`. For use from a remote system the guide recommends ssh into the varnishd host and running varnishadm there (`ssh $hostname varnishadm help`). With no command it is interactive with completion and history; with a command, the result goes to stdout and the exit status is zero on success, non-zero otherwise.

Every CLI reply starts with a three-digit status: 200 and 201 are OK (201 means output was truncated, see the `cli_limit` parameter); anything else means the command did not run. With a command argument, any other status makes varnishadm exit 1 and print the status on stderr.

```bash
varnishadm vcl.load v2 /path/to/new.vcl
varnishadm vcl.use v2
varnishadm ban 'req.url ~ "logo.*[.]png"'
varnishadm param.show prefer_ipv6
varnishadm param.set prefer_ipv6 true
varnishadm stop ; varnishadm start
varnishadm status -j
```

- VCL: `vcl.load <name> <file>` compiles and loads (a compile error is reported); `vcl.use <name>` switches instantly, new requests use it and in-flight requests finish on their old VCL; `vcl.use` the old name to go back. The guide recommends keeping an emergency VCL loaded. Also `vcl.list`, `vcl.show`, `vcl.discard`, `vcl.inline`, `vcl.label`.
- Bans: `ban req.url ~ "logo.*[.]png"` bans objects (still in cache, but not delivered); banning everything with `ban obj.http.date ~ .*` is faster and less disruptive than a restart. `ban.list` shows active bans.
- Parameters: `param.show [-l|-j] [<param>|changed]`, `param.set`, `param.reset`. Most take effect at once or after a short delay; a few need a child restart, noted in the parameter description. Change them only with a good reason such as tuning or security.
- Process: `stop`, `start`, `status`, `pid`, `panic.show`, `panic.clear`. With `varnishd -d` you must start the child explicitly. If the child dies the master restarts it unless the `auto_restart` parameter is off.
- Quoting: arguments with spaces need double quotes. Through varnishadm the command is expanded twice (shell, then CLI), so quote the quotes: `varnishadm param.set cc_command '"my alternate cc command"'`; without that you get `Unknown request` / `Too many parameters` and code 105. Here documents need `<<` and the word separated by a blank, and only the last argument may be one.
- `-j` gives JSON for informational commands; the top-level array holds a format version, the command as an array, a timestamp, then command-specific data. Errors are returned in the non-JSON form.

## Checked
2026-11-08. Read in full: the Users Guide CLI page, the varnishadm manual page and the varnish-cli reference. Confirmed: options, status codes, command names and behaviours listed above. Changed: removed the claim that remote use requires `-T`/`-S` (the guide recommends ssh), and the `vcl.use` and ban behaviour now follows the guide wording.
Method: documentation only; no commands were run.
