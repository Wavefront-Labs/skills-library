---
id: computing-software.data-engineering.kestra.kestractl
name: kestractl
category: computing-software
field: data-engineering
product: kestra
tags: [kestractl, cli, flows-deploy, executions, nsfiles, contexts]
level: practitioner
status: docs-checked
description: "Manage a Kestra instance from the command line with kestractl: contexts, flow validate and deploy, running executions, namespaces, files and KV."
sources:
  - https://kestra.io/docs/kestra-cli/kestractl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`kestractl` is the API-level CLI (flows, executions, namespaces, namespace files, KV). The separate Kestra Server CLI handles starting servers and server-side plugin installation.

Contexts live in `~/.kestractl/config.yaml`:

```bash
kestractl config add default http://localhost:8080 main --username YOUR_USERNAME --password YOUR_PASSWORD --default
kestractl config add default https://kestra.example.com production --token YOUR_TOKEN --default
```

Open source uses basic auth; Enterprise uses an API token. Precedence: flags, environment variables (`KESTRACTL_HOST`, `KESTRACTL_TENANT`, `KESTRACTL_TOKEN`, ...), config file, defaults.

```bash
kestractl flows validate ./flows/
kestractl flows deploy ./flows/ --namespace prod --override --fail-fast
kestractl executions run my.namespace my-flow --wait --output json
kestractl nsfiles upload my.namespace ./assets --path resources --override
kestractl kv set my.namespace STRING session_token "abc" --ttl PT1H
```

Caveats:

- `kv list` needs token auth and returns 401 with basic auth.
- `--namespace` and `--namespace-prefix` are mutually exclusive on `flows deploy`.
- `--disable-triggers` errors on YAML-aliased or flow-style trigger mappings.
- `executions watch` exits non-zero on FAILED, KILLED or CANCELLED.
- `--variable` and `--variables-file` replace the namespace's whole variable set.
- `--verbose` prints credentials in HTTP requests.

## Checked

2026-11-04. Confirmed against the Kestra kestractl docs page: the config add commands and config file path, basic auth versus token, configuration precedence and the KESTRACTL environment variables, the validate, deploy, run, nsfiles and kv examples, and every listed caveat. Corrected: the page says the Server CLI covers starting servers and server-side plugin installation, not the database.

Method: documentation only; no commands were run.
