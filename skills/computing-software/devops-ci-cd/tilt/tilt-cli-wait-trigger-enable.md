---
id: computing-software.devops-ci-cd.tilt.tilt-cli-wait-trigger-enable
name: tilt-cli-wait-trigger-enable
category: computing-software
field: devops-ci-cd
product: tilt
tags: [cli-wait-trigger-enable]
level: practitioner
status: docs-checked
description: "Control a running Tilt with tilt wait, trigger, enable and disable: wait on conditions, force updates, and switch resources on or off."
sources:
  - "https://docs.tilt.dev/cli/tilt_wait.html"
  - "https://docs.tilt.dev/cli/tilt_trigger.html"
  - "https://docs.tilt.dev/cli/tilt_enable.html"
  - "https://docs.tilt.dev/cli/tilt_disable.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tilt wait, trigger, enable, disable

Goal: script a running Tilt instance. Each command accepts `--host` (default `localhost`) and `--port` (default 10350) for a Tilt started with non-default values.

## tilt wait (experimental)

Waits until a condition is seen in the Status field of every given resource, then prints a success message to stdout.

```
tilt wait ([-f FILENAME] | resource.group/resource.name | resource.group [(-l label | --all)]) [--for=delete|--for condition=available]
```

```
# Wait for the tiltfile to load.
tilt wait --for=condition=Ready "uiresource/(Tiltfile)"

# When used with a Kubernetes resource, waits for the pod
# to deploy, start running, and pass all readiness probes.
tilt wait --for=condition=Ready "uiresource/my-kubernetes-deployment"
```

- `--for`: `create`, `delete`, `condition=condition-name[=condition-value]` or `jsonpath='{JSONPath expression}'=[JSONPath value]`. Default condition-value is true.
- `--timeout`: default 30s; zero checks once without waiting; negative waits a week.
- Selection: `-l, --selector`, `--all`, `--field-selector`, `-A, --all-namespaces`.

## tilt trigger

```
tilt trigger [RESOURCE_NAME]
```

If the resource has Trigger Mode: Manual and has pending changes, the pending changes are applied. Otherwise it forces a full rebuild.

## tilt enable

```
tilt enable {-all | [--only] <resource>...}
```

```
tilt enable frontend backend          # enable these
tilt enable --only frontend backend   # enable these, disable all others
tilt enable --all                     # enable everything
```

`-l, --labels` enables all resources with the given labels.

## tilt disable

```
tilt disable {-all | <resource>...}
```

```
tilt disable frontend backend
tilt disable --all
```

`-l, --labels` disables all resources with the given labels.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/cli/tilt_wait.html, https://docs.tilt.dev/cli/tilt_trigger.html, https://docs.tilt.dev/cli/tilt_enable.html, https://docs.tilt.dev/cli/tilt_disable.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Added tilt_trigger, tilt_enable and tilt_disable pages to sources (resolve) and read them.

Method: documentation only; no commands were run.
