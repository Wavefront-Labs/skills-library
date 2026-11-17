---
id: computing-software.cloud-infrastructure-engineering.nginx.config-test
name: config-test
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, nginx-t, nginx--t, syntax-check, config-dump]
level: intro
status: docs-checked
description: "Validating nginx configuration with nginx -t, dumping it with -T, and the other command-line switches used around a reload."
sources: ["https://nginx.org/en/docs/switches.html", "https://nginx.org/en/docs/control.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

nginx command-line parameters relevant to checking a configuration:

- `-t` tests the configuration: nginx checks the syntax, then tries to open the files the configuration refers to.
- `-T` does the same as `-t` and also dumps the configuration files to standard output (1.9.2).
- `-q` suppresses non-error messages during configuration testing.
- `-c file` uses an alternative configuration file.
- `-p prefix` sets the path prefix (default `/usr/local/nginx`).
- `-v` prints the version; `-V` prints the version, compiler version and configure parameters.
- `-s signal` sends a signal to the master process: `stop` (fast shutdown), `quit` (graceful shutdown), `reload` (reload configuration, start new workers, gracefully stop old ones) or `reopen` (reopen log files).

```bash
nginx -t
nginx -T
nginx -t -c /path/to/other.conf
```

Test before you reload: on `HUP` (`nginx -s reload`) the master also checks the syntax and rolls back to the old configuration if applying the new one fails, but a test first gives the message without touching the running server.

## Checked

2026-11-03. Confirmed against the nginx "Command-line parameters" page (switches) and "Controlling nginx" (reload behaviour). Removed: claims about what `-t` cannot catch (ports, DNS, reuseport duplicates), `unknown directive` message text, the compiled-in modules pipeline, CI and permissions advice, and the Verify step.
Method: documentation only; no commands were run.
