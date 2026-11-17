---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-feature-monitoring
name: tetragon-feature-monitoring
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [features-monitoring, tetragon, execution-monitoring, file-integrity, network-observability]
level: intro
status: docs-checked
description: "Understand what Tetragon offers for execution monitoring, file integrity monitoring and network observability, and why in-kernel eBPF helps."
sources:
  - "https://tetragon.io/docs/overview/"
  - "https://tetragon.io/"
  - "https://tetragon.io/docs/concepts/events/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon monitoring features

Goal: choose which Tetragon capability answers a detection question.

## How it works
Tetragon is an eBPF-based security observability and runtime enforcement tool. It applies policy and filtering in the kernel (filters on file, socket, binary names, namespace/capabilities and more), so only relevant events reach the user-space agent, which reduces overhead. It can hook any Linux kernel function and filter on arguments, return values and process metadata, and nothing about traced functions is hard-coded in the engine; tracing policies decide. Hooking deep in the kernel avoids syscall-tracing issues such as data being maliciously altered or missing due to page faults. In Kubernetes it understands namespaces and pods.

## Execution monitoring
- Process lifecycle: executed binaries, command-line arguments, UID, parent processes, start time.
- Kubernetes integration: link processes to pods, namespaces and labels.
- Policies can control binary execution (for example disallow execution from `/tmp`) and detect Linux namespace and privilege changes.

## File integrity monitoring
File Integrity Monitoring is one of the use cases Tetragon lists. It captures file access events in the kernel, can tie them to the process and Kubernetes workload, and can block malicious activity at the kernel level.

## Network observability
Tetragon captures network communications and correlates them with network data to identify the responsible binary. In Kubernetes it recognizes workload identities such as namespace and pod metadata.

## Checked

Date: 2026-11-07

The cited tetragon.io/features/ page returns only a banner (it renders with JavaScript), so it could not be read and was dropped from sources. Claims were re-checked against the Overview page, the tetragon.io home page and the events page, all read in full. Removed claims none of them confirm (ELF early detection, Inotify and hard link or bind mount detail, bytes sent and received, socket lifecycle).

Method: documentation only; no commands were run.
