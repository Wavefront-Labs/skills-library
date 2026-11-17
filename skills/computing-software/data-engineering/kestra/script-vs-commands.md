---
id: computing-software.data-engineering.kestra.script-vs-commands
name: script-vs-commands
category: computing-software
field: data-engineering
product: kestra
tags: [script-task, commands-task, python, namespace-files, inline-code]
level: intro
status: docs-checked
description: "Choose between Kestra Script tasks with inline code and Commands tasks that run files from namespace files, and how to pass values to each."
sources:
  - https://kestra.io/docs/scripts/commands-vs-scripts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Script tasks embed code inline in the flow YAML. Good for short scripts that need direct access to inputs and outputs; the code is versioned with the flow revision.

```yaml
- id: python
  type: io.kestra.plugin.scripts.python.Script
  beforeCommands:
    - pip install requests kestra
  script: |
    from kestra import Kestra
    import requests
    response = requests.get('https://kestra.io')
    Kestra.outputs({'status': response.status_code})
```

Commands tasks run code kept in separate files, usually namespace files. Better for long or multi-file scripts and shared modules.

```yaml
- id: python
  type: io.kestra.plugin.scripts.python.Commands
  namespaceFiles:
    enabled: true
    include:
      - main.py
  beforeCommands:
    - pip install requests kestra
  commands:
    - python main.py
```

Guidance:

- Script tasks suit quick iteration; the docs recommend Commands for advanced production workloads.
- Long inline scripts are harder to read and test.
- Script tasks can use expressions directly in code; with Commands, pass values as environment variables.

## Checked

2026-11-04. Confirmed against "When to Use Script Tasks vs Commands Tasks" (scripts/commands-vs-scripts): Script versus Commands guidance, advantages and disadvantages, production recommendation, both example flows, expression versus env var value passing. No claims removed.
Method: documentation only; no commands were run.
