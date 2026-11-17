---
id: computing-software.cloud-infrastructure-engineering.docker.debug-image-variants-with-busybox
name: debug-image-variants-with-busybox
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, debug-container, debug-image-tag, distroless, busybox, docker-debug, debugging]
level: practitioner
status: docs-checked
description: "Swap a distroless image for its :debug variant to get a busybox shell, or use docker debug and a shared PID namespace when the production image must stay unchanged."
sources: ["https://github.com/GoogleContainerTools/distroless#debug-images", "https://docs.docker.com/reference/cli/docker/debug/", "https://docs.docker.com/reference/cli/docker/container/run/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug image variants with a busybox shell

Distroless images contain only the application and its runtime dependencies, with no package
manager, shell or other programs. Each published distroless image also has a `:debug` tag
that adds a busybox shell.

## Which tag to use
| Base | Production | Debug variant |
|---|---|---|
| Google distroless | `gcr.io/distroless/static-debian13` (also `:nonroot`) | `gcr.io/distroless/static-debian13:debug` and `:debug-nonroot` |

If the image you use already has a tag, the debug tag is `debug-<existing tag>`: for example
`gcr.io/distroless/java17-debian13:nonroot` becomes `gcr.io/distroless/java17-debian13:debug-nonroot`.
Tags are listed per image in the distroless README; images are tagged with a Debian version
suffix, and that README names `-debian13` images, so check it for the current suffix before
copying a tag from an older Dockerfile.

## Swapping for an investigation
Edit the final stage to use the debug tag, rebuild, and start a shell instead of the app
(this is the README's own example, using a Python image):
```dockerfile
FROM gcr.io/distroless/python3-debian13:debug
COPY . /app
WORKDIR /app
CMD ["hello.py", "/etc"]
```
```bash
docker build -t my_debug_image .
docker run --entrypoint=sh -ti my_debug_image
```
The README notes `ldd` is not installed in the base image because it is a shell script.
Distroless images have no shell, so an `ENTRYPOINT` or `CMD` written in shell form does not
work: use the vector (exec) form, for example `ENTRYPOINT ["myapp"]`.

## When not to swap
If the issue only reproduces in the exact production image, use `docker debug <container>`.
Docker Debug gives a shell into any container or image, even one without a shell, using its
own toolbox; it does not modify the image, and for images and stopped containers all changes
are discarded when you leave the shell. A running or paused container sees filesystem
changes made from the debug shell directly. `docker debug --command "<cmd>" <container>`
evaluates one command instead of opening an interactive session.

Another option is a throwaway container that joins the target's PID namespace:
`docker run --rm -it --pid=container:<name> <tools-image>` (`--pid=container:<name|id>` joins
another container's PID namespace; the `docker run` page uses an Alpine image with strace as
its example). Swapping the base changes the image digest and can mask bugs specific to the
production base.

## Guardrails
- Keep debug tags out of production: a CI check that the final stage's base image is not a
  `:debug` or `debug-*` tag.
- Remember that `debug-nonroot` exists as a separate tag from `debug`; check which user the
  tag you choose runs as before drawing conclusions about permission problems.

## Checked
Date: 2026-11-07
Pages read: the distroless README (whole repo page, text read in full, including the Debug Images and
Entrypoints sections); the `docker debug` CLI page (read in full); docker container run page (option table
and the `--pid` section searched, the rest of this large page not read in full).
Trimmed or corrected: the Chainguard row and source (the cited edu.chainguard.dev page returns 404, no
replacement found); the Docker Hardened Images `-dev` row (no cited page); the claim that busybox lives at
`/busybox/sh` and that plain `sh` may not be on PATH (the README example uses `--entrypoint=sh`); the claim
that debug variants run as root (README does not say so); the `--network container:<c>` sidecar option (not on
the docker run page I read); the invented Verify steps; `static-debian12` examples replaced by the `-debian13`
tags the README lists; the ARG/--build-arg swap pattern (not on a cited page) replaced by the README's own
example. The README table of images was read but its per-image architecture lists are not reproduced.
Method: documentation only; no commands were run.
