---
id: computing-software.devops-ci-cd.jenkins.linting-jenkinsfiles
name: linting-jenkinsfiles
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, declarative-linter, linter-api, jenkinsfile-validation, pipeline-model-converter, declarative-linter-cli, jenkins-cli, pre-commit, vscode-jenkins-pipeline-linter, npm-groovy-lint, ci-lint]
level: practitioner
status: docs-checked
description: "Validate Declarative Jenkinsfiles before pushing: the pipeline-model-converter HTTP endpoint, declarative-linter over SSH, editor integrations and pre-commit hooks."
sources: ["https://www.jenkins.io/doc/book/pipeline/development/#linter", "https://www.jenkins.io/doc/book/managing/cli/", "https://github.com/nvuillam/npm-groovy-lint"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linting Jenkinsfiles

The controller's own Pipeline Linter (HTTP or SSH) validates a Jenkinsfile against that controller.

## HTTP endpoint
```bash
JENKINS_URL=https://jenkins.example.com
curl -sf -u "$USER:$API_TOKEN" -X POST \
  -F "jenkinsfile=<Jenkinsfile" "$JENKINS_URL/pipeline-model-converter/validate"
# -> "Jenkinsfile successfully validated." when valid
```
If CSRF protection is enabled, the VS Code connector needs its `crumbUrl` setting.

## SSH
```bash
ssh -p $JENKINS_PORT $JENKINS_HOST declarative-linter < Jenkinsfile
```
The SSH form is documented in the Jenkins pipeline development guide.

## Wiring it in
- **pre-commit** hook calling the curl or ssh command for changed `Jenkinsfile*`. It needs network access and credentials, so consider running it in CI instead.
- **CI job**: lint Jenkinsfile changes on PR in a lightweight job; useful in shared
  library repos holding Jenkinsfile templates.
- Editors: VS Code *Jenkins Pipeline Linter Connector* posts to the same endpoint.
- **npm-groovy-lint**: based on CodeNarc; lints Groovy and Jenkinsfiles and can auto-fix some rules with `--fix`.

## What linting does not catch
See the Limitations section of the Jenkins pipeline development guide. Runtime concerns such as credential IDs, agent labels and `when` conditions are outside what a syntax linter can verify.

## Verify
Introduce a typo in the Jenkinsfile and confirm the linter reports an error; fix it and get `Jenkinsfile successfully validated.`

## Checked
2026-10-28. Confirmed on the Jenkins pipeline development guide: `curl -X POST ... -F "jenkinsfile=<Jenkinsfile" "$JENKINS_URL/pipeline-model-converter/validate"`, `ssh -p $JENKINS_PORT $JENKINS_HOST declarative-linter < Jenkinsfile`, the success message, the `crumbUrl` connector setting. Confirmed in the npm-groovy-lint README: CodeNarc base, Jenkinsfile support, `--fix`.
Removed (not confirmed): the `java -jar jenkins-cli.jar declarative-linter` form and exit-code claim, the crumbIssuer URL, the HTTP 200 claim, the example error text, the pre-commit `stages: [manual]` advice, `npx` invocation, the list of what linting does not catch, and the cross-reference to an unchecked skill.

Method: documentation only; no commands were run.
