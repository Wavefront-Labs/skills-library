---
id: computing-software.devops-ci-cd.jenkins.tools-directive-and-global-tool-configuration
name: tools-directive-and-global-tool-configuration
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, tools-directive, global-tool-configuration, tool-installers, maven, jdk, gradle, nodejs, tool-step, declarative-pipeline, jcasc, path]
level: practitioner
status: docs-checked
description: "Use the declarative tools directive: define JDK/Maven/Gradle/NodeJS installations in Global Tool Configuration or JCasC, reference them by name, and know when containers beat it."
sources: ["https://www.jenkins.io/doc/book/pipeline/syntax/#tools", "https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps/#tool-use-a-tool-from-a-predefined-tool-installation", "https://plugins.jenkins.io/configuration-as-code/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The `tools` directive

**Goal:** a stage gets an exact JDK/Maven/Node version on `PATH` without baking it into
every agent image by hand.

## 1. Define the installation (once, on the controller)
*Manage Jenkins → Tools* (older: *Global Tool Configuration*). Each entry has a **name**
(what pipelines reference) and either a fixed home path or an *Install automatically*
installer (downloaded and extracted on the agent on first use).

Same thing as code: JCasC has a `tool:` root with per-tool `installations` (name,
home or installer properties). Export the live config (*Manage Jenkins → Configuration
as Code*) to get the exact installer keys for your plugin versions instead of guessing.

## 2. Use it in a Jenkinsfile
```groovy
pipeline {
  agent { label 'linux' }
  tools {
    jdk   'jdk21'          // type keyword + configured NAME, not a version
    maven 'maven-3.9'
  }
  stages {
    stage('Build') { steps { sh 'java -version && mvn -B verify' } }
  }
}
```
- Supported type keywords per the Pipeline syntax reference: `maven`, `jdk`, `gradle`.
  Use the *Declarative Directive Generator → tools* to see what your controller supports.
- Allowed inside the `pipeline` block or a `stage` block; it puts the tools on the `PATH`.
  The name must be pre-configured under *Manage Jenkins → Tools*.
- Scripted equivalent: `def mvnHome = tool 'maven-3.9'` then
  `withEnv(["PATH+MAVEN=${mvnHome}/bin"]) { sh 'mvn -v' }`.

## 3. When not to use it
- `agent { docker { image 'maven:3.9-eclipse-temurin-21' } }` or a Kubernetes pod
  container already has the toolchain; `tools` would install a second copy. Prefer images
  for ephemeral agents.
- `tools` is ignored if `agent none` is specified.

## Failure modes
- "Tool type ... does not have an install of ... configured" -> name mismatch; use the
  name you gave the installation, not the version.
- First build on a fresh agent is slow (download); cache via a persistent agent volume
  or pre-bake into the agent image.
- Installer download blocked by proxy / air gap -> use a fixed `home` path on a
  pre-provisioned image, or an *Extract *.zip/*.tar.gz* installer pointing at an
  internal artifact URL.

## Verify
`sh 'which java; java -version'` in the stage prints the tool's path, not the system Java.

## Checked
2026-11-02. Confirmed against the Pipeline syntax reference (tools directive: supported tools maven, jdk, gradle; allowed in pipeline or stage; tools ignored with agent none; names pre-configured under Manage Jenkins > Tools) and the Pipeline steps reference (tool step). Removed: JCasC installer keys and versions, download hosts and install path, M2_HOME claim, plugin-added tool types, PATH shadowing, exact error text.
Method: documentation only; no commands were run.
