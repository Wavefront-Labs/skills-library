---
id: computing-software.devops-ci-cd.nomad.alloc-exec
name: alloc-exec
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, alloc-exec, exec, debugging, interactive-shell, disable-remote-exec, alloc-node-exec, acl, cli]
level: practitioner
status: docs-checked
description: "Run commands inside a running Nomad allocation with nomad alloc exec including -task, -job, -group, -i, -t, escape character, quoting pitfalls and ACL capabilities."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/alloc/exec.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad alloc exec

Alias: `nomad exec`. Runs a command inside a running task, for debugging without SSH access to the node.

```
nomad alloc exec [options] <allocation> <command> [<args>...]
nomad alloc exec -i -t -task mytask a1827f93 /bin/bash
nomad alloc exec -job <job-id> <command>
```
If the allocation runs one task the task name can be omitted. `-job` selects a random allocation of that job (job ID prefix accepted), preferring a running one; add `-group` to pick the group.

## Options
- `-task=<name>`, `-job=<job-name|job-id>`, `-group=<name>`.
- `-i` pass stdin (default true; `-i=false` to disable).
- `-t` allocate a pseudo-tty (default true when stdin is a tty).
- `-e <char>` escape character for pty sessions (default `~`, recognised only at line start; `~.` closes the connection; `none` makes the session fully transparent).

## ACLs
`alloc-exec`, `read-job` and `list-jobs` in the allocation's namespace. If the driver has no filesystem isolation (`raw_exec`), `alloc-node-exec` is required instead of `alloc-exec`.

## Disabling
Enabled by default. Set the client option `disable_remote_exec` on all clients, or only those running sensitive workloads.

## Quoting pitfall
Your local shell expands variables before Nomad sees them:
```
nomad alloc exec eb17e557 echo $NOMAD_ALLOC_ID            # wrong: local value
nomad alloc exec eb17e557 /bin/sh -c 'echo $NOMAD_ALLOC_ID'  # right
nomad alloc exec eb17e557 /bin/sh <<'EOF'
echo $NOMAD_ALLOC_ID
EOF
```
The heredoc form also keeps pipelines running inside the task instead of streaming intermediate output over the network.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 alloc exec command page: options and defaults, ACL capabilities, disable_remote_exec, escape character, the quoting examples. Nothing removed.

Method: documentation only; no commands were run.
