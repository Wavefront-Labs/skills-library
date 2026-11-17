---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-grpc-api-process
name: tetragon-grpc-api-process
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [grpc-api-core]
level: sme
status: docs-checked
description: "Reference for core Tetragon gRPC messages: Process, ProcessExec, ProcessExit, ProcessKprobe, Pod, Container, Capabilities and KprobeAction."
sources:
  - "https://tetragon.io/docs/reference/grpc-api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC API core messages (tetragon/tetragon.proto)

Goal: know which fields an event carries.

## Process

- `exec_id`: uniquely identifies the process over time across all nodes in the cluster. `parent_exec_id` is the parent's.
- `pid` (host PID namespace), `tid`, `uid` (effective user id), `auid` (audit user id, inherited even after `su`), `cwd`, `binary` (absolute path), `arguments`, `start_time`, `docker` (first 15 digits of the container ID).
- `pod`: Pod info. `cap`: Capabilities. `ns`: Namespaces, off unless `--enable-process-ns`. `process_credentials`: off unless `--enable-process-cred`.
- `binary_properties` (ProcessExec only), `user` (needs `--username-metadata` set to "unix"), `in_init_tree` (true if in the process tree rooted at pid 1 of its PID namespace; useful to detect nsenter or kubectl exec), `environment_variables`, `refcnt`.
- `flags` are for debugging only: for example `execve` (from an execve syscall), `procFS` (loaded from /proc at Tetragon init), `clone`, `rootCWD`, `truncArgs`, `miss`.

## Events

- `ProcessExec`: `process`, `parent`, `ancestors`.
- `ProcessExit`: `process`, `parent`, `signal` (for example SIGKILL), `status`, `time`, `ancestors`.
- `ProcessKprobe`: `process`, `parent`, `function_name`, `args` and `return` (KprobeArgument), `action`, `return_action`, `policy_name`, `message`, `tags`, `kernel_stack_trace`, `user_stack_trace`, `ancestors`, `data`.
- Similar: `ProcessTracepoint` (`subsys`, `event`), `ProcessUprobe` (`path`, `symbol`, `offset`), `ProcessLsm` (`function_name`, `ima_hash`), `ProcessUsdt` (`provider`, `name`), `ProcessLoader` (`path`, `buildid`).

## Pod and Container

`Pod`: `namespace`, `name`, `uid`, `container`, `pod_labels`, `workload`, `workload_kind`, `pod_annotations`. `Container`: `id`, `name`, `image` (`id`, `name`), `start_time`, `pid`, `maybe_exec_probe`, `security_context` (`privileged`).

## KprobeAction values

`POST` (1, default, creates an event), `SIGKILL` (3), `OVERRIDE` (5, modifies the return value), `GETURL` (7), `DNSLOOKUP` (8), `NOPOST` (9, suppresses the event), `SIGNAL` (10), `TRACKSOCK` (11), `UNTRACKSOCK` (12), `NOTIFYENFORCER` (13), `CLEANUPENFORCERNOTIFICATION` (14), `SET` (15), `UPDATE_STATE` (16). FOLLOWFD, UNFOLLOWFD and COPYFD are deprecated and no longer supported.

Other messages: `KprobeArgument` (typed args such as `file_arg`, `sock_arg`, `path_arg`), `HealthStatus`, `CreateContainer` and `RuntimeHookRequest` for OCI hooks.

## Checked

Date: 2026-11-07

gRPC API reference (about 64 KB) read in full, including the sensors.proto section the skill does not cover. Added CLEANUPENFORCERNOTIFICATION (14) to the KprobeAction list.

Method: documentation only; no commands were run.
