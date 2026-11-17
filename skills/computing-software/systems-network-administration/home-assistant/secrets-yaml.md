---
id: computing-software.systems-network-administration.home-assistant.secrets-yaml
name: secrets-yaml
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [secrets, secret, password]
level: practitioner
status: docs-checked
description: "Move passwords and API keys out of configuration.yaml into secrets.yaml with !secret, and debug where secrets are resolved from."
sources:
  - https://www.home-assistant.io/docs/configuration/secrets/
  - https://www.home-assistant.io/docs/configuration/securing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: remove private values from YAML so the configuration can be shared.

1. Create `secrets.yaml` in the Home Assistant configuration directory.
2. Replace the value in the configuration with `!secret` and an identifier:

```yaml
rest:
  - authentication: basic
    username: "admin"
    password: !secret rest_password
```

3. Store the value under that identifier in secrets.yaml:

```yaml
rest_password: "YOUR_PASSWORD"
```

Resolution order when configuration is split into subfolders:

- A `secrets.yaml` in the same folder as the YAML file that references the secret.
- Then parent folders, stopping at the folder holding the main configuration.yaml.

To log where each secret is loaded from, add this to secrets.yaml. The secret values themselves are not printed:

```yaml
logger: debug
```

Storing values in secrets.yaml does not encrypt them: the file is still plain text, so back it up and protect it. The securing checklist in the docs says the same.

Secrets help keep all passwords and API keys in one place instead of spread across many YAML files.

## Checked

2026-11-04. Confirmed against the Secrets page and the Securing page (which holds the checklist claim). Nothing removed; added the Securing page to sources.

Method: documentation only; no commands were run.
