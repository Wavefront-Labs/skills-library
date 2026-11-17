---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-ls-language-server-and-editor-integration
name: terraform-ls-language-server-and-editor-integration
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-ls, language-server, editor-integration, vscode, lsp, format-on-save, code-completion, tofu-ls]
level: intro
status: docs-checked
description: "Set up terraform-ls through the VS Code HashiCorp Terraform extension: completion, validation, format-on-save, schema refresh, root module settings."
sources: ["https://github.com/hashicorp/terraform-ls", "https://github.com/hashicorp/vscode-terraform", "https://github.com/opentofu/tofu-ls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# terraform-ls language server and editor integration

**Goal:** an editor that knows the provider schema, so attribute names are completed and
validated as you type.

## 1. What it is
- `terraform-ls` is HashiCorp's official Terraform language server and gives IDE features to any
  LSP-compatible editor. `tofu-ls` is the OpenTofu Core Team's language server, which used terraform-ls
  as its starting point. Some editors install and update the server automatically; each project's
  installation page covers manual install.
- The VS Code extension (HashiCorp Terraform, `hashicorp.terraform`) bundles the language server and is
  a self-contained install. It needs VS Code 1.86 or later and Terraform 0.12 or later.

## 2. VS Code features
- IntelliSense for providers, resources, data sources and attributes, plus modules installed in the
  workspace; syntax validation as you type; Go to Definition and Declaration (and Peek);
  `terraform fmt` based formatting; snippets; Module and Provider explorers; HCP Terraform workspaces
  and runs view; Command Palette commands Terraform: init, init current folder, validate and plan.
- Enhanced validation of `.tf` and `.tfvars` files is on by default; turn it off with
  `"terraform.validation.enableEnhancedValidation": false`.
- Terraform: validate runs `terraform validate`, which needs the Terraform CLI and a previous
  successful `terraform init`; it is the slowest but most thorough check. An experimental
  `"terraform.experimentalFeatures.validateOnSave": true` validates on save.

## 3. Settings worth setting
```json
{
  "[terraform]": { "editor.defaultFormatter": "hashicorp.terraform", "editor.formatOnSave": true, "editor.formatOnSaveMode": "file" },
  "[terraform-vars]": { "editor.defaultFormatter": "hashicorp.terraform", "editor.formatOnSave": true, "editor.formatOnSaveMode": "file" },
  "terraform.codelens.referenceCount": true,
  "terraform.experimentalFeatures.prefillRequiredFields": true
}
```
- Set `editor.defaultFormatter` so VS Code knows which extension formats Terraform files. The
  `terraform` binary must be on PATH or formatting silently fails.
- `prefillRequiredFields` is experimental; with `editor.suggest.preview` it gives inline snippet
  suggestions for whole blocks.

## 4. Why it needs `terraform init`
The extension picks up new provider schema automatically whenever something changes inside `.terraform`.
To refresh it, run Terraform: init current folder or `terraform init` in a terminal.

## 5. Workspaces and multiple root modules
- Open the containing folder (or a VS Code workspace with several folders) rather than a single file:
  opening a single Terraform file is not supported. A workspace uses one terraform-ls process with
  knowledge of the whole project.
- Several root modules: `terraform.languageServer.rootModules`, or let it search and exclude folders with
  `terraform.languageServer.excludeRootModules`; `terraform.languageServer.ignoreDirectoryNames`
  skips folders when indexing.
- Other settings: `terraform.languageServer.terraform.path`, `.timeout`, `.logFilePath`.

## Gotchas
- Syntax errors present when a document opens can prevent full completions. Run Terraform: validate, fix
  the errors and reload the document.
- Completion inside incomplete blocks such as `resource "` is not supported.
- Some folder layouts, notably a root module that is not a parent of its submodules, are not yet supported.
- If the Problems pane or hover stops updating, run Reload Window from the Command Palette.

## Verify
- [ ] Saving a file with bad formatting reformats it.
- [ ] After Terraform: init current folder, provider attributes complete inside a resource block.

## Checked
Read the terraform-ls, vscode-terraform and tofu-ls GitHub pages as downloaded text; the full vscode-terraform README sections for features, requirements, usage, configuration, known issues and troubleshooting were read. Removed as unconfirmed on those pages: Neovim and nvim-lspconfig setup, brew install, tflint langserver, the OpenTofu VS Code extension id, the modules.json requirement, dev_overrides behaviour, tf.json parsing, and the encryption-block claim. The incorrect setting name `terraform-ls.excludeRootModules` was corrected to `terraform.languageServer.excludeRootModules`.
Method: docs-checked 2026-11-09 against the three cited GitHub pages; no commands were run.
