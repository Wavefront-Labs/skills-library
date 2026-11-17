---
id: computing-software.devops-ci-cd.argo-workflows.container-args-offloading
name: container-args-offloading
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [container-args-offload, argo-container-args-file, at-filename-syntax, emissary-args, e2big]
level: advanced
status: docs-checked
description: "Understand automatic offload of container args above 128KB into a ConfigMap and per-argument files using the at-filename syntax your program must support."
sources: ["https://argo-workflows.readthedocs.io/en/latest/offloading-large-workflows/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container arguments offloading
Very large container arguments are offloaded automatically, with no workflow changes.

Stage 1, total args over 128KB (131,072 bytes of marshaled JSON): the controller stores them in a ConfigMap under key `ARGO_CONTAINER_ARGS_FILE`, mounts it at `/argo/config/`, sets env var `ARGO_CONTAINER_ARGS_FILE` to `/argo/config/ARGO_CONTAINER_ARGS_FILE` and clears the args in the pod spec. The emissary executor reads and applies them at runtime.

Stage 2, any single argument over 128KB, which would still trigger the exec "argument list too long" (E2BIG) error: the emissary writes it to `/tmp/argo_arg_N.txt` and replaces the argument with `@/tmp/argo_arg_N.txt`. Your program must support `@filename`: detect an argument starting with `@`, read the file at the following path, and use the contents as the value.

If it cannot, either add that expansion, keep arguments under 128KB, or pass input another way (environment variables, mounted ConfigMaps).

Log evidence:
- controller: `Offloaded container args to configmap. Args >128KB will use @filename syntax container=...`
- emissary: `Reading container args from file argsFile=...`, `Loaded container args from file count=5`, and `Offloaded large argument to file ... argIndex=1 size=140000 filePath=/tmp/argo_arg_1.txt`

If offload does not seem to happen, check the thresholds (both 131,072 bytes) and search those log messages.

## Checked
2026-11-03. Confirmed against the Offloading Large Workflows page (Container Arguments Offloading section): the 128KB (131,072 byte) thresholds, ConfigMap key, mount path, env var, `/tmp/argo_arg_N.txt` replacement, program requirements, options and log lines.
Method: documentation only; no commands were run.
