---
id: computing-software.devops-ci-cd.tilt.tilt-example-java
name: tilt-example-java
category: computing-software
field: devops-ci-cd
product: tilt
tags: [example-java, tilt, spring-boot, live-update]
level: practitioner
status: docs-checked
description: "Speed up the Tilt feedback loop for a Spring Boot Java server: local Gradle build, unpacked jar layers, Jib, and live_update with restart_process."
sources:
  - "https://docs.tilt.dev/example_java.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java with Tilt

Goal: shorten code-change-to-new-process time for a Spring Boot server (example repo: tilt-example-java).

## Step 0 and 1: baseline

```python
docker_build('example-java-image', '.')
k8s_yaml('kubernetes.yaml')
k8s_resource('example-java', port_forwards=8000)
```

Names must match the Deployment's container `image` and `metadata.name`. A `deploy` local_resource running `./record-start-time.sh` (and `resource_deps=['deploy']` on the server) measures it. Naive: 87.7s, since each change copies source, downloads Gradle and Spring dependencies, and compiles from scratch.

## Step 2: compile locally (13.4s)

```python
local_resource(
  'example-java-compile',
  './gradlew bootJar',
  deps=['src', 'build.gradle'],
  resource_deps = ['deploy'])
docker_build(
  'example-java-image',
  './build/libs',
  dockerfile='./Dockerfile')
```

## Step 3: unpack the fat jar (6.5s)

Unzip so jar contents become Docker layers:

```python
local_resource(
  'example-java-compile',
  './gradlew bootJar && ' +
  'unzip -o build/libs/example-0.0.1-SNAPSHOT.jar -d build/jar',
  deps=['src', 'build.gradle'],
  resource_deps = ['deploy'])
```

```
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
ADD BOOT-INF/lib /app/lib
ADD META-INF /app/META-INF
ADD BOOT-INF/classes /app
ENTRYPOINT java -cp .:./lib/* dev.tilt.example.ExampleApplication
```

Files are added from least to most frequently used to improve caching. Jib (a Java image builder with Maven and Gradle plugins; the example repo's Tiltfile uses `custom_build` with it) is an alternative.

## Step 4: live update (4.8s)

```python
load('ext://restart_process', 'docker_build_with_restart')
local_resource(
  'example-java-compile',
  gradlew + ' bootJar && ' +
  'unzip -o build/libs/example-0.0.1-SNAPSHOT.jar -d build/jar-staging && ' +
  'rsync --inplace --checksum -r build/jar-staging/ build/jar',
  deps=['src', 'build.gradle'],
  resource_deps = ['deploy'])
docker_build_with_restart(
  'example-java-image',
  './build/jar',
  entrypoint=['java', '-noverify', '-cp', '.:./lib/*', 'dev.tilt.example.ExampleApplication'],
  dockerfile='./Dockerfile',
  live_update=[
    sync('./build/jar/BOOT-INF/lib', '/app/lib'),
    sync('./build/jar/META-INF', '/app/META-INF'),
    sync('./build/jar/BOOT-INF/classes', '/app'),
  ],
)
```

`live_update` copies only touched files, so `rsync --checksum` from a staging directory avoids touching unchanged files. `docker_build_with_restart` re-executes `entrypoint` after syncing.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/example_java.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Removed the `./gradlew jibDockerBuild --image $EXPECTED_REF` command, which the page does not give; corrected "frequently changed" to "frequently used".

Method: documentation only; no commands were run.
