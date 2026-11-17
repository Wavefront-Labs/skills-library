---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.building-bundles-with-opa-build
name: building-bundles-with-opa-build
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [opa-build, bundles, optimize, entrypoint, bundle-signing]
level: practitioner
status: docs-checked
description: "Build OPA policy bundles with opa build -b, optimise with --optimize and --entrypoint, sign with key flags, and how multiple -b inputs merge under their paths."
sources:
  - https://www.openpolicyagent.org/docs/management-bundles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: package policy and data into a distributable `bundle.tar.gz`.

Basic build from a directory `foo` (the output is named `bundle.tar.gz` by default):

```
ls foo/
example.rego
opa build -b foo/
```

Optimise, which requires an entrypoint given either by flag or by a Rego metadata annotation:

```
opa build -b foo/ --optimize=1 --entrypoint authz/allow
```

`-O` is the short form of `--optimize`.

Sign while building:

```
opa build --verification-key /path/to/public_key.pem --signing-key /path/to/private_key.pem --bundle foo/
```

Several inputs merge into one bundle:

```
opa build -b foo/ -b bar/
```

Each input bundle's files go under the path it was given (`/foo/...` and `/bar/...`) and a new `.manifest` is written at the root of the result. Leading `..` segments are replaced with the name of the directory they refer to, so `opa build -b ../foo/ -b bar/` run from `/src/app` places files under `/src/foo/...` and `/bar/...`.

Bundles served to OPA are then fetched over the Bundle Service API (see bundle-service-configuration). Loaded bundle policy and data are readable through the standard REST API, but by default the REST API refuses to modify content that came from a bundle.

Check: run the build, list the archive contents, and confirm the `.manifest` and your `.rego` files are present at the paths you expect.

## Checked

2026-11-04. Confirmed against the OPA docs Bundles page (docs/management-bundles in the open-policy-agent/opa repo): opa build -b, default bundle.tar.gz name, --optimize/-O with --entrypoint or a metadata annotation, --verification-key and --signing-key, merging of several -b inputs, the REST API refusing to modify bundle content by default. Nothing removed.

Method: documentation only; no commands were run.
