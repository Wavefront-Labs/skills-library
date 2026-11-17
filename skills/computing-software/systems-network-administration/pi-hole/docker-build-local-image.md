---
id: computing-software.systems-network-administration.pi-hole.docker-build-local-image
name: docker-build-local-image
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [docker-build-sh, pihole-local-image, branch-image]
level: advanced
status: docs-checked
description: "Build a custom or branch-specific Pi-hole image with the repository's build.sh instead of pihole checkout."
sources: ["https://docs.pi-hole.net/docker/build-image/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Build the Pi-hole image locally

Clone the repository first:

```bash
git clone https://github.com/pi-hole/docker-pi-hole
cd docker-pi-hole
```

**build.sh usage**

```text
./build.sh [-l] [-f <ftl_branch>] [-c <core_branch>] [-w <web_branch>] [-t <tag>] [use_cache]
```

| Option | Meaning |
| --- | --- |
| `-f` | FTL branch (not with `-l`) |
| `-c` | Core branch |
| `-w` | Web branch |
| `-p` | PADD branch |
| `-t` | Image tag (default `pihole:local`) |
| `-l` | Use a locally built FTL binary (needs `src/pihole-FTL`) |
| `use_cache` | Enable caching; by default `--no-cache` is used |

With no options it runs `docker buildx build src/. --tag pihole:local --load --no-cache`.

**Use cases**

- Contributing: run `./build.sh` after your changes; `./build-and-test.sh` runs the same tests as GitHub.
- As a replacement for `pihole checkout` (disabled in the image): `./build.sh -f new/Sensors` builds with an FTL branch.
- A docker-specific branch: `git checkout fix/logRotate`, then `./build.sh`.

**Use the image.** Replace `pihole/pihole:latest` with `pihole:local` in compose or in `docker run`.

**Checklist**

1. Check out the docker-pi-hole branch you need, or pass `-f`, `-c` or `-w` for a component branch.
2. Run `./build.sh`.
3. Point compose or `docker run` at the new tag.

## Checked

2026-11-03. Read the Docker Building page: the clone commands, the build.sh usage text and options (including `-p` and `use_cache`), the default `docker buildx build` command, the contributing and `pihole checkout` alternative examples, and using `pihole:local`.

Method: documentation only; no commands were run.
