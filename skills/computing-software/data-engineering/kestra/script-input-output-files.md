---
id: computing-software.data-engineering.kestra.script-input-output-files
name: script-input-output-files
category: computing-software
field: data-engineering
product: kestra
tags: [inputfiles, outputfiles, scripts, working-directory, remote-runners]
level: practitioner
status: docs-checked
description: "Pass files into and out of Kestra script tasks with inputFiles and outputFiles, glob versus named files, and path handling on remote task runners."
sources:
  - https://kestra.io/docs/scripts/input-output-files
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`inputFiles` maps filename to content, inline or from namespace files via `read()`:

```yaml
namespaceFiles:
  enabled: true
inputFiles:
  inventory.ini: "{{ read('inventory.ini') }}"
  myplaybook.yml: "{{ read('myplaybook.yml') }}"
```

`outputFiles` persists generated files to internal storage and accepts globs:

```yaml
outputFiles:
  - "*.txt"
```

A later task reads one with `{{ outputs.python_output.outputFiles['myfile.txt'] }}`.

Paths:

- Local runners (Process, Docker): write files by plain name.
- Remote runners (Kubernetes, AWS Batch, Azure Batch and others): the working directory is an execution-specific absolute path. Use `{{ outputFiles["out.txt"] }}`, which resolves to the same value as `{{ workingDir }}/out.txt`.

```yaml
outputFiles:
  - out.txt
commands:
  - echo "Hello" > {{ outputFiles["out.txt"] }}
```

Caveat: only named files work as Pebble expressions. A glob such as `*.csv` is collected after the run but cannot be referenced as `{{ outputFiles["*.csv"] }}`. Declare names for outputs you reference by path.

## Checked

2026-11-04. Confirmed against "Pass Files Into Scripts and Capture Output with inputFiles & outputFiles" (scripts/input-output-files): inputFiles with read() and namespaceFiles, outputFiles with globs, outputs.<task>.outputFiles reference form, local versus remote runner paths, outputFiles[name] equal to workingDir/name, named-files-only limit. No claims removed.
Method: documentation only; no commands were run.
