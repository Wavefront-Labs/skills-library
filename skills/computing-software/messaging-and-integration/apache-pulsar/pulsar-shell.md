---
id: computing-software.messaging-and-integration.apache-pulsar.pulsar-shell
name: pulsar-shell
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [pulsar-shell, config-create, config-use, non-interactive, admin-commands]
level: practitioner
status: docs-checked
description: "Use Pulsar shell to switch between clusters (config create/use from client.conf) and run admin or client commands interactively or in scripted -e, -f and stdin modes."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/administration-pulsar-shell.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage several Pulsar clusters from one shell and script multi-command setups.

Pulsar shell exposes all Admin API features under the `admin` command and all pulsar-client features under `client`. Install by downloading the shell tarball from the download page, extracting it and running `./bin/pulsar-shell`. By default it connects to a local instance (service URL `pulsar://localhost:6650/`, admin URL `http://localhost:8080/`). Type `help`, use TAB completion, and `exit` or `quit` to leave.

Register a cluster. The source must be a valid `client.conf`, the same file used by pulsar-admin and pulsar-client:
```
config create --url https://<url_to_my_client.conf> mycluster
config create --file ./my-cluster-my-client.conf mycluster
config create --value "base64:<client.conf_base64_encoded>" mycluster
config use mycluster
```
`--url` must point to a valid remote file. After `config use`, the prompt and URLs switch to that cluster.

Non-interactive modes run commands sequentially:
```shell
./bin/pulsar-shell -e "
config use my-cluster
admin tenants create new-tenant
admin namespaces create new-tenant/new-namespace
" --fail-on-error
./bin/pulsar-shell -f ./setup-shell.txt --fail-on-error
```
`-e` takes a multi-line command string, `-f` a file (lines starting with `#` are comments), and `-` reads standard input. The page's examples pass `--fail-on-error` and start the script with `config use my-cluster`.

## Checked

2026-11-03. Confirmed against the pulsar-site page administration-pulsar-shell: admin and client commands, default URLs, the three `config create` forms, `config use`, and the `-e`, `-f` and `-` modes. Removed the unsourced `--fail-on-error` semantics, the gotcha and the invented Verify step.

Method: documentation only; no commands were run.
