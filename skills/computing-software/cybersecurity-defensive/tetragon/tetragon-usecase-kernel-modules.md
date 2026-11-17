---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-usecase-kernel-modules
name: tetragon-usecase-kernel-modules
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [usecase-kmods, tetragon, kernel-modules, module-signing]
level: practitioner
status: docs-checked
description: "Detect which process loads, auto-loads or unloads Linux kernel modules, and whether they are signed, with the Tetragon module policy."
sources:
  - "https://tetragon.io/docs/use-cases/host-system-changes/linux-kernel-modules/"
  - "https://raw.githubusercontent.com/cilium/tetragon/main/examples/tracingpolicy/host-changes/monitor-kernel-modules.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor Linux kernel modules with Tetragon

Goal: answer which process or container loads or unloads kernel modules, which request triggered an automatic load, and whether modules are signed.

```shell
kubectl apply -f https://raw.githubusercontent.com/cilium/tetragon/main/examples/tracingpolicy/host-changes/monitor-kernel-modules.yaml
kubectl exec -it -n kube-system ds/tetragon -c tetragon -- tetra getevents
```

## Kprobes in monitor-kernel-modules

All with `syscall: false`:

- `security_kernel_module_request` (arg 0 `string`, `return: true`): automatic module loading.
- `security_kernel_read_file` (args `file`, `int`, `return: true`): explicit load by file descriptor, with a `matchArgs` on index 1 `Equal` `"2"` (READING_MODULE) to print the module path.
- `do_init_module` (arg `module`): final load for both `init_module()` and `finit_module()`.
- `free_module` (arg `module`): unload.

Limitations noted in the policy: for `init_module()` the full path is unavailable; rootkits that unlink a module from kernel module state without unloading it evade `free_module`, so watch the load hooks.

## Events

Loading with `insmod` yields `security_kernel_read_file` (`file_arg.path`) then `do_init_module` with `module_arg` holding `name` and `tainted`, e.g. `TAINT_OUT_OF_TREE_MODULE`, `TAINT_UNSIGNED_MODULE`.

Automatic loads (e.g. mounting xfs) yield `security_kernel_module_request` with `string_arg` `fs-xfs` (the kernel prefixes the requesting subsystem), then a `process_exec` of `/sbin/modprobe` started from the host namespaces, then `security_kernel_read_file` on the host module path.

## Signatures

Needs a kernel built with `CONFIG_MODULE_SIG`. Apply `monitor-signed-kernel-modules.yaml` (same directory); its `find_module_sections` event has `module_arg.signature_ok`. If `true`, verification succeeded; `false` or missing means not verified or failed.

Unloading with `rmmod` produces a `free_module` event.

Remove: `kubectl delete -f` the same URL.

## Checked

2026-11-08. Read the kernel modules page in full and the monitor-kernel-modules.yaml example policy; added the example policy as a source for the per-hook policy details. The monitor-signed-kernel-modules.yaml file was not read; the skill only names it as the page does.

Method: documentation only; no commands were run.
