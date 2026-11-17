---
id: computing-software.devops-ci-cd.jenkins.docker-in-pipelines
name: docker-in-pipelines
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, docker-pipeline-plugin, docker-workflow, docker-image-inside, dockerfile-agent, docker-agent, docker-withregistry, docker-build, docker-push, agent-docker-args, reuse-node, docker-socket, docker-in-docker, dind-sidecar, with-run, kaniko-in-jenkins, buildkit, image-cleanup, docker-prune, user-mapping, uid-gid, workspace-mount, jenkinsfile-docker]
level: practitioner
status: docs-checked
description: "Use Docker from Jenkins pipelines: agent docker/dockerfile, docker.image().inside and withRun, withRegistry push, uid and workspace-mount gotchas, dind vs socket vs kaniko, cleanup."
sources: ["https://www.jenkins.io/doc/book/pipeline/docker/", "https://www.jenkins.io/doc/book/pipeline/syntax/", "https://github.com/jenkinsci/docker-workflow-plugin/blob/master/docs/docker-workflow.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker in pipelines

**Goal:** build steps run in a pinned toolchain image, images get built and pushed from
the Jenkinsfile, and the agent host doesn't fill up or get rooted in the process.

## 1. Run steps inside an image (Docker Pipeline plugin)
```groovy
pipeline {
  agent {
    docker {
      image 'maven:3.9-eclipse-temurin-21'
      args  '-v $HOME/.m2:/root/.m2'                          // cache deps on the agent
      label 'docker'                                          // agents that have Docker
      reuseNode true                                          // reuse the workspace/node of the outer agent
      registryUrl 'https://registry.example.com'              // for private images
      registryCredentialsId 'registry-creds'
    }
  }
  stages { stage('Build') { steps { sh 'mvn -B verify' } } }
}
```
Per-stage: `stage('Test') { agent { docker { image 'node:20' ; reuseNode true } } … }`.
`agent { dockerfile { additionalBuildArgs '--build-arg foo=bar' } }` builds the image from a
Dockerfile first (the Pipeline docker page also documents `registryUrl` and
`registryCredentialsId` for `dockerfile`).

How the plugin behaves (Pipeline docker page and plugin documentation):
- For a containerized stage without `reuseNode true`, Jenkins picks an agent and creates a new
  empty workspace; with `reuseNode true` no new workspace is created and the current workspace
  of the current agent is mounted into the container on the same node.
- The Docker server and the Jenkins agent must share a filesystem so the workspace can be
  mounted. With a remote Docker server (`docker.withServer`, Swarm), `inside()` and `build()`
  do not work out of the box; typical symptoms are negative exit codes or errors such as
  `cannot create /...@tmp/durable-.../pid: Directory nonexistent`.
- When the agent itself runs in a Docker container, the plugin passes `--volumes-from` to the
  `inside` container automatically.
- Package caches inside the container are lost every build unless redirected, for example the
  documented `args '-v $HOME/.m2:/root/.m2'` for Maven.

## 2. Scripted API
```groovy
node('docker') {
  checkout scm
  def img = docker.build("registry.example.com/team/app:${env.BUILD_NUMBER}")
  docker.image('postgres:16').withRun('-e POSTGRES_PASSWORD=x') { db ->
    sh './integration-tests.sh'          // steps here run on the agent, not inside the container
  }
  docker.withRegistry('https://registry.example.com', 'registry-creds') {
    img.push(); img.push('latest')
  }
}
```
- `withRun` starts a container for the block and stops it at the end; unlike `inside`, shell
  steps inside the block run on the agent.
- `docker.withRegistry(url, credentialsId)` selects a custom registry; the credential is a
  Username/Password credential.
- `docker.withServer('tcp://remote:2376', 'tls-creds')` targets a remote daemon (the credential
  is a *Docker Server Certificate Authentication* credential); see the limitation above.

## 3. Where does Docker come from?
- Docker on the agent host: simplest, but anyone who can run Docker on that host effectively
  controls it; use only for trusted jobs and agents.
- Kubernetes agents: use the Kubernetes plugin's pod containers (`container('name')`) rather
  than the Docker Pipeline plugin, which needs a daemon reachable from the agent.
- Daemonless image builders (Kaniko, BuildKit) avoid a privileged socket; consult their own
  documentation for flags and configuration.

## 4. Pushing and credentials
Use `docker.withRegistry(url, credentialsId)` for pushes. Never interpolate a password into an
`sh` string (`sh "docker login -p ${PASSWORD}"`); the Jenkinsfile docs show double-quoted
interpolation of credentials as wrong; use single quotes with environment variables.
For Amazon ECR see `docker-registry-credentials-and-amazon-ecr`.

## 5. Cleanup
Build images and layers accumulate on agents until the disk fills, and every job on that agent
then fails. Schedule pruning with Docker's own prune commands (see the Docker CLI reference for
`docker image prune` and `docker system prune` filters) and clean workspaces.

## Verify
- [ ] A step inside the container can read and write the workspace.
- [ ] Image push uses credentials from `withRegistry`; the log shows no password.
- [ ] Agent disk usage is stable across a week of builds.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed: `agent { docker { image, label, args, reuseNode, registryUrl, registryCredentialsId } }` and `dockerfile` agent options (Pipeline Syntax and docker pages); `reuseNode` workspace behaviour, `withRun`, `withRegistry`, `withServer` and its `inside()`/`build()` limitation, `--volumes-from` and the Maven cache example (Pipeline docker page and docker-workflow plugin docs). Removed the unconfirmed `docker run` internals, uid/entrypoint/ENV behaviours, dind/Kaniko flags, ECR syntax, buildx, `--link` and prune command specifics.
Method: documentation only; no commands were run.
