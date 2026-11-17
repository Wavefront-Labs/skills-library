---
id: computing-software.devops-ci-cd.dagger.chaining-export-publish-services
name: chaining-export-publish-services
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, chaining, export, publish, services, as-service, cli]
level: practitioner
status: docs-checked
description: "Export Dagger directories, files and containers to the host, publish containers to a registry, and start containers as host-forwarded services via CLI chaining."
sources: [https://docs.dagger.io/0.21/extending/modules/chaining]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Export, publish and run as a service

Goal: get chained results out of the Dagger DAG (Dagger 0.21 docs). Data flows one way between Dagger operations: edits made to a mounted or copied host directory/file in a container do not return to the host. You must explicitly export.

## Export

`export` works on `Directory`, `File` and `Container` values; the host destination is `--path`.

```shell
dagger -m github.com/kpenfound/dagger-modules/golang@v0.2.1 call \
  build --source=https://github.com/dagger/dagger --args=./cmd/dagger \
  export --path=./my-build
```

- By default a directory export adds files without deleting what already exists at the target. Add `--wipe` to make the host directory match the exported one exactly.
- Single file: chain `file ./dagger` then `export ./my-file` (Shell: `build ... | file ./dagger | export ./my-file`).
- A report file, e.g. `dagger -m github.com/dagger/dagger/modules/ruff call lint --source https://github.com/dagger/dagger report export --path=/tmp/report.json`.
- A container exports as an OCI tarball: `dagger -m github.com/dagger/dagger/modules/wolfi@v0.16.2 call container export --path=./tarball.tar`.

## Publish a container

`Container.publish` takes `--address` and returns a string with the image reference in the registry:

```shell
dagger -m github.com/dagger/dagger/modules/wolfi@v0.16.2 call container publish --address=ttl.sh/my-wolfi
```

Shell: `... | container | publish ttl.sh/my-wolfi`.

## Start a container as a service

`as-service` turns a container into a `Service`; chain `up` to forward its ports to the host (a "programmable docker-compose").

```shell
dagger -c 'github.com/kpenfound/dagger-modules/nginx@v0.1.0 | container | as-service | up'
```

- Default: each port maps to the same host port.
- Custom mapping (host:service): `up --ports=8080:80`; then `curl localhost:8080` returns the NGINX welcome page.
- Random host port: `up --random`.

## Related

computing-software.devops-ci-cd.dagger.chaining-container-operations; computing-software.devops-ci-cd.dagger.function-return-types

## Checked

2026-11-07

Read in full from the docs source: extending/modules/chaining.mdx (export, --wipe, publish, as-service and up sections). Every command, option and the one-way data flow note matched. No corrections needed.

Method: documentation only; no commands were run.
