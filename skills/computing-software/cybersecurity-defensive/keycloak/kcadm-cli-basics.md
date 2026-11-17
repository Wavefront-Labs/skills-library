---
id: computing-software.cybersecurity-defensive.keycloak.kcadm-cli-basics
name: kcadm-cli-basics
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, kcadm, admin-cli, config-credentials, rest-api]
level: practitioner
status: docs-checked
description: "Authenticate the Keycloak admin CLI kcadm.sh and create, get, update and delete realms, clients and users, including config and --no-config modes."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/admin-cli.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kcadm cli basics
`kcadm.sh` (`kcadm.bat` on Windows) ships in the server's `bin` directory (add it to PATH; set KEYCLOAK_HOME). It makes HTTP requests to the Admin REST endpoints, which need authentication. Start a session, then run CRUD commands:
```
kcadm.sh config credentials --server http://localhost:8080 --realm demo --user admin --client admin
kcadm.sh create realms -s realm=demorealm -s enabled=true -o
CID=$(kcadm.sh create clients -r demorealm -s clientId=my_client -s 'redirectUris=["http://localhost:8980/myapp/*"]' -i)
kcadm.sh get clients/$CID/installation/providers/keycloak-oidc-keycloak-json
```
Pattern: `kcadm.sh create|get|update|delete ENDPOINT [ARGUMENTS]`, mapping to POST, GET, PUT and DELETE. A relative ENDPOINT resolves to `SERVER_URI/admin/realms/REALM/ENDPOINT`; `realms` and `serverinfo` are outside any realm. `-r` names the target realm when it differs from the login realm. `-s` / `--set` sets name=value pairs (values are assumed to be JSON, else sent as text); `-f FILE` sends a JSON document (`-f -` reads standard input); `-o` prints the result and `-i` prints the new id; `--fields realm,enabled` limits attributes and `--format csv --noquotes` gives CSV.

Updating: `get realms/demorealm > demorealm.json`, edit, then `update realms/demorealm -f demorealm.json`; or `update realms/demorealm -s enabled=false`. By default `update` does a GET and merges; `-n` does a PUT without the GET (needed for endpoints with no GET, such as `reset-password`). Delete: `kcadm.sh delete realms/demorealm`. Reset a password: `kcadm.sh set-password -r demorealm --username testuser --new-password NEWPASSWORD --temporary`.

Authentication: log in with a server URL, realm and user name, or with only a clientId (a unique service account; then only the client secret, or a signed JWT, is needed). The account needs permission to call the Admin REST operations (for example `realm-admin` of the `realm-management` client). `config credentials` saves the access and refresh tokens and secrets in `$HOME/.keycloak/kcadm.config`; that file must stay private (use `--config` for a different file and keep one config per thread). With `--no-config` each command authenticates itself and nothing is saved, at the cost of more token requests. If `--password` is omitted you are prompted unless `KC_CLI_PASSWORD` is set; avoid passwords on the command line. For https servers not covered by Java's default truststore, run `kcadm.sh config truststore --trustpass $PASSWORD ~/.keycloak/truststore.jks`.

Run `kcadm.sh help` and `kcadm.sh config credentials --help` for full option lists.

## Checked
2026-11-03. Confirmed against server_admin/topics/admin-cli.adoc: all commands, flags, config-file location and `--no-config`. Removed: the unsourced `--secret` login form, "do not run as master admin" and "exact id" gotchas and the Verify step.
Method: documentation only; no commands were run.
