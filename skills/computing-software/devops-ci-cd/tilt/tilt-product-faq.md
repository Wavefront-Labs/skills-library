---
id: computing-software.devops-ci-cd.tilt.tilt-product-faq
name: tilt-product-faq
category: computing-software
field: devops-ci-cd
product: tilt
tags: [product-faq, tilt]
level: intro
status: docs-checked
description: "Who Tilt is for, why it focuses on Kubernetes, who develops it, and how to get support or file issues."
sources:
  - "https://docs.tilt.dev/product_faq.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tilt product FAQ

Goal: decide whether Tilt fits your team and know where to get help.

## What it is

Tilt is a free, open-source microservice development environment for teams that deploy to Kubernetes. A microservice development environment understands how your files and your servers fit together, and helps you understand your system. Once set up, any contributor should be able to run `tilt up` to get a complete dev environment.

## Who should use it

Teams developing microservice apps, where the pain is most acute. Signs it fits:

- You keep 5 terminal windows open to stream the logs of all your servers.
- Devs keep asking in team chat how to tell meaningful error logs from noise.
- You have a complicated Bash script that sets up all your dev servers but is always breaking.

## Why Kubernetes

Kubernetes defines well-thought-out building blocks (containers, pods, services) that are becoming industry standards, and the docs argue they should be used for all development environments. Tilt also supports docker-compose and building with local shell commands (`local_resource`), mostly to make it easier for teams to migrate.

## Governance and support

- As of May 2022, Tilt was acquired by Docker. The current plan is to keep maintaining Tilt as an open-source project.
- Real-time support: the Kubernetes slack (slack.k8s.io), #tilt channel. A Tilt developer is active during NYC business hours (10am-5pm Monday through Friday).
- File an issue in the tilt-dev/tilt GitHub repo. A developer should acknowledge it on normal work days; if you hear nothing after a day or two, it is OK to ping the thread or ask in Slack.
- Filing a GitHub issue helps get features onto the roadmap.
- The name is a Don Quixote reference (tilting at windmills); the demo app is called Servantes.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Who is Tilt for? page in full. Confirmed the product description, the fit signs, the Kubernetes rationale, the May 2022 Docker acquisition and open-source statement, the Slack support hours, the issue acknowledgement policy, the roadmap note and the name origin. Nothing removed. The skill is thin and mostly non-technical. 

Method: documentation only; no commands were run.
