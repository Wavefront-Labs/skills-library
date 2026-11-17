---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-cscli-bouncers-and-machines
name: crowdsec-cscli-bouncers-and-machines
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [cscli, bouncers, machines, api-key, lapi-register, authentication]
level: practitioner
status: docs-checked
description: "Register bouncers and Log Processor machines with the Local API using cscli, including remote machine validation and credential file handling."
sources: ["https://docs.crowdsec.net/docs/local_api/authentication", "https://docs.crowdsec.net/docs/local_api/configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Local API has three authentication methods:

1. **API key** for remediation components. Read-only access to decisions.
2. **Login and password** for Log Processors (machines). They can read, create and delete decisions.
3. **TLS client certificates** for either, see the TLS authentication skill.

## Bouncers

Run on the LAPI server:

```console
sudo cscli bouncers add testBouncer
```

Keep the generated API token and put it in the remediation component's configuration file.

## Machines

On the LAPI server, `sudo cscli machines add testMachine` generates credentials. If the LAPI server already has its own credentials file, pass `-f /path/to/credentials.yaml` (or `-f-` to print to stdout) so you do not overwrite it when generating for another host.

Alternatively a remote machine self-registers:

```console
sudo cscli lapi register -u http://REMOTE_API:8080
sudo cscli machines list
sudo cscli machines validate MACHINE_NAME
sudo systemctl restart crowdsec
```

On the registered machine, replace `local_api_credentials.yaml` if you are installing credentials there, and set `api.server.enable: false` in `config.yaml` so it stops running its own Local API and forwards everything to the server. The LAPI default listen address is loopback, so for remote clients change `listen_uri`.

## Checked
2026-11-08. Confirmed against the Local API Authentication and Configuration pages: the three authentication kinds and their permissions, `cscli bouncers add`, `cscli machines add` with `-f`, `cscli lapi register`, `machines list|validate`, the restart, `api.server.enable: false` and the loopback default. Removed: the "shown once", 403 and `bouncers list` claims (not on these pages).
Method: documentation only; no commands were run.
