---
id: computing-software.devops-ci-cd.tilt.tilt-cli-apply-patch-delete
name: tilt-cli-apply-patch-delete
category: computing-software
field: devops-ci-cd
product: tilt
tags: [cli-apply-patch-delete]
level: practitioner
status: docs-checked
description: "Use tilt apply, tilt patch and tilt delete to create, modify and remove API objects on a running Tilt instance, with their main flags."
sources:
  - "https://docs.tilt.dev/cli/tilt_apply.html"
  - "https://docs.tilt.dev/cli/tilt_patch.html"
  - "https://docs.tilt.dev/cli/tilt_delete.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tilt apply, patch and delete

Goal: change or remove objects on a running Tilt instance from the command line. All three commands talk to the Tilt HTTP server, so they accept `--host` (default `localhost`, overrides TILT_HOST) and `--port` (default 10350, overrides TILT_PORT) if Tilt was started with non-default values.

## tilt apply

Applies a configuration to a resource by filename or stdin.

```
tilt apply (-f FILENAME | -k DIRECTORY)
```

- `-f, --filename`: files, directories or URLs holding the configuration.
- `-k, --kustomize`: process a kustomization directory; cannot be combined with `-f` or `-R`.
- `-R, --recursive`: process the `-f` directory recursively.
- `--server-side`: run the apply in the server instead of the client; `--force-conflicts` forces changes against conflicts.
- `--dry-run`: `none`, `server` or `client`. Client only prints the object that would be sent.
- `--prune`: delete objects not in the configs; use with `-l` or `--all`.
- `-l, --selector`, `--all`, `-o, --output`, `--validate`, `--wait`, `--timeout` are also available.

## tilt patch

Updates fields of a resource using a strategic merge patch, a JSON merge patch or a JSON patch (JSON and YAML accepted). It uses the same semantics as `kubectl patch`.

```
tilt patch (-f FILENAME | TYPE NAME) [-p PATCH|--patch-file FILE]
```

- `--type`: one of `json`, `merge`, `strategic` (default `strategic`).
- `-p, --patch`: the patch inline; `--patch-file`: a file containing the patch.
- `--local`: operate on the content of the file, not the server-side resource.

## tilt delete

Deletes resources by filenames, stdin, resources and names, or by resources and label selector.

```
tilt delete ([-f FILENAME] | [-k DIRECTORY] | TYPE [(NAME | -l label | --all)])
```

- `--all`, `-l, --selector`, `-A, --all-namespaces`, `--field-selector` choose targets.
- `--now`: immediate shutdown, same as `--grace-period=1`.
- `--ignore-not-found`: treat "not found" as success (defaults to true with `--all`).
- `-i, --interactive`: delete only on user confirmation.
- `--wait` (default true) waits for resources to be gone, including finalizers.
- `--cascade`: `background` (default), `orphan` or `foreground`.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/cli/tilt_apply.html, https://docs.tilt.dev/cli/tilt_patch.html, https://docs.tilt.dev/cli/tilt_delete.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Added tilt_patch and tilt_delete pages to sources (resolve) and read them.

Method: documentation only; no commands were run.
