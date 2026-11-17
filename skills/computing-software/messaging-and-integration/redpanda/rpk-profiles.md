---
id: computing-software.messaging-and-integration.redpanda.rpk-profiles
name: rpk-profiles
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [rpk, profiles, rpk-yaml, sasl, tls, prompt, multiple-clusters]
level: practitioner
status: docs-checked
description: "Create, switch, edit and use rpk profiles for several Redpanda clusters, with brokers, SASL and TLS in rpk.yaml, kept out of Git."
sources:
  - https://docs.redpanda.com/streaming/current/get-started/config-rpk-profile/
  - https://docs.redpanda.com/streaming/current/reference/rpk/rpk-profile/rpk-profile-set/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Profiles are the recommended way to configure rpk. Each is a named, reusable configuration for one cluster, stored together in an `rpk.yaml` file in a default OS directory. The file may hold passwords and SASL credentials, so never commit it to Git.

**Create** (rpk switches to the new profile automatically):

```bash
rpk profile create <profile-name> \
  --set brokers=<hostname:port> \
  --set admin.hosts=<hostname:port> \
  --set user=<username> \
  --set pass=<password> \
  --set sasl.mechanism=<mechanism> \
  --set tls.enabled=true \
  --description "<profile-description>"
```

The mechanism is `SCRAM-SHA-256`, `SCRAM-SHA-512` or `PLAIN`. Always set `--description`; it shows in `rpk profile list`. A profile can also be generated with `--from-redpanda` (a `redpanda.yaml`) or `--from-profile`.

**Operate**
- `rpk profile current` shows the active profile; `rpk profile use <name>` switches.
- `rpk profile set k=v` and `rpk profile edit` change one profile; `rpk profile set-globals` and `rpk profile edit-globals` change settings shared by all. A key can be a `-X` name or a YAML path, so `tls.enabled=true` equals `kafka_api.tls.enabled=true`.
- Pass `--profile dev` on any command, e.g. `rpk topic produce dev-topic --profile dev`.
- `rpk profile delete` removes one.

**Prompt.** Set `prompt: hi-red, "[%n]"` through `rpk profile edit dev` (`%n` is the profile name), then in a shell rc file use single quotes:

```bash
export PS1='\u@\h\n$(rpk profile prompt)% '
```

## Checked

2026-11-08. Read the whole rpk Profiles page and the rpk profile set page. Confirmed the create command and mechanisms, automatic switch on create, the --from-redpanda and --from-profile sources, the description advice, rpk.yaml location, set/edit/set-globals/edit-globals, the --profile flag, the prompt example with single quotes, and the Git caution; the equivalence of -X names and YAML paths is from the rpk profile set page. Nothing removed.

Method: documentation only; no commands were run.
