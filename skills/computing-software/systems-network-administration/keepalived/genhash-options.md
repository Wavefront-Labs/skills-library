---
id: computing-software.systems-network-administration.keepalived.genhash-options
name: genhash-options
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, genhash, digest, http-get, command-line, health-checking]
level: practitioner
status: docs-checked
description: "genhash command-line options for producing the digest used by HTTP_GET and SSL_GET checks: server, port, URL, SSL, virtual host, hash algorithm."
sources:
  - https://keepalived.readthedocs.io/en/latest/programs_synopsis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# genhash options

`genhash` generates a digest string for a web page, for use in health checks.

| Option | Meaning |
|---|---|
| `-S`, `--use-ssl` | Connect with SSL |
| `-s`, `--server <host>` | IP address of the server |
| `-p`, `--port <port>` | Port |
| `-u`, `--url <url>` | Path of the page to hash |
| `-V`, `--use-virtualhost <host>` | Virtual host sent in the HTTP headers |
| `-H`, `--hash <alg>` | Hash algorithm; the help screen lists choices and marks the default |
| `-v`, `--verbose` | Verbose output |
| `-r`, `--release` | Show version and exit |
| `-h`, `--help` | Help and exit |

Run it against each real server and URL you will check, then place the result in the `digest` of the matching `url` block.

## Checked

2026-11-04. Confirmed every option and its long form against the Keepalived programs synopsis page (genhash utility section). Removed an unsourced verification sentence.

Method: documentation only; no commands were run.
