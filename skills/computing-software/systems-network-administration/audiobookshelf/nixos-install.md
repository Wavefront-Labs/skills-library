---
id: computing-software.systems-network-administration.audiobookshelf.nixos-install
name: nixos-install
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [nixos, nix, configuration-nix, systemd, nginx]
level: practitioner
status: docs-checked
description: "Install Audiobookshelf on NixOS declaratively, set host and port flags, and enable services.audiobookshelf with an optional nginx proxy."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/linux/5.linux-install-nix.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Declarative install:

```nix
environment.systemPackages = [ pkgs.audiobookshelf ];
```

The executable takes the same options as the Docker container as parameters. The page's example of the defaults:

```bash
audiobookshelf --metadata "$(pwd)/metadata" --config "$(pwd)/config" --port 8000 --host 0.0.0.0
```

Behind a reverse proxy, listen on localhost with `--host 127.0.0.1`.

To start at boot, enable the systemd service in `configuration.nix`:

```nix
services.audiobookshelf.enable = true;
```

The page's optional nginx block sets `recommendedProxySettings = true`, a virtual host with `forceSSL`, and a `/` location with `proxyPass = "http://127.0.0.1:${builtins.toString config.services.audiobookshelf.port}"`, `proxyWebsockets = true` and `proxy_redirect http:// $scheme://;`. Check state with `systemctl status audiobookshelf.service`.

As with other native installs, you cannot load a backup from another install method without losing progress.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: NixOS install page.

Method: documentation only; no commands were run.
