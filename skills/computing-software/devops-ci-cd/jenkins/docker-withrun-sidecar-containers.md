---
id: computing-software.devops-ci-cd.jenkins.docker-withrun-sidecar-containers
name: docker-withrun-sidecar-containers
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, withrun, docker-pipeline-plugin, docker-image-inside]
level: practitioner
status: docs-checked
description: "Run databases and other sidecar containers for tests in Jenkins with docker.image().withRun, linking them to an inside() build container and waiting for readiness."
sources: ["https://www.jenkins.io/doc/book/pipeline/docker/", "https://github.com/jenkinsci/docker-workflow-plugin/blob/master/docs/docker-workflow.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# withRun sidecar containers for tests

```groovy
node('docker') {
  checkout scm
  docker.image('postgres:16').withRun('-e POSTGRES_PASSWORD=pw -e POSTGRES_DB=app') { db ->
    // wait for readiness using a throwaway container on the same link
    docker.image('postgres:16').inside("--link ${db.id}:db") {
      sh 'until pg_isready -h db -U postgres; do sleep 1; done'
    }
    docker.image('python:3.12').inside("--link ${db.id}:db") {
      sh 'pip install -r requirements.txt && DATABASE_URL=postgresql://postgres:pw@db/app pytest'
    }
  }   // the container is stopped when the block ends
}
```

## Notes
- `withRun` starts the container for the block, passes a handle (`db.id`) and stops the container
  at the end. Unlike `inside`, shell steps in the block run on the agent, not in the container.
- The Pipeline docker page links the sidecar with `inside("--link ${c.id}:db")`; `--link` is a legacy
  Docker feature, so check your Docker version's documentation for network-based alternatives.
- `docker logs ${c.id}` can be run inside the block to dump logs.
- On Kubernetes agents use extra containers in the pod template instead (see the Kubernetes plugin).

## Gotchas
- Publishing fixed ports (`-p 3306:3306`, as the docs example does) can collide on shared agents; prefer not to publish.

## Verify
- [ ] `docker ps -a` on the agent shows no leftover postgres container after the build.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in the Pipeline docker page and docker-workflow docs: `docker.image(...).withRun(args) { c -> ... }` (stops the container at block end, steps run on the agent), `c.id`, `inside("--link ${c.id}:db")` and `docker logs ${c.id}`. Removed unconfirmed `db.port`, user-network recipe, declarative and UID notes.
Method: documentation only; no commands were run.
