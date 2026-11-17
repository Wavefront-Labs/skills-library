---
id: computing-software.devops-ci-cd.tilt.tilt-multiple-repos
name: tilt-multiple-repos
category: computing-software
field: devops-ci-cd
product: tilt
tags: [multiple-repos, tilt]
level: practitioner
status: docs-checked
description: "Organise Tiltfiles across many services and repos with load, include, load_dynamic, tilt enable/disable, sibling checkouts, and git_resource."
sources:
  - "https://docs.tilt.dev/multiple_repos.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Many Tiltfiles and many repos

Goal: pull services into one dev environment wherever they are defined. Do NOT restructure your project for Tilt; restructure your Tiltfiles to match your project structure.

## Shared functions: load()

```python
load('../common/Tiltfile', 'VERSION', 'common_config_yaml')

print('Loading version: ', VERSION)
k8s_yaml(common_config_yaml())
```

## Sub-Tiltfiles: include()

`include()` loads files that do not export helper functions:

```python
include('./frontend/Tiltfile')
include('./backend/Tiltfile')
```

## Conditional loading: load_dynamic()

It lacks the nice syntax for loading constants but allows conditional loading:

```python
USE_OAUTH2 = os.path.exists('../.secrets/values-dev.yaml')
USE_TLS = False
if USE_OAUTH2:
  symbols = load_dynamic('../oauth2-proxy/Tiltfile')
  USE_TLS = symbols['USE_TLS']
```

## Running subsets of services

Use one Tiltfile per configuration, or load everything and enable/disable sets:

- `tilt enable a b` enables 'a' and 'b'
- `tilt enable --only a b` enables 'a' and 'b' and disables all others
- `tilt enable --all` enables all services
- `tilt disable a b` disables 'a' and 'b'
- `tilt disable --all` disables all services

For more complicated setups, define your own flags to `tilt up` (see the per-user config guide).

## Other git repositories

Simplest: ask users to check out other repos as a sibling directory.

```python
if not os.path.exists('../backend'):
  fail('Please "git clone" the backend repo in ../backend!')

include('../backend/Tiltfile')
```

Or take the directory from an environment variable:

```python
backend_dir = os.environ.get('BACKEND_REPO_DIR', '../backend')
if not os.path.exists(backend_dir):
  fail('Please "git clone" the backend repo in %s!' % backend_dir)

include(os.path.join(backend_dir, 'Tiltfile'))
```

Alternatively the `git_resource` extension checks out repos from the Tiltfile:

```python
load('ext://git_resource', 'git_checkout')
git_checkout('git@github.com:tilt-dev/tilt-example-html.git#master', '/path/to/local/checkout')
```

Community extensions live in the tilt-extensions repo; teams can also keep their own extension repos.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Many Tiltfiles and Many Repos page in full (library functions, sub-Tiltfiles, conditional loading, to-run vs to-edit, other git repositories, extension repositories). Confirmed `load`, `include`, `load_dynamic`, the five `tilt enable` and `tilt disable` forms, the sibling-checkout and environment-variable patterns and the `git_resource` example. Not opened: the git_resource README and the ClusterAPI link. Nothing removed. 

Method: documentation only; no commands were run.
