---
id: computing-software.data-science-and-analytics.jupyter-notebooks.register-venv-kernel
name: register-venv-kernel
category: computing-software
field: data-science-and-analytics
product: jupyter-notebooks
tags: [ipykernel-install, jupyter-kernelspec, notebook-environment, jn-kernels-environments]
level: practitioner
status: docs-checked
description: "Install ipykernel in a project environment and register a uniquely named kernel so notebooks run against the right dependencies."
sources:
  - https://ipython.readthedocs.io/en/stable/install/kernel_install.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-project kernel
```bash
# with the project's environment active
python -m pip install ipykernel
python -m ipykernel install --user --name myproj --display-name "Python (myproj)"
```
Conda variant:
```bash
conda create -n py312 python=3.12 ipykernel
conda activate py312
python -m ipykernel install --user --name py312 --display-name "Python 3.12"
```
## Gotchas
- Give each environment a unique `--name`; the name is used by Jupyter internally and installing again with the same name overwrites the existing kernel. `--display-name` is what shows in the notebook menus.
- Run the install with the Python of the environment you want the kernel to use; the spec is written for the current Python installation.
- To expose a kernel from one env to Jupyter in another, run `ipykernel install --prefix=/path/to/jupyter/env --name 'python-my-env'` from the kernel's env.
- Kernel spec files are JSON and can be edited. To edit before installing: `ipython kernel install --prefix /tmp`, edit `/tmp/share/jupyter/kernels/python3`, then `jupyter kernelspec install /tmp/share/jupyter/kernels/python3`.
- In a conda env using pip for ipykernel, make sure pip is installed in that env first.
- `jupyter --paths` shows the locations kernel configuration can land (system-wide, Jupyter's env, per-user).
## Verify
- [ ] The new kernel name appears in the notebook's kernel menu with the intended display name.

## Checked

2026-11-09. Confirmed against the IPython kernel install page: ipykernel install flags, unique names, overwrite behaviour, --prefix, kernelspec editing, conda variant, jupyter --paths. Removed: venv creation lines, `jupyter kernelspec list`/`remove`, the `%pip` versus `!pip` gotcha, restart-kernel advice and the sys.executable check (not on this page).
Method: docs-checked 2026-11-09 against the IPython kernel install page.
