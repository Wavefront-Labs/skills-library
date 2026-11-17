---
id: computing-software.devops-ci-cd.tilt.tilt-extensions
name: tilt-extensions
category: computing-software
field: devops-ci-cd
product: tilt
tags: [extensions, tilt, tiltfile, load]
level: practitioner
status: docs-checked
description: "Load and share Tiltfile code: ext:// extensions, relative load(), load_dynamic, custom extension repos, and CLI debugging of extension loading."
sources:
  - "https://docs.tilt.dev/extensions.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tilt extensions

Goal: share Tiltfile functionality (tool-version checks, build or deploy scripts, custom buttons) across repos.

## Use one

```python
load('ext://hello_world', 'hi')
hi()
```

Tilt checks out the tilt-extensions repo in the background, reads `hello_world/Tiltfile`, and binds `hi` locally.

## Single repo: no extension needed

```python
load('./common/Tiltfile', 'hi')
```

For more flexible scripting:

```python
symbols = load_dynamic('./common/Tiltfile')
hi = symbols.get('hi')
```

## Default repo, spelled out (Tilt v0.25+)

`load('ext://hello_world', 'hi')` is shorthand for:

```python
v1alpha1.extension_repo(name='default', url='https://github.com/tilt-dev/tilt-extensions')
v1alpha1.extension(name='hello_world', repo_name='default', repo_path='hello_world')
load('ext://hello_world', 'hi')
```

A local repo uses `file:///` with an absolute path, for experimentation only.

## Your own repo

Pin a fork by tag:

```python
v1alpha1.extension_repo(name='default', url='https://github.com/my-org/tilt-extensions', ref='v0.25.0')
```

Or add a repo alongside the default and point an extension at it with `repo_name='my-repo'`. For a private repo, configure git auth in the background, for example in `~/.gitconfig`:

```
[url "ssh://git@github.com/"]
	insteadOf = https://github.com/
```

## Debugging

```bash
tilt get extensionrepo
tilt get extensionrepo default -o jsonpath='{.status}{"\n"}' | jq
tilt get extension
tilt get extension hello_world -o jsonpath='{.status}{"\n"}' | jq
```

Status shows checkoutRef, lastFetchedAt and the on-disk path.

## Upgrading

Before v0.25.0 extensions were downloaded into a `tilt_modules` directory next to the Tiltfile. From v0.25.0 they are stored in the XDG data directory, customisable with the XDG environment variables.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/extensions.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
