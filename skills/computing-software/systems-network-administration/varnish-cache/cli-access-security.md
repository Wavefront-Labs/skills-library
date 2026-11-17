---
id: computing-software.systems-network-administration.varnish-cache.cli-access-security
name: cli-access-security
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [secret-file, cli-auth, varnishd-jail, cli-security]
level: advanced
status: docs-checked
description: "Secure the Varnish management CLI and process: -T address, -S pre-shared key file, -M reverse mode, read-only parameters, CLI syslog, VMOD paths and the -j jails."
sources:
  - https://www.varnish.org/docs/users-guide/run_security/
  - https://www.varnish.org/docs/reference/varnishd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cli access security

Varnish has four levels of authority: command line arguments (decided at start, so they cannot be manipulated later), the CLI, VCL programs, and HTTP requests.

CLI access:

- `-T address:port` offers the CLI (examples: `127.0.0.1:631`, `'[fe80::1]:8082'`; `none` disables it). Default `localhost:0` picks a random port that varnishadm learns from shared memory. A localhost address restricts access to the machine. A routable address gives no secrecy: commands cross the network as unencrypted text, protected only by the pre-shared key.
- `-S file` is the pre-shared key (PSK). Without `-S`, a random secret is written to a `_.secret` file in the working directory, owned by the user who started varnishd. To delegate access, create your own file readable only by those users, e.g. `dd if=/dev/random of=<path> count=1`; the varnishd master must also be able to read it. The file is re-read on each CLI authentication, so it can change while running. Remote varnishadm needs a copy via `-S`. `-S none` disables authentication.
- `-M address:port`: varnishd connects out and offers the CLI to a central management facility (reverse mode); still unencrypted, still PSK. The reference adds that with -M and no backend defined, the child does not start initially.
- Safer remote access: bind to localhost and use ssh or a VPN; with ssh you can restrict users to varnishadm or wrapper scripts allowing specific commands. There is no built-in way to restrict commands per CLI connection.
- `-d` gives a CLI on stdin/stdout.

Parameters: `-r param[,param...]` makes them read-only from the CLI. Protect `cc_command` (runs arbitrary programs), `vmod_path` (could load rogue modules), and `vcc_feature`'s `allow_inline_c` and `unsafe_path` flags. `syslog_cli_traffic` (bool, default on) logs all CLI traffic to syslog.

VCL: VMODs and inline-C can execute arbitrary code with the child process's privileges. Inline-C is disabled by default since Varnish 4. If varnishd is started as root, the child is sandboxed; otherwise not. Restricting VMODs to a designated directory limits VCL authors to pre-approved VMODs. Restrict administrative HTTP requests such as PURGE to trusted IPs with ACLs.

Jails, `-j`:
- `linux`: default on Linux; extends the unix jail, warns when the workdir is not on tmpfs, tries to keep the process dumpable and controls transparent hugepages (`try-disable` default).
- `unix[,user=,ccgroup=,workuser=]`: default elsewhere when started as root; defaults to users `varnish` and `vcache`.
- `solaris[,worker=privspec]`: reduced privileges; not using `worker` is always more secure.
- `none`: all processes run with the privileges varnishd started with (last resort).

## Checked

Method: 2026-11-08 docs-only read of the security guide; the -T, -M, -S, -r and -j entries and syslog_cli_traffic in the varnishd reference were checked by search, not read in full. Added the default secret file behaviour and -T none; the earlier text was otherwise accurate.
