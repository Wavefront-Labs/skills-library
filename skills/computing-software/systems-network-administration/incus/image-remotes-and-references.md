---
id: computing-software.systems-network-administration.incus.image-remotes-and-references
name: image-remotes-and-references
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, images, remote, simplestreams, oci, docker-hub, fingerprint, alias]
level: practitioner
status: docs-checked
description: "Add image remotes (simplestreams, OCI such as Docker Hub, Incus servers), reference images as remote:alias, set the default remote."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/images_remote.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image remotes

```
incus remote list
incus image list <remote>:
incus remote add <name> <URL> --protocol=simplestreams
incus remote add oci-docker https://docker.io --protocol=oci
incus remote add oci-myregistry https://code.example.org --token abcMyToken --protocol=oci
incus remote add my-remote 192.0.2.10
incus remote get-default
incus remote switch <remote_name>
```

- Simple streams servers are pure image servers; `incus`-format remotes are Incus servers that may also serve images.
- Simplestreams and OCI URLs must use HTTPS.
- Adding an Incus server prompts to confirm the fingerprint then asks for a token; OIDC needs `--auth-type=oidc`.
- Reference an image as `<remote>:<alias or fingerprint>`, e.g. `images:debian/12` or `local:ed7509d7e83f`.
- Names without a remote prefix use the default remote.

## Checked

2026-11-09. Confirmed against the Incus doc howto/images_remote.md: remote list and add forms per protocol, HTTPS requirement, fingerprint and token prompt, OIDC flag, image reference syntax and default remote. Removed: nothing needed removing.

Method: documentation only; no commands were run.
