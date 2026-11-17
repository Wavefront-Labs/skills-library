---
id: computing-software.cloud-infrastructure-engineering.terraform.attaching-a-debugger-to-a-provider-with-debug-mode
name: attaching-a-debugger-to-a-provider-with-debug-mode
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, provider-debug-mode, delve-debugging, reattach, tf-reattach-providers, provider-development, plugin-framework, debugging, breakpoints]
level: advanced
status: docs-checked
description: "Run a provider in -debug mode under Delve or an IDE, export TF_REATTACH_PROVIDERS, and step through CRUD code while terraform plan/apply drives it."
sources: ["https://developer.hashicorp.com/terraform/plugin/debugging", "https://developer.hashicorp.com/terraform/plugin/framework/debugging", "https://github.com/go-delve/delve"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attaching a debugger to a provider with `-debug` mode

**Goal:** set a breakpoint in a provider's `Create` or `Read`, run
`terraform apply`, and stop there. Debugging is most useful for a reliably
reproducible bug; for automated checks use acceptance tests, and for quick
reproduction with a local build consider `dev_overrides` in the CLI configuration.

## Prerequisites
- Terraform 0.12.26 or later.
- The configuration is compatible with the provider code being debugged.
- The configuration does not contain multiple provider aliases with different provider configurations.

## 1. Provider side: enable debug mode
Add a debug mode to the provider's `main` function, using the mechanism of your SDK:
`terraform-plugin-framework` (`ServeOpts` debug option), `terraform-plugin-sdk/v2`,
or `terraform-plugin-go` `tf5server.WithManagedDebug()` / `tf6server.WithManagedDebug()`.
Provider-mux and translation packages (`tf5muxserver`, `tf5to6server`, `tf6muxserver`,
`tf6to5server`) have their own sections in the plugin docs. Pass `-debug` to the binary.

Build with optimisation and inlining off so the debugger maps lines:
```bash
go build -gcflags="all=-N -l" -o terraform-provider-thing .
```

## 2. Start under Delve or an IDE
```bash
dlv exec --accept-multiclient --continue --headless ./terraform-provider-thing -- -debug
dlv connect 127.0.0.1:<PORT>      # port printed by dlv exec ("API server listening at")
```
The provider prints a `TF_REATTACH_PROVIDERS='{...}'` line. In VS Code with the Go
extension, a `launch.json` entry with `"mode": "debug"` and `"args": ["-debug"]`
prints the reattach configuration to the debug console.

## 3. Terraform side
Copy the `TF_REATTACH_PROVIDERS` line exactly, then export it or prefix each command:
```bash
TF_REATTACH_PROVIDERS='<pasted value>' terraform apply
```
Breakpoints halt execution and show current variable values.

## Behaviour differences in debug mode
- Terraform does not start the provider process; you run it manually.
- The same provider process is reused until the command completes, instead of being
  restarted once per walk of the graph.
Start a provider in debug mode only when you intend to debug it.

## Typical breakpoints
Resource `Create`/`Read`/`Update`/`Delete`, provider `Configure`, `ValidateConfig` and
`ModifyPlan`.

## Gotchas
- `TF_REATTACH_PROVIDERS` stays in your shell for every later command: `unset` it when done.
- Paste the reattach value rather than retyping it.

## Verify
- [ ] With the variable set, `terraform plan` stops at your breakpoint.
- [ ] Without it, Terraform launches the normal provider again.

## Checked
2026-10-31. Confirmed against the Terraform "Debugging providers" page: prerequisites
(0.12.26+, aliases), caveats, `-gcflags="all=-N -l"`, SDK options and mux packages, the
Delve and VS Code workflow, `dlv connect`, and how to pass `TF_REATTACH_PROVIDERS`. Removed:
the Go `main.go` listing and registry address, `ProtocolVersion` and the protocol 5/6
mapping, the explanation of the `Test` field, the Windows named-pipe note, the claim that
OpenTofu honours the variable, `-refresh=false` and gRPC timeout remarks, and
statements about the lock file and `init` behaviour under reattach, none of which the
fetched pages confirm.
Method: documentation only; no commands were run.
