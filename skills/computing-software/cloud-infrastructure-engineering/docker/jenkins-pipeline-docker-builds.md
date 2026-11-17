---
id: computing-software.cloud-infrastructure-engineering.docker.jenkins-pipeline-docker-builds
name: jenkins-pipeline-docker-builds
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, jenkins-docker, jenkins-pipeline, docker-pipeline-plugin, jenkinsfile, docker-agent, withregistry, ci-builds]
level: practitioner
status: docs-checked
description: "Build, test and push images from a Jenkinsfile with the Docker Pipeline plugin: docker.build, inside, withRegistry, docker and dockerfile agents, reuseNode."
sources: ["https://www.jenkins.io/doc/book/pipeline/docker/", "https://plugins.jenkins.io/docker-workflow/", "https://www.jenkins.io/doc/book/pipeline/syntax/#agent", "https://plugins.jenkins.io/credentials-binding/", "https://docs.docker.com/build/ci/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jenkins pipeline Docker builds

The Docker Pipeline plugin is required: without it Jenkins cannot use the `docker` agent type in Declarative Pipeline or `docker.image(...).inside {}` in Scripted Pipeline.

## Build, test, push (Scripted Pipeline)
```groovy
node {
  checkout scm
  def customImage = docker.build("my-image:${env.BUILD_ID}")
  customImage.inside { sh 'make test' }
  docker.withRegistry('https://registry.example.com', 'registry-credentials-id') {
    customImage.push()
  }
}
```
- `docker.build("name")` builds the Dockerfile in the current directory; pass a directory path as the second argument to build elsewhere.
- `push()` publishes to Docker Hub or a custom registry via `docker.withRegistry(url, credentialsId)`.
- `customImage.inside { ... }` runs steps in a container started from the image.

## Docker agents (run stages inside a container)
```groovy
agent {
  docker {
    image '<IMAGE>'
    args  '-v $HOME/.m2:/root/.m2'
    reuseNode true
  }
}
// or build the agent image from the repo:  agent { dockerfile true }
```
- `reuseNode true` keeps the current workspace mounted in the container on the same node; without it a dockerized stage may run in a temporary workspace, possibly on another agent.
- `agent { dockerfile true }` builds a new image from the Dockerfile in the repository root instead of pulling one; further options are on the Pipeline Syntax page.
- `reuseNode` is not supported in Scripted Pipeline.

## Credentials
Use the Credentials Binding plugin (`withCredentials`) for secrets in `sh` steps. Reference them from the shell (single-quoted `sh '...'`) rather than interpolating in Groovy, so the secret is not expanded into the build log.

## Checked
2026-10-28. Confirmed against the Jenkins "Using Docker with Pipeline" page and the Pipeline Syntax agent section: plugin requirement, `docker.build`, `inside`, `push`, `withRegistry`, `reuseNode`, `agent { dockerfile true }`, `args`. Removed unconfirmed claims: buildx/cache flags, executor and uid/HOME behaviour, Kubernetes agent advice, prune and storage figures, and the Groovy-interpolation warning wording (kept only as general advice).
Method: documentation only; no commands were run.
