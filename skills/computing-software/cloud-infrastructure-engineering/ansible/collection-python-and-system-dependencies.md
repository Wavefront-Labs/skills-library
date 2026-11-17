---
id: computing-software.cloud-infrastructure-engineering.ansible.collection-python-and-system-dependencies
name: collection-python-and-system-dependencies
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collections-usage, collection-python-deps, bindep, requirements-txt]
level: practitioner
status: docs-checked
description: "Find and install the Python and system packages collections need, read requirements.txt and bindep.txt in collections, and keep control node, EE and targets aligned."
sources: ["ansible-builder collection-level dependencies (https://github.com/ansible/ansible-builder/blob/devel/docs/collection_metadata.rst)", "ansible-builder execution environment definition (https://github.com/ansible/ansible-builder/blob/devel/docs/definition.rst)", "Collection structure (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collection Python and system dependencies

Collections do not install their Python dependencies: `ansible-galaxy` only installs Ansible content.

## Where the requirements are declared
- `requirements.txt` at the collection root (pip format) for Python packages.
- `bindep.txt` at the collection root (bindep format) for system packages; add profiles such as `[platform:rpm]`.
- Optionally `meta/execution-environment.yml` pointing at other files (`dependencies: {python: meta/ee-requirements.txt, system: meta/ee-bindep.txt}`). Use it when the root `requirements.txt` or `bindep.txt` list anything other than controller-side dependencies, for example test requirements.
- The `requirements:` section of each module's documentation.

## Install for the control node
```bash
COLL=~/.ansible/collections/ansible_collections
python -m pip install -r $COLL/<namespace>/<collection>/requirements.txt   # repeat per collection you use
```

## Who needs them: controller or target?
| Plugin type | Runs on | Install deps on |
|---|---|---|
| filters, lookups, inventory, callbacks | controller | control node / EE |
| cloud/API modules run with `delegate_to: localhost` | controller | control node / EE |
| modules that run on managed hosts | target | the target's Python (`ansible_python_interpreter`) |

## Execution environments
When ansible-builder installs collections into an execution environment it also installs the controller-side Python and system dependencies each collection declares (in `meta/execution-environment.yml`, or by default `requirements.txt` and `bindep.txt` in the collection root). Those files must be inside the published tarball, not in `build_ignore`. Certain packages (test packages and packages that provide Ansible itself) are ignored, and only bindep entries with no profile are installed in the final image (`compile` entries are build-time only). Check what will be picked up with `ansible-builder introspect <collections path>` (add `-v3` to see exclusions).

## Gotchas
- Installing deps into the wrong Python: `ansible --version` shows the controller interpreter; `pip` on PATH may be another one. Use `python -m pip` with that interpreter.
- Version conflicts between collections (two need different versions of one package): resolve with constraints files and test.
- Missing dependencies surface at run time as a module error naming the missing library.

## Verify
```bash
ansible-builder introspect ~/.ansible/collections    # lists the Python and system requirements ansible-builder would collect
```

## Checked

Checked 2026-10-26 against ansible-builder devel documentation (`collection_metadata.rst`, `definition.rst`). Confirmed: default `requirements.txt` and `bindep.txt` locations, `meta/execution-environment.yml` override and its `dependencies` keys, files must not be in `build_ignore`, ignored packages, bindep profile handling, `introspect` and `-v3`. Removed unconfirmed package pins, the `bindep` command line, the error message text and the AWS verification command.

Method: documentation only; no commands were run.
