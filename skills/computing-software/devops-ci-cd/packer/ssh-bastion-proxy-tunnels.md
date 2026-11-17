---
id: computing-software.devops-ci-cd.packer.ssh-bastion-proxy-tunnels
name: ssh-bastion-proxy-tunnels
category: computing-software
field: devops-ci-cd
product: packer
tags: [ssh-bastion, socks-proxy, tunnels, jump-host, comm-ssh-bastion]
level: advanced
status: docs-checked
description: "Reach a build machine through an SSH bastion, a SOCKS proxy, or remote and local tunnels."
sources:
  - "https://developer.hashicorp.com/packer/docs/communicators/ssh/"
  - "https://github.com/hashicorp/packer-plugin-sdk/blob/main/cmd/packer-sdc/internal/renderdocs/docs-partials/packer-plugin-sdk/communicator/SSH-not-required.mdx"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When the build machine is not directly reachable, the SSH communicator options for intermediaries are defined in the packer-plugin-sdk communicator documentation (shared by every builder that uses the SSH communicator).

Bastion host:

- `ssh_bastion_host` is the bastion used for the actual SSH connection; `ssh_bastion_port` defaults to `22`; `ssh_bastion_username` is the user.
- Authenticate with `ssh_bastion_password`, `ssh_bastion_private_key_file` (a PEM encoded key file; `~` is expanded), `ssh_bastion_agent_auth` (uses the local SSH agent; default `false`), `ssh_bastion_interactive` (keyboard-interactive) or `ssh_bastion_certificate_file` (a user certificate).

```hcl
ssh_bastion_host             = "bastion.example.com"
ssh_bastion_username         = "jump"
ssh_bastion_private_key_file = "/path/to/key.pem"
```

SOCKS proxy:

- `ssh_proxy_host` is the SOCKS proxy host; `ssh_proxy_port` defaults to `1080`; `ssh_proxy_username` and `ssh_proxy_password` are optional credentials.

Tunnels (each a list of strings):

- `ssh_remote_tunnels` forward a port from your local machine to the instance. Format `REMOTE_PORT:LOCAL_HOST:LOCAL_PORT`; the docs example `9090:localhost:80`.
- `ssh_local_tunnels` forward a port from the instance to your local machine. Format `LOCAL_PORT:REMOTE_HOST:REMOTE_PORT`; the docs example `8080:localhost:3000`.

`ssh_timeout` is the time to wait for SSH to become available, which matters when the route is slow to come up.

Keep the key outside the template repository and put the bastion host and credentials in variables so templates stay portable across networks.

## Checked

2026-11-09. Checked against the SDK communicator partial for SSH optional settings (`SSH-not-required.mdx` in packer-plugin-sdk): all `ssh_bastion_*`, `ssh_proxy_*`, tunnel options, defaults 22 and 1080, and `ssh_timeout`. The Packer SSH communicator page itself only embeds these partials.

Removed: the unsupported advice to prefer key authentication over passwords and the "choose bastion versus proxy" guidance, which are judgement, not documented behaviour.

Method: documentation only; no commands were run.
