---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.immutable-container-images-with-buildah-and-dockerfiles
name: immutable-container-images-with-buildah-and-dockerfiles
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, immutable-infrastructure, container-images, buildah, dockerfile, containerfile, ansible-buildah-connection, image-digests, reproducible-builds]
level: advanced
status: docs-checked
description: "Build immutable container images from code with Dockerfiles or buildah commands (including Ansible over the buildah connection); pin bases by digest and rebuild often."
sources: ["https://docs.docker.com/build/building/best-practices/", "https://raw.githubusercontent.com/containers/buildah/main/docs/tutorials/01-intro.md", "https://docs.ansible.com/ansible/latest/collections/containers/podman/buildah_connection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Immutable container images with buildah and Dockerfiles

Goal: every change produces a new image built from code, identified by digest; running containers
are replaced, never modified. Rollback = deploy the previous digest.

## Dockerfile practices (Docker build best practices)
- Rebuild images often so base-image and package updates arrive. `--pull` fetches the latest base image, and `--no-cache` forces all layers to rebuild from scratch (both can be combined).
- Pin base image versions. A tag such as `alpine:3.21` resolves to the latest patch of that version and can point at a different image when you rebuild months later. To fully secure supply-chain integrity, pin to a digest as well: `FROM alpine:3.21@sha256:<digest>`. Docker notes you then need a process to update pinned digests, and suggests automating base tag and digest updates on a schedule rather than leaving a floating tag.
- Use the exec form for `CMD` (`CMD ["executable", "param1"]`), which the guide recommends for service images.

## Scripted buildah
The Buildah tutorial builds images without a Dockerfile, using subcommands:
- `buildah from <image>` creates a working container and prints its name (often stored in a shell variable).
- `buildah run $ctr -- <command>` runs a command inside it; `--` ends buildah's own options so the command's flags are not parsed by buildah. The tutorial says `buildah run` is meant for debugging and build-time commands, not for running production containers (use Podman or a CRI service).
- `buildah copy $ctr <src> <dest>` copies files in; `buildah config` sets image metadata such as `--cmd`, `--label`, `--author` and `--created-by`; `buildah commit $ctr <name>` writes the image.
- Rootless use needs the same additional setup as rootless Podman. Mounting a container in rootless mode needs `buildah unshare` first.

## Reusing Ansible roles to build images
The `containers.podman.buildah` connection plugin (part of the containers.podman collection, not ansible-core) runs commands and transfers files in an existing buildah working container. The container is identified by `remote_addr` (default: the inventory hostname, also settable with `ansible_host` or `ansible_buildah_host`), `remote_user` sets the in-container user, and `auto_commit` (default false) can commit changes after successful operations. Create the working container with `buildah from`, add it to inventory with that connection, run the roles, then commit.

## Immutability rules (practitioner guidance)
- Tag with the git commit and never reuse a tag; deploy by digest, because tags can be moved.
- Fix the build and ship a new image rather than patching running containers.
- Rebuild on base-image updates on a schedule, then scan and promote the same image through environments.

## Verify
- [ ] The deployment references the image by digest, and the digest matches the one recorded at build time.

## Checked
Method: docs-checked 2026-11-09 against the Docker build best-practices page, the Buildah intro tutorial (raw GitHub), and the containers.podman buildah connection plugin page. The buildah.io landing page is only a news page and was not relied on.
Removed as unconfirmed: the UBI image sample and exact buildah build/push flags (`--layers`, `--digestfile`), `commit --rm`, `config --user/--port`, the Ansible sample playbook, the ubi-minimal lacks Python remark, the BuildKit/buildah `--secret` and cache-registry gotchas, and the skopeo inspect verification step.
