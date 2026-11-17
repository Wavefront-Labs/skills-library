---
id: computing-software.cloud-infrastructure-engineering.docker.remote-compose-files-from-git-and-oci
name: remote-compose-files-from-git-and-oci
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-include, remote-include, compose-oci, oci-artifacts, git-remote, compose-file]
level: advanced
status: docs-checked
description: "Run or include Compose applications straight from a Git repository or an OCI registry artifact: URL syntax, pinning refs and digests, caching, prompts and trust considerations."
sources: ["https://docs.docker.com/compose/how-tos/multiple-compose-files/include/", "https://docs.docker.com/reference/compose-file/include/", "https://docs.docker.com/compose/how-tos/oci-artifact/", "https://docs.docker.com/reference/cli/docker/compose/publish/", "https://docs.docker.com/compose/trust-model/", "https://github.com/docker/compose/tree/main/pkg/remote"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote Compose files from Git and OCI

Compose can load Compose files from remote locations instead of a local checkout, both with
`-f` and inside `include` (the include guide says `include` can reference Compose files from
remote sources such as OCI artifacts or Git repositories).

## Git
```bash
docker compose -f https://github.com/org/stack.git#v1.4.0:deploy/compose.yaml up -d
```
```yaml
include:
  - https://github.com/org/platform.git#v2.1.0:postgres/compose.yaml
```
Reference form: `<repository URL>#<ref>:<subdir-or-file>`. The Compose source parses it with
the BuildKit git reference parser, which splits the fragment into a ref (commit, tag or
branch) and a sub-path; an `https` URL must end in `.git`. If the sub-path is a directory,
Compose looks for a default Compose file name in it. The loader resolves the ref with
`git ls-remote`, fetches it with `git fetch --depth=1` and checks it out into a local cache
directory named by the resolved commit, so the `git` client must be installed. Pin a tag or
commit rather than a moving branch for servers.

## OCI artifact
```bash
docker compose -f oci://docker.io/username/my-compose-app:latest up -d
docker compose -f oci://docker.io/username/my-compose-app@sha256:<digest> up -d
```
Artifacts are produced by `docker compose publish` (see
`publishing-compose-apps-as-oci-artifacts`). The Docker docs feature banner requires Compose
2.34.0 or later for OCI artifact applications.

## Behaviour
- Remote resources are downloaded to a local cache. For an OCI artifact Compose prints the
  directory where the resources were stored (for example under the user's cache directory).
- Publishing refuses bind mounts, so remote stacks should use images, named volumes,
  configs and secrets.
- Both remote loaders are enabled by default in the Compose source; setting
  `COMPOSE_EXPERIMENTAL_GIT_REMOTE` or `COMPOSE_EXPERIMENTAL_OCI_REMOTE` to a false value
  disables the corresponding loader (an invalid value is an error).
- Git operations run with prompting disabled by default (`GIT_TERMINAL_PROMPT=0`, and an SSH
  command with `BatchMode=yes` unless you set `GIT_SSH` or `GIT_SSH_COMMAND`), so use
  credentials that work non-interactively.

## Trust
Loading a remote Compose file gives its author control over what runs on your host:
privileged containers, host mounts, `network_mode: host`. Compose asks you to confirm
interpolation variables, environment variables and remote includes when you run an OCI
artifact. Pin by commit or digest, review changes like code, and read the Compose trust
model page.

## Verify
```bash
docker compose -f oci://docker.io/username/my-compose-app:latest config     # inspect before up
```

## Gotchas
- With no network access to the remote at `up` time, the load fails unless the resource is
  already cached.
- Variables that the artifact does not embed (see `publish --with-env`) must be supplied
  locally.

## Checked
Date 2026-10-23. Documentation release: Compose v5.6.1 source (`pkg/remote/git.go`,
`oci.go`) and BuildKit `dfgitutil` git reference parser, plus Docker docs (docker/docs main).
Method: documentation only; no commands were run.
Confirmed in the Compose source: git fragment parsing, `ls-remote` ref resolution, shallow
fetch, default-file lookup in a directory, cache keyed by commit, the two environment
variables (both default to enabled), git non-interactive environment settings; in the BuildKit
parser: the `#ref:subdir` form and the `.git` suffix rule for HTTP(S); in the Docker docs:
remote include sources, OCI usage and prompts, trust model link, 2.34.0 requirement.
Corrected: an earlier claim that remote loaders are gated behind experimental variables
(they are on by default). Removed: the SSH `git@` example (not verified), the `.env` caching
claim and the `ConfigFiles` listing command.
