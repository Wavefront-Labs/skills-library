---
id: computing-software.collaboration-platform-administration.matrix-synapse.choose-server-name-and-generate-config
name: choose-server-name-and-generate-config
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, server-name, generate-config, signing-key, report-stats, homeserver-yaml, install]
level: practitioner
status: docs-checked
description: "Choose a permanent Synapse server_name, generate homeserver.yaml and signing keys with --generate-config, and understand what to back up and what changing keys involves."
sources:
  - https://element-hq.github.io/synapse/latest/setup/installation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The server name cannot be changed after installation, so decide it first. It forms the domain part of every user ID (`@user:my.domain.name`) and tells other servers how to reach you. For a test, use the host name. For production the docs suggest your bare domain (`example.com`) rather than a Matrix-specific host, the same way an email address is `user@example.com`, but this may need delegation; see the federation docs. Read the security page before setting up.

Generate the config from the Synapse virtualenv:

```sh
cd ~/synapse
python -m synapse.app.homeserver \
    --server-name my.domain.name \
    --config-path homeserver.yaml \
    --generate-config \
    --report-stats=[yes|no]
```

`--report-stats` chooses whether to report usage statistics (hostname, Synapse version, uptime, total users and so on) to the developers.

The command also produces the server's signing keys, which identify your homeserver to others. Do not lose or delete them; back them up somewhere safe. If you must change the signing key, other servers may have the old key cached, so rename the key in the `<server name>.signing.key` file (its second word) to something different; the Matrix server-server spec on retrieving server keys has the details.

Start the server from the working directory with the virtualenv active:

```sh
cd ~/synapse
source env/bin/activate
synctl start
```

Debian packages keep config at `/etc/matrix-synapse/homeserver.yaml`, and you can put overrides in `/etc/matrix-synapse/conf.d/` so package upgrades do not prompt about replacing the main file.

## Checked

Method: docs-checked 2026-11-09 against docs/setup/installation.md (Synapse develop branch, raw markdown; server name, generate-config, signing key, Debian conf.d sections read).
