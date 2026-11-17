---
id: computing-software.devops-ci-cd.jenkins.jenkinsfile-editor-integration
name: jenkinsfile-editor-integration
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jenkinsfile-vscode, intellij-gdsl, pipeline-linter]
level: intro
status: docs-checked
description: "Edit Jenkinsfiles with fast feedback: VS Code Jenkins Pipeline Linter Connector, IntelliJ GDSL completion from your controller, and pre-commit validation."
sources: ["https://www.jenkins.io/doc/book/pipeline/development/#linter", "https://www.jenkins.io/doc/book/pipeline/development/#ide-integrations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editor integration for Jenkinsfiles

## VS Code
- Extension "Jenkins Pipeline Linter Connector" posts the open file to
  `<jenkins>/pipeline-model-converter/validate` and shows errors. Settings:
  `jenkins.pipeline.linter.connector.url`, `.user`, `.pass` (use an API token), `.crumbUrl` if needed.

## Other editors
The Jenkins pipeline development guide lists IDE integrations: Eclipse (Jenkins Editor), Visual Studio Code (Jenkins Pipeline Linter Connector), Neovim (nvim-jenkinsfile-linter), Atom (linter-jenkins) and Sublime Text (Jenkinsfile package).

## Pre-commit lint (any editor)
```bash
curl -fsS -X POST -u "$JENKINS_USER:$JENKINS_TOKEN" \
  -F "jenkinsfile=<Jenkinsfile" "$JENKINS_URL/pipeline-model-converter/validate"
```
Prints "Jenkinsfile successfully validated." when the file is valid.

## Gotchas
- Do not commit API tokens in workspace settings; use user settings or env vars.

## Verify
- [ ] Introducing a typo in a stage directive shows an error in the editor.

## Checked
2026-10-28. Confirmed on the Jenkins pipeline development guide: POST to `/pipeline-model-converter/validate` with `jenkinsfile=<Jenkinsfile`, the success message, the VS Code Jenkins Pipeline Linter Connector settings `jenkins.pipeline.linter.connector.user`, `.pass` and `.crumbUrl` (needed when CSRF protection is on), and the list of IDE integrations.
Removed (not confirmed): the `files.associations` tip, the IntelliJ GDSL steps and URL, the claim that only declarative syntax is validated, and the gotcha about differing plugin sets.

Method: documentation only; no commands were run.
