---
id: computing-software.systems-network-administration.headscale.remote-cli
name: remote-cli
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, remote-cli, cli-address, cli-api-key, insecure]
level: practitioner
status: docs-checked
description: "Run the headscale CLI from a workstation against a remote server using an API key, via environment variables or a cli config section."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote CLI

Prerequisites: a workstation, a Headscale server reachable over HTTP(S), and an API key (api-keys-rest). The `headscale` binary on the workstation must match the server version (download from the GitHub releases, then `chmod +x /usr/local/bin/headscale`).

## Environment variables

```shell
export HEADSCALE_CLI_ADDRESS="<HEADSCALE_URL>"
export HEADSCALE_CLI_API_KEY="<API_KEY>"
```

## Or config

```yaml
cli:
    address: <HEADSCALE_URL>
    api_key: <API_KEY>
```

Test it:

```
headscale nodes list
```

## Notes

- Works through the existing reverse proxy without extra setup.
- A bare host without a scheme is assumed to be `https`.

## TLS problems

Verify the certificate, or add a self-signed certificate to the OS trust store. As a last resort, `cli.insecure: true` or `HEADSCALE_CLI_INSECURE=1` disables verification; the docs do not recommend disabling certificate validation.

## Checked

2026-11-04. Confirmed against the Headscale API reference (Remote control): prerequisites, same-version requirement, binary placement, the cli config section and environment variables, bare host assumed https, nodes list test, reverse proxy note, and the insecure options. Removed an unsourced claim about commands that cannot run remotely.
Method: documentation only; no commands were run.
