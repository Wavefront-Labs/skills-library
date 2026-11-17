---
id: computing-software.devops-ci-cd.tekton.tekton-task-scripts-in-steps
name: tekton-task-scripts-in-steps
category: computing-software
field: devops-ci-cd
product: tekton
tags: [task, steps, script, shebang]
level: intro
status: docs-checked
description: "Write script bodies in Tekton Task steps, including the default sh preamble, shebang overrides for bash, Python or Node, and the script versus command rule."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/tasks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A step may set `script` instead of `command`; the two cannot both be present. The script runs as if stored in the container image, and any `args` are passed to it.

A script without a shebang gets this preamble prepended:

```bash
#!/bin/sh
set -e
```

Override it by starting the script with a shebang for a parser that exists in that step image:

```yaml
steps:
  - image: ubuntu # contains bash
    script: |
      #!/usr/bin/env bash
      echo "Hello from Bash!"
  - image: python
    script: |
      #!/usr/bin/env python3
      print("Hello from Python!")
  - image: node
    script: |
      #!/usr/bin/env node
      console.log("Hello from Node!")
```

Scripts can call files placed in the workspace (for example `/workspace/my-script.sh`) or binaries inside the image (`/bin/my-binary`). The doc also has a separate section for Windows scripts. Because `set -e` is only in the default preamble, a custom shebang script does not stop on the first failing command unless you add that yourself.

## Checked

Checked 2026-11-08 against docs/tasks.md in tektoncd/pipeline (main), reading the Running scripts within Steps section and the Windows scripts subsection (partial read of a long file). Confirmed script versus command exclusivity, the default sh preamble with set -e, shebang overrides, workspace and image binary examples, and the Windows section. No changes needed to claims.

Method: documentation only; no commands were run.
