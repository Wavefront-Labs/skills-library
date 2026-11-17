---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-notebooks-container-images
name: kubeflow-notebooks-container-images
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [container-images, jovyan, s6-overlay, nb-prefix, custom-image]
level: practitioner
status: docs-checked
description: "Pick or build Kubeflow Notebook images: the official image tree, the requirements (port 8888, jovyan user, PVC home), package installs and the s6-overlay startup mechanism."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/notebooks/container-images.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Notebooks container images

The image decides the IDE and the installed packages. Official example images form a tree: `base` leads to `jupyter`, `codeserver` and `rstudio`; Jupyter leads to `jupyter-pytorch`, `jupyter-scipy`, `jupyter-tensorflow`, plus CUDA and `-full` variants; `codeserver-python` and `rstudio-tidyverse` extend their bases.

Requirements for any custom image:
- Expose HTTP on port `8888`; the `NB_PREFIX` environment variable gives the URL path to serve under. Because Kubeflow uses iframes, return `Access-Control-Allow-Origin: *`.
- Run as user `jovyan` with the `jovyan` user home directory and UID `1000`.
- Start with an empty PVC mounted at the jovyan home directory.

The easiest route is to extend a base image.

Packages installed after launch last only as long as the pod unless they live in a PVC-backed directory. Bake packages into a custom image, or install into a PVC path. Warning: `pip install --user` writes into the PVC-backed home and can shadow or conflict with versions in `/opt`.

Linux packages: switch to `root` before `apt-get` and back to `$NB_USER` afterwards.

s6-overlay manages startup and multiple processes (unlike tini, which suits a single PID 1 process):
- Startup scripts go in `/etc/cont-init.d/`, run in ascending order; use `with-contenv` to see container environment variables.
- Extra services go in `/etc/services.d/<name>/` with a `run` script and optional `finish`.
- The example images run s6 as `$NB_USER`, so its files must be owned by that user. To run a service as root, end the Dockerfile with `USER root` and use `s6-setuidgid` for user-facing services.

## Checked

Confirmed the image tree, the port 8888, NB_PREFIX, jovyan and UID 1000 requirements, the PVC home behaviour, the pip install --user warning, the apt-get root switch and the s6-overlay paths and ownership rules. Nothing removed.

Method: docs-checked 2026-11-09 against the raw kubeflow/website notebooks container-images.md page, read in full.
