---
id: computing-software.devops-ci-cd.dagger.api-concepts-and-cli
name: api-concepts-and-cli
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, dagger-api, function-chaining, dagger-cli, dagger-shell, modules]
level: practitioner
status: docs-checked
description: "Compose Dagger workflows by chaining core API functions from dagger shell, dagger core or dagger call, and consume remote modules without installing them."
sources: [https://docs.dagger.io/0.21/getting-started/api, https://docs.dagger.io/0.21/getting-started/api/clients-cli]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger API concepts and CLI calls (Dagger 0.21 docs)

Goal: build a workflow by chaining Dagger API functions from the command line, then reuse module functions from Git.

## Concepts

- A workflow is a sequence of function calls. Each function returns a typed object (`Container`, `Directory`, `File`, `Service`, `Secret`...) and you call that type's functions next. This is function chaining.
- Typed arguments are real engine state, not strings: a `Directory` argument given `https://github.com/dagger/dagger` is the actual filesystem tree, managed by the engine.
- Modules are collections of Dagger Functions; loading one dynamically extends the API, so you can call core functions plus the module's functions.
- Ways to call the API: Dagger CLI (`dagger`, `dagger core`, `dagger call`), a custom app built with an SDK (`dagger run`), a GraphQL client, `curl`, or `dagger query`.

## Same chain, three syntaxes

System shell (heredoc into `dagger`):

```shell
dagger <<EOF
container |
  from alpine |
  file /etc/os-release |
  contents
EOF
```

Dagger CLI equivalent (flags are named after arguments):

```shell
dagger core container \
  from --address=alpine \
  file --path=/etc/os-release \
  contents
```

A build-and-export chain, showing `with-exec` after `--` in shell syntax:

```shell
dagger <<EOF
container |
  from golang:latest |
  with-directory /src https://github.com/dagger/dagger#main |
  with-workdir /src/cmd/dagger |
  with-exec -- go build -o dagger . |
  file ./dagger |
  export ./dagger.bin
EOF
```

## CLI patterns from the page

- Interactive container, like `docker run`: `dagger -c 'container | from cgr.dev/chainguard/wolfi-base | terminal'`.
- Core API only, faster startup: pass `-M` (`--no-mod`); `dagger -M` equals `dagger core`.
- Call a module's auto-generated function: `dagger call container-echo --string-arg="Welcome to Dagger!" stdout`. All names are converted to kebab-case.
- Call a remote module without installing: `dagger -m github.com/jpadams/daggerverse/trivy@v0.5.0 call scan-image --image-ref=ubuntu:latest` (shell form: `github.com/jpadams/daggerverse/trivy@v0.5.0 | scan-image ubuntu:latest`).
- Discover functions: `dagger -m <module> call --help`, or in shell `.help <module>`. Arguments of one function: `dagger -m <module> call scan-image --help`.
- Publish a container: `dagger core container from --address="alpine:latest" with-entrypoint --args="cat","/etc/os-release" publish --address="ttl.sh/my-alpine"`.

## Notes

- The CLI can call functions from the local filesystem or a remote Git repo; no other infrastructure is required.
- The Daggerverse (daggerverse.dev) indexes public modules.

Related: computing-software.devops-ci-cd.dagger.graphql-http-clients, computing-software.devops-ci-cd.dagger.sdk-module-init-develop.

## Checked

2026-11-07

Read in full from the docs source: getting-started/api.mdx and getting-started/api/clients-cli.mdx. Every example, flag (-M / --no-mod, -m, --help), kebab-case note and the remote trivy module call matched. No corrections needed.

Method: documentation only; no commands were run.
