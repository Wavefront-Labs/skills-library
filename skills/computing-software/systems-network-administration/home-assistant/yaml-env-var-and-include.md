---
id: computing-software.systems-network-administration.home-assistant.yaml-env-var-and-include
name: yaml-env-var-and-include
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [env-var, include, core-install]
level: practitioner
status: draft
description: "Pull values into Home Assistant YAML with !env_var (with default) on Core installs and !include for whole files."
sources:
  - https://www.home-assistant.io/docs/configuration/yaml/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: keep values out of configuration.yaml by reading them from the environment or from another file.

Environment variables

`!env_var` reads a system environment variable. It only works on Home Assistant Core installations where you can set variables. Other users are told to use `!include` instead.

```yaml
example:
  password: !env_var PASSWORD
```

Default value

If the variable is not set, a second argument is used as the fallback:

```yaml
example:
  password: !env_var PASSWORD default_password
```

Including entire files

Move a whole domain into its own file with `!include`:

```yaml
light: !include lights.yaml
```

The included file holds only what belongs under that key. Do not repeat the parent key inside it. For the full include family and file layout, see the splitting-configuration skill.

Choosing between them

- Secret values that differ per machine and are set by the host: `!env_var`, Core only.
- Values you want in a separate, editable or shareable file: `!include`.
- Passwords and tokens kept in the configuration directory: `!secret` (see the secrets-yaml skill).

After editing, run the configuration check before restarting so a typo does not stop Home Assistant from starting.
