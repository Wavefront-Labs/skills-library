---
id: computing-software.devops-ci-cd.tilt.tilt-buttons
name: tilt-buttons
category: computing-software
field: devops-ci-cd
product: tilt
tags: [buttons, tilt]
level: practitioner
status: docs-checked
description: "Add custom buttons with local commands and checkbox or text inputs to the Tilt web UI using the uibutton extension's cmd_button."
sources:
  - "https://docs.tilt.dev/buttons.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom UI buttons

Goal: add a button to the Tilt web UI that runs a local command when clicked, optionally taking input from the UI. This is lighter-weight than a `local_resource`. The simplest route is the `uibutton` extension; more complex cases can create buttons directly via Tilt's API.

## Button on a resource

```python
load('ext://uibutton', 'cmd_button')
cmd_button('letters:yarn install',
           argv=['sh', '-c', 'cd letters && yarn install'],
           resource='letters',
           icon_name='cloud_download',
           text='yarn install',
)
```

The button appears in the table view and the resource view, and its logs go into the "letters" resource's logs.

## Checkbox input

```python
load('ext://uibutton', 'cmd_button', 'bool_input', 'location')
cmd_button('migrate db',
           argv=['sh', '-c', 'yarn run db:migrate $DRY_RUN'],
           location=location.NAV,
           icon_name='developer_board',
           text='Run database migration',
           inputs=[
             bool_input('DRY_RUN', true_string='--dry-run', false_string=''),
           ],
)
```

`bool_input` adds a checkbox and sets the `$DRY_RUN` environment variable to `true_string` or `false_string`. Invoke via `sh -c` so the shell expands the variable; this is only needed when `argv` itself needs shell expansion.

## Text input

```python
load('ext://uibutton', 'cmd_button', 'text_input', 'location')
cmd_button('hello',
           argv=['sh', '-c', 'echo Hello, $NAME'],
           location=location.NAV,
           icon_name='front_hand',
           text='Hello!',
           inputs=[
             text_input('NAME'),
           ],
)
```

## Exec in a pod

The page's example uses two `text_input`s (`resource`, `command`) and a script that finds the pod with `tilt get kubernetesdiscovery "$resource" -ojsonpath='{.status.pods[0].name}'`, then runs `kubectl exec "$POD_NAME" -- $command`. It suggests putting a long script in a separate file.

See the uibutton README (tilt-extensions) for usage specifics.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/buttons.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Changed `$DRYRUN` to `$DRY_RUN` in the example so it matches the variable the prose describes.

Method: documentation only; no commands were run.
