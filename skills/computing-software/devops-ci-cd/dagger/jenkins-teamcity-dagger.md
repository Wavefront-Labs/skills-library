---
id: computing-software.devops-ci-cd.dagger.jenkins-teamcity-dagger
name: jenkins-teamcity-dagger
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, jenkins, teamcity, ci, kotlin-dsl, jenkinsfile]
level: practitioner
status: docs-checked
description: "Call Dagger from a Jenkinsfile on a labelled agent, or from TeamCity through the JetBrains Dagger recipe in the Kotlin DSL, with the prerequisites and token handling."
sources: [https://docs.dagger.io/0.21/getting-started/ci-integrations/jenkins, https://docs.dagger.io/0.21/getting-started/ci-integrations/teamcity]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger on Jenkins and TeamCity (Dagger 0.21 docs)

Goal: keep your existing CI server and agents, but move pipeline logic into Dagger Functions.

## Jenkins

Prerequisites: a Jenkins agent labelled `dagger`, a Docker engine that can run containers (can be `docker:dind`), and the `docker` client on the agent. Token: a Jenkins credential named `DAGGER_CLOUD_TOKEN`.

```groovy
pipeline {
  agent { label 'dagger' }
  environment {
    DAGGER_VERSION = "<version>"
    PATH = "/tmp/dagger/bin:$PATH"
    DAGGER_CLOUD_TOKEN =  credentials('DAGGER_CLOUD_TOKEN')
  }
  stages {
    stage("dagger") {
      steps {
        sh '''
          curl -fsSL https://dl.dagger.io/dagger/install.sh | BIN_DIR=/tmp/dagger/bin DAGGER_VERSION=$DAGGER_VERSION sh
          dagger call -m github.com/shykes/hello hello --greeting "bonjour" --name "from jenkins"
        '''
      }
    }
  }
}
```

The docs template substitutes the Dagger version into `DAGGER_VERSION`; pin your own. The install script honours `BIN_DIR` and `DAGGER_VERSION`.

## TeamCity

Uses the "Dagger" recipe from the JetBrains Marketplace (`tc:recipe:jetbrains/dagger@1.0.0`). Needs a TeamCity server, an agent with Docker, and a repo holding the build configuration as code. The recipe installs the requested CLI version on the agent, then runs your command. Select Docker-capable agents with `requirements { exists("docker.server.version") }`.

```kotlin
step {
    id = "hello from dagger"
    type = "tc:recipe:jetbrains/dagger@1.0.0"
    param("env.input_version", "0.19.2")
    param("env.input_command", """dagger call -m github.com/shykes/hello hello --greeting "bonjour"""")
}
```

For test then publish, keep the recipe type, version and module in constants and run two steps: `dagger -m <module> call test --source=.` and `dagger -m <module> call build-container --source=. --args=. publish --address=ttl.sh/my-app-%env.BUILD_NUMBER%`, with a `GitVcsRoot` for the repo. Settings use Kotlin DSL `version = "2025.07"`.

## Gaps

The TeamCity page does not say how to pass `DAGGER_CLOUD_TOKEN` to the recipe; it only says telemetry is sent when the variable is set.

Related: computing-software.devops-ci-cd.dagger.circleci-azure-codebuild-dagger.

## Checked

2026-11-07

Read getting-started/ci-integrations/jenkins.mdx and teamcity.mdx in full (both slugs return 200) plus the three snippet files they embed (Jenkinsfile, teamcity-hello, teamcity-test-build). Confirmed the dagger agent label, Docker and docker:dind prerequisites, the DAGGER_CLOUD_TOKEN credential, the install-script BIN_DIR and DAGGER_VERSION usage, the {{ version }} template placeholder, the JetBrains recipe id tc:recipe:jetbrains/dagger@1.0.0, the env.input_version and env.input_command parameters, the docker.server.version requirement, the test and publish commands, the GitVcsRoot and the Kotlin DSL version 2025.07. The statement about the missing token-passing instructions is accurate for the TeamCity page. No corrections needed.

Method: documentation only; no commands were run.
