---
id: computing-software.devops-ci-cd.dagger.ci-workflow-quickstart
name: ci-workflow-quickstart
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, ci, quickstart, dagger-init, functions, publish, as-service, build-env, sdk]
level: practitioner
status: docs-checked
description: "Daggerize an app: dagger init with an SDK, write build, test, publish and build-env functions, run them from Dagger Shell, and serve the built image locally."
sources: [https://docs.dagger.io/0.21/getting-started/quickstarts/ci/, https://docs.dagger.io/0.21/getting-started/quickstarts/basics, https://docs.dagger.io/0.21/introduction/core-concepts/functions, https://docs.dagger.io/0.21/introduction/features/programmability]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build a CI workflow with Dagger functions

Goal: replace ad hoc CI scripts with a Dagger module run identically locally and in CI (Dagger 0.21 docs).

## Setup

Needs the Dagger CLI, Git and a container runtime. The quickstart uses a Vue app from the `dagger/hello-dagger-template` GitHub template:
```shell
gh repo create hello-dagger --template dagger/hello-dagger-template --public --clone
cd hello-dagger
dagger init --sdk=go --name=hello-dagger     # or python, typescript, php, java
dagger functions                             # shows generated container-echo and grep-dir
```
`dagger init` creates `dagger.json` and a `.dagger` directory with example functions. Optional: `dagger login` links Dagger Cloud for traces.

## The four functions (Go form)

Replace `.dagger/main.go` (Python: `.dagger/src/hello_dagger/main.py`; TypeScript: `.dagger/src/index.ts`):
- `BuildEnv(source)`: `From("node:21-slim")`, `WithDirectory("/src", source)`, `WithMountedCache("/root/.npm", dag.CacheVolume("node"))`, `WithWorkdir("/src")`, `WithExec({"npm","install"})`.
- `Test(ctx, source)`: BuildEnv then `WithExec({"npm","run","test:unit","run"})`, returns `Stdout`.
- `Build(source)`: BuildEnv, `npm run build`, take `./dist`, copy into `nginx:1.25-alpine` at `/usr/share/nginx/html`, `WithExposedPort(80)`.
- `Publish(ctx, source)`: calls `Test`, then `Build(source).Publish(ctx, "ttl.sh/hello-dagger-<random>")`.

Every `source` argument is annotated `// +defaultPath="/"` (Python `DefaultPath("/")`), so the repo root is supplied automatically.

## Run

In Dagger Shell (`dagger`):
```shell
publish                                   # tests, builds, publishes
build-env | terminal --cmd=bash           # shell inside the build environment
build | as-service | up --ports=8080:80   # serve at http://localhost:8080
```
Without the shell, call functions with `dagger call`. Container port 80 is remapped to host 8080 because port 80 is often privileged.

## Function patterns (core-concepts)

Build functions return a Container; test functions return `Stdout`; generate functions return a `Changeset` via `dir.Changes(source)`. Functions return just-in-time artifacts (Container, File, Directory) you can keep chaining, e.g. return `*dagger.File` via `.File("/src/build/hello")` and export it.

## Next

Add a check (`computing-software.devops-ci-cd.dagger.checks-create`) and run `dagger check` in CI.

## Checked

2026-11-07

Read in full from the docs source: getting-started/quickstarts/ci/index.mdx with the Go snippet (main.go) and the Python snippet, introduction/core-concepts/functions.mdx, and introduction/features/programmability.mdx with its programmability-2 Go snippet (File("/src/build/hello")). Confirmed the init commands, the four functions, image names and tags, ttl.sh publish, defaultPath annotations, the Shell commands, the port 80 to 8080 mapping and the function patterns. No corrections needed.

Method: documentation only; no commands were run.
