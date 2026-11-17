---
id: computing-software.email-administration.dovecot.health-check-service-for-load-balancers
name: health-check-service-for-load-balancers
category: computing-software
field: email-administration
product: dovecot
tags: [health-check, health-check-script, passthrough-mode, load-balancer, service-script, script-environment]
level: advanced
status: docs-checked
description: "Offer a Dovecot health-check listener backed by a script, with passthrough mode, allowed environment variables and the request protocol."
sources:
  - https://doc.dovecot.org/main/core/config/health_check.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To offer health checks, extend the `health-check` service with a listener. The documented default is the simple PING-to-PONG example: `executable = script -p health-check.sh` with an `inet_listener health-check` on port 5001. The manual says to be extremely careful when modifying `health-check.sh` or implementing your own; treat a faulty or unsafe script as an attack surface.

Options on the script service:
- `-e name value` lists environment variables that a request may set before the script runs. Example: `script -e foo bar health-check.sh` sets `FOO=BAR`.
- `-p` enables passthrough mode, which calls the script directly with no protocol and returns its output directly. This is the simple choice for load balancers that only read the reply.

Without passthrough, the request must follow the script protocol, line by line: a `VERSION` line (`VERSION\tscript\t4\t0\n` at the time of writing), an optional `alarm=<secs>` line (which must come before `noreply`), optional `env_<name>=<value>` lines for variables allowed by `-e`, a `noreply` line or `-` (anything really, but `-` must be given if `noreply` is absent), then one argument per line, an empty line, and the DATA input to pass to the script.

The `noreply` behaviour disables the success or fail answer that the script executable itself sends, which is useful when the script produces its own response.

Design points:
- Keep the script fast and local; a slow check makes load balancers flap.
- Do not let requests pass arbitrary environment variables; allow only what the script needs.
- Check what matters, such as auth and mail storage reachability, not only that the port is open.

## Checked

2026-11-08. Read the Health Check Scripting page in full. Added the documented default listener (port 5001, script -p health-check.sh) and the line-by-line request protocol, including the VERSION line.

Method: documentation only; no commands were run.
