---
id: computing-software.devops-ci-cd.earthly.earthly-import-targets
name: earthly-import-targets
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, import, build, copy, from, remote-target, wildcard-builds, wildcard-copy]
level: practitioner
status: docs-checked
description: "Reference targets and artifacts in Earthly from the same Earthfile, another directory or a remote repo, using the IMPORT command, inline references, and experimental globbing."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/importing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Importing targets and artifacts in Earthly

Goal: connect targets across Earthfiles, directories and repos so build code is reused.

## Same Earthfile

Target reference is `+name`; artifact reference is the target ref plus `/path`:

```Dockerfile
target1:
    RUN echo "Hello World" > out.txt
    SAVE ARTIFACT out.txt

target2:
    BUILD +target1
    COPY +target1/out.txt ./
```

## Other repository: IMPORT

`IMPORT` takes an Earthfile reference and an optional alias:

```Dockerfile
IMPORT github.com/earthly/hello-world:main AS hello-world

my-target:
    BUILD hello-world+hello
    COPY hello-world+hello/hello.txt ./
```

`BUILD` just issues the build of the target; `COPY` brings in artifacts and `FROM` brings in images. The `AS` part is optional and only needed when the alias should differ from the repository name (with no alias, `IMPORT github.com/earthly/earthly/buildkitd` gives the alias `buildkitd`, and `IMPORT github.com/earthly/earthly:v0.8.13` gives `earthly`).

## Other directory

Same as a repo, but the reference is a relative path:

```Dockerfile
IMPORT ./some/other/dir AS other-dir

my-target:
    BUILD other-dir+my-target
    COPY other-dir+my-target/out.txt ./
```

## Inline, no IMPORT

```Dockerfile
BUILD github.com/earthly/hello-world:main+hello
COPY ./some/other/dir+my-target/out.txt ./
```

## Wildcards (experimental)

In `BUILD` a target ref and in `COPY` an artifact ref may contain a glob such as `./parent/*+<target-name>` or `./parent/*+<target-name>/<artifact-path>`. Enable with `VERSION --wildcard-builds 0.8` (for `BUILD`) or `VERSION --wildcard-copy 0.8` (for `COPY`).

## Gotcha

Local paths in references must start with `./`, `../` or `/`, on any OS including Windows; relative paths are recommended for portability.

## Checked

2026-11-07. Read docs/guides/importing.md in full. IMPORT with and without AS, the buildkitd and earthly default aliases, inline references, wildcard flags and the ./ ../ / path rule match. Nothing removed.
Method: documentation only; no commands were run.
