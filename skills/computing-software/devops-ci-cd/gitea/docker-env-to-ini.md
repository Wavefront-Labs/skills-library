---
id: computing-software.devops-ci-cd.gitea.docker-env-to-ini
name: docker-env-to-ini
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-environment-to-ini, gitea, gitea-section-key, env-file-secret, generate-secret, app-ini-env]
level: practitioner
status: docs-checked
description: "Set or override any Gitea app.ini key in Docker with GITEA__section__KEY env vars or a __FILE variant, and generate SECRET_KEY and INTERNAL_TOKEN."
sources: ["https://docs.gitea.com/installation/install-with-docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GITEA__section__KEY environment settings (Docker)

Any `app.ini` setting can be set or overridden with an environment variable named `GITEA__<section_name>__<KEY_NAME>=value`. On each container start the `environment-to-ini` command (a wrapper of `gitea config edit-ini`; see `./gitea config edit-ini --help`) applies them to the file. They are not passed to Gitea's sub-processes.

```yaml
environment:
  - GITEA__database__DB_TYPE=postgres
  - GITEA__database__HOST=db:5432
  - GITEA__mailer__ENABLED=true
  - GITEA__mailer__PROTOCOL=smtps
  - GITEA__mailer__USER=${GITEA__mailer__USER:-apikey}
  - GITEA__mailer__PASSWD="""${GITEA__mailer__PASSWD:?GITEA__mailer__PASSWD not set}"""
```
The docs use compose substitution (`${VAR:?message}` fails fast when unset) with a `.env` file beside the compose file, and wrap the password in triple quotes.

To read a value from a file instead (Docker/Kubernetes secrets), append `__FILE`: `GITEA__section_name__KEY_NAME__FILE=/path/to/file`.

## Image-level variables
`USER` (default git), `USER_UID` (1000), `USER_GID` (1000). Match UID/GID to the owner of a host-mounted `/data`; not needed for named volumes.

## Secrets
Gitea generates secrets for each new install and writes them to `app.ini`. To supply your own:
```sh
docker run -it --rm docker.gitea.com/gitea:1 gitea generate secret SECRET_KEY
docker run -it --rm docker.gitea.com/gitea:1 gitea generate secret INTERNAL_TOKEN
```
then set `GITEA__security__SECRET_KEY` and `GITEA__security__INTERNAL_TOKEN`. Never lose or change `SECRET_KEY` after installation: encrypted data can no longer be decrypted.

## Checked

2026-11-03: read https://docs.gitea.com/installation/install-with-docker/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
