---
id: computing-software.systems-network-administration.audiobookshelf.podman-quadlet-deployment
name: podman-quadlet-deployment
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [podman, quadlet, systemd, containers, selinux]
level: practitioner
status: docs-checked
description: "Run Audiobookshelf under Podman 4.4 or later with a Quadlet .container file or a podman run command, including the SELinux relabel step."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/7.podman.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Quadlet containers need Podman 4.4 or above. Example `audiobookshelf.container`:

```ini
[Container]
ContainerName=audiobookshelf
Image=ghcr.io/advplyr/audiobookshelf:latest
AutoUpdate=registry
NoNewPrivileges=true
PublishPort=13378:80
Volume=</path/to/audiobooks>:/audiobooks
Volume=</path/to/podcasts>:/podcasts
Volume=</path/to/config>:/config
Volume=</path/to/metadata>:/metadata

[Service]
Restart=always

[Install]
WantedBy=default.target
```

The page's example also maps a `/books` volume. The equivalent `podman run -d -p 13378:80 -v ... --name audiobookshelf -e TZ="America/Toronto" ghcr.io/advplyr/audiobookshelf:latest` takes the same mounts.

Remove the `<>` symbols from paths, and keep all volume mappings as separate directories not contained in each other.

SELinux: if it is enabled on the host, the container may be blocked from the mapped directories. The page's fix:

```bash
sudo chcon -R -t svirt_sandbox_file_t /path/to/directory
```

## Checked

Method: docs-checked 2026-11-09 against the Podman page of the Audiobookshelf docs repo (full raw markdown: Container Example, run command, SELinux caution). Dropped a paragraph explaining individual Quadlet directives and systemd reload, which the page does not state.
