---
id: computing-software.devops-ci-cd.tilt.tilt-controlloop
name: tilt-controlloop
category: computing-software
field: devops-ci-cd
product: tilt
tags: [controlloop, tilt]
level: practitioner
status: docs-checked
description: "Understand how Tilt turns a Tiltfile into resources and updates them: Tiltfile execution, resource grouping, and the events that trigger re-execution."
sources:
  - "https://docs.tilt.dev/controlloop.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tilt's control loop

Goal: build a mental model of the flow from Tiltfile to running services, useful for debugging and custom functionality.

## Resources

A resource is any bundle of work managed by Tilt. It can be:

- a container image to build plus Kubernetes YAML to deploy (a microservice you work on),
- just Kubernetes YAML (like a database instance),
- a command to run on localhost (like a script that generates an artifact you sync into a container).

Resources are what the Tilt sidebar shows.

## The Tiltfile

A Tiltfile is Starlark, a dialect of Python, so you can use conditionals, loops, and functions. It does not execute anything in your cluster: it stitches together information about resources and relays it to the Tilt engine.

- `k8s_yaml` registers YAML internally rather than applying it; at the end of Tiltfile execution Tilt packages it into a resource and sends it to the engine.
- `docker_build` tells Tilt how to build images.
- Heuristics group related work: a "myservice" image build plus YAML deploying an image called "myservice" become one resource.
- Tilt watches the Tiltfile and files feeding into it, and re-evaluates it if a change might affect its output.

## Applying resources

How depends on the resource: run local commands locally; build the image if build instructions are present; deploy Kubernetes YAML if present. When configured, Tilt can modify a running container in place.

When: Tilt reacts to key events:

- a change to the resource's definition in the Tiltfile,
- a user manually triggering the resource,
- a change to a file the resource cares about.

Files are declared explicitly in the Tiltfile, or implicitly: if the image build context is the "myservice" directory, any change in it affects that resource.

## Summary

1. Execute the Tiltfile, creating resource definitions (some manual, some assembled by heuristics).
2. Re-execute it whenever it changes and update definitions.
3. The engine executes resources; Kubernetes objects are deployed to the cluster.
4. Resources update on a triggering event.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/controlloop.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
