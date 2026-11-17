---
id: computing-software.cloud-infrastructure-engineering.saltstack.renderers-pipelines-shebang
name: renderers-pipelines-shebang
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, renderers, shebang, pipeline, jinja, yaml, py, text-renderer, data-renderer]
level: practitioner
status: docs-checked
description: "Choose and chain Salt renderers: default jinja|yaml, text vs data renderers, per-file shebang pipelines, and the rule that a pipeline ends in a data renderer."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/renderers/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Renderer pipelines

Renderers turn SLS input into Python data structures. The default is set by the `renderer` option in master or minion config and is `jinja|yaml`.

- Text renderers return strings: aws_kms, cheetah, genshi, gpg, jinja, mako, nacl, pass, py, wempy.
- Data renderers return structures: dson, hjson, json5, json, pydsl, pyobjects, py, stateconf, yamlex, yaml, gpg. `py` and `gpg` can serve either role.

Override per file with a shebang-style first line:

```
#!py
#!jinja|mako|yaml
```

Pipelines chain with `|` and evaluate left to right, each receiving the previous output. A pipeline must end in a data renderer; a text renderer after a data renderer is a mistake, because text renderers do not accept data structures.

A `#!py` file defines `run()` returning a dictionary, equivalent to the matching YAML state.

## Checked

2026-11-09. Read in full the Salt Renderers page (doc/ref/renderers/index.rst, master branch). Completed the renderer lists from the page.

Method: documentation only; no commands were run.
