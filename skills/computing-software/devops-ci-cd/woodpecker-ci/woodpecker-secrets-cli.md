---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-secrets-cli
name: woodpecker-secrets-cli
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [secrets-cli, woodpecker-cli, ssh-key]
level: practitioner
status: docs-checked
description: "Create Woodpecker secrets from the command line, limited by image and event."
sources: ["https://woodpecker-ci.org/docs/usage/secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker secrets from the CLI

Use `woodpecker-cli repo secret add` to create a repository secret. By default it is available to all images for `push`, `tag` and `deployment` events, but not `pull_request`.

```bash
woodpecker-cli repo secret add \
  --repository octocat/hello-world \
  --name aws_access_key_id \
  --value <value>
```

Limit it to one or more images with repeated `--image` flags:

```bash
woodpecker-cli repo secret add \
  --repository octocat/hello-world \
  --image woodpeckerci/plugin-s3 \
  --image woodpeckerci/plugin-docker-buildx \
  --name aws_access_key_id \
  --value <value>
```

Enable events with repeated `--event` flags:

```bash
woodpecker-cli repo secret add \
  --repository octocat/hello-world \
  --event push --event tag \
  --name aws_access_key_id \
  --value <value>
```

Load a value from a file with `@`. This preserves line breaks, which matters for SSH keys:

```bash
woodpecker-cli repo secret add \
  --repository octocat/hello-world \
  --name ssh_key \
  --value @/path/to/id_rsa
```

Connect the CLI first with `woodpecker-cli setup`, which opens the Woodpecker UI in your browser to confirm the login and saves the server and token as a context. Secrets can also be managed in the UI.

## Checked

2026-11-03. Read the Woodpecker secrets usage page and confirmed the woodpecker-cli secret add commands and flags. Nothing removed. 

Method: documentation only; no commands were run.
