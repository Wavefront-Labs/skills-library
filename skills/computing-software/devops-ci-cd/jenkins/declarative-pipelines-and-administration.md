---
id: computing-software.devops-ci-cd.jenkins.declarative-pipelines-and-administration
name: declarative-pipelines-and-administration
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jenkinsfile, declarative-pipeline, scripted-pipeline, groovy, ci, cd, ci-cd, agents, controller, build-agents, kubernetes-plugin, docker-agent, shared-libraries, multibranch-pipeline, credentials, withcredentials, plugins, plugin-management, jcasc, configuration-as-code, lts, parallel-stages, timeout, input-step, blue-ocean, replay]
level: practitioner
status: docs-checked
description: "Run Jenkins sanely: declarative Jenkinsfiles with agents, parallel stages and credentials, shared libraries, no builds on the controller, and safe plugin/LTS upkeep."
sources: ["https://www.jenkins.io/doc/book/pipeline/syntax/", "https://www.jenkins.io/doc/book/pipeline/docker/", "https://www.jenkins.io/doc/book/pipeline/shared-libraries/", "https://www.jenkins.io/doc/book/pipeline/development/", "https://www.jenkins.io/doc/book/security/controller-isolation/", "https://github.com/jenkinsci/configuration-as-code-plugin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jenkins — declarative pipelines and administration

**Goal:** pipelines defined in a `Jenkinsfile` in the repo, run on disposable agents,
with a controller that you can upgrade without fear.

## 1. A baseline declarative Jenkinsfile
```groovy
pipeline {
  agent none
  options {
    timeout(time: 30, unit: 'MINUTES')
    buildDiscarder(logRotator(numToKeepStr: '30'))
    disableConcurrentBuilds(abortPrevious: true)
    timestamps()
  }
  stages {
    stage('Build') {
      agent { docker { image 'maven:3.9-eclipse-temurin-21'; args '-v $HOME/.m2:/root/.m2' } }
      steps {
        sh 'mvn -B verify'
      }
      post { always { junit '**/target/surefire-reports/*.xml' } }
    }
    stage('Checks') {
      parallel {
        stage('Lint')  { agent { label 'linux' } steps { sh './lint.sh' } }
        stage('Audit') { agent { label 'linux' } steps { sh './audit.sh' } }
      }
    }
    stage('Deploy') {
      when { branch 'main' }
      agent { label 'deploy' }
      steps {
        input message: 'Deploy to production?', ok: 'Deploy'   // see gotcha below
        withCredentials([string(credentialsId: 'prod-deploy-token', variable: 'TOKEN')]) {
          sh './deploy.sh'      // reads $TOKEN from env; never echo it
        }
      }
    }
  }
}
```
- Use a **Multibranch Pipeline** (or Organization Folder) job so every branch/PR with a
  `Jenkinsfile` gets a job automatically.
- Some options come from plugins (the syntax reference names `timestamps`); `docker` agents
  need the Docker Pipeline plugin and a Docker-capable agent.
- **Gotcha — `input` holds an executor:** an `input` inside a stage that has an agent
  keeps that agent busy while waiting. Use the stage-level `input {}` directive, which pauses
  before entering the stage's `agent` block (or a stage with no agent), and wrap it in a `timeout`.
- **Gotcha — credential interpolation:** use single quotes `sh './deploy.sh'` or
  `sh 'curl -H "Authorization: $TOKEN" ...'` so the *shell* expands the secret. Double-quoted
  Groovy strings (`"... ${TOKEN}"`) interpolate it in Groovy, and the Jenkinsfile docs mark that
  as wrong because process listings can disclose the value.

## 2. Keep work off the controller
Set the built-in node's executors to **0** (*Manage Jenkins › Nodes › Built-In Node*).
The controller-isolation guide recommends not building on the built-in node, since an agent or
build there is closer to controller data. Run agents as:
- **Kubernetes plugin** pods (one pod per build, defined in `podTemplate` or a YAML in
  the repo) — the usual choice today;
- inbound (JNLP/WebSocket) or SSH agents on VMs, labelled (`linux`, `windows`, `gpu`);
- cloud plugins (EC2 etc.) for autoscaled VMs.

## 3. Shared libraries
Repo layout: `vars/buildApp.groovy` (global steps, `def call(Map cfg) { ... }`),
`src/org/acme/...` (classes), `resources/`. Register under *Manage Jenkins › System ›
Global Trusted Pipeline Libraries*, then `@Library('acme-lib@v3') _` at the top of the
Jenkinsfile. Pin to a tag, not `main`, so a library change can't break every build at once.
A library marked trusted can run any Java, Groovy, Jenkins-internal or plugin methods, and the
docs warn that anyone able to push to its repository could obtain unlimited access to Jenkins;
restrict pushes. Configuring them needs the Overall/RunScripts permission.

## 4. Configuration as code and plugins
- Use the **Configuration as Code (JCasC)** plugin: a `jenkins.yaml` (pointed to by
  `CASC_JENKINS_CONFIG`) defines security realm, clouds, credentials references and tools,
  so the controller is reproducible.
- Pin plugins in `plugins.txt` and install with `jenkins-plugin-cli --plugin-file plugins.txt`
  when building a controller image.
- Track the **LTS** line rather than weekly releases. Upgrade procedure: back up `$JENKINS_HOME`
  (or snapshot the volume) → upgrade core in a staging copy → update plugins there →
  run a few representative pipelines → promote (see `backup-restore-and-lts-upgrades`).
- Fewer plugins means a smaller attack surface and less upgrade work. Remove unused ones and
  read the Jenkins security advisories for those you keep.

## 5. Debugging
- *Replay* on a build lets you edit the Jenkinsfile for one run without committing.
- *Pipeline Syntax* (snippet generator) at `<job>/pipeline-syntax` gives exact step syntax
  for installed plugins.
- Validate before running: `curl -X POST --user "$JENKINS_AUTH" -F "jenkinsfile=<Jenkinsfile" "$JENKINS_URL/pipeline-model-converter/validate"`
  (the Command-line Pipeline Linter in the Pipeline development docs; a Jenkins CLI command exists too).
- "Scripts not permitted to use method …" → script security sandbox; move logic into a
  trusted shared library rather than blanket-approving signatures.

## Verify
- [ ] Built-in node has 0 executors; builds land on labelled or pod agents.
- [ ] Every pipeline has a `timeout` and build discarder.
- [ ] Secrets only via `withCredentials`/`credentials()`, with single-quoted `sh`.
- [ ] Shared library is referenced by tag.
- [ ] Controller config is in JCasC + `plugins.txt`, and an upgrade was rehearsed on a copy.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed: declarative `options` (`buildDiscarder(logRotator(...))`, `timestamps`, `disableConcurrentBuilds(abortPrevious: true)`), `docker` agent with `args '-v $HOME/.m2:/root/.m2'` (Pipeline docker page), stage `input` directive, Docker Pipeline plugin requirement, trusted library warning and Overall/RunScripts requirement (Shared Libraries), the command-line linter endpoint (Pipeline development page), `CASC_JENKINS_CONFIG` (JCasC README), Built-In Node with 0 executors (controller isolation). Removed the unconfirmed `-ntp` Maven flag and upgrade-skew claims.
Method: documentation only; no commands were run.
