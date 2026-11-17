---
id: computing-software.devops-ci-cd.dagger.module-dependencies-install-update
name: module-dependencies-install-update
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, module-dependencies, install, uninstall, update, git-refs, private-modules]
level: practitioner
status: docs-checked
description: "Install, call, update and uninstall Dagger module dependencies using git refs, including private and local modules, from dagger.json and the dag client."
sources: [https://docs.dagger.io/0.21/extending/module-dependencies]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module dependencies in Dagger

Goal: call functions from other Dagger modules inside your own. Dagger 0.21 docs.

## Reference format
`[proto://]host/repo[/subpath][@version]`
- `proto://` optional, `ssh://` or `https://`; if omitted Dagger picks based on available authentication.
- `subpath` optional, for monorepos.
- `@version` tag, branch or commit; default branch if omitted.
- Example: `github.com/shykes/daggerverse/hello@v0.3.0`.
- `.git` is optional for HTTP refs or explicit SSH refs, except on GitLab for modules in a private repo or private subgroup.

## Install
```shell
dagger install github.com/shykes/daggerverse/hello@v0.3.0
```
This adds to `dagger.json` a `dependencies` entry such as `{"name": "hello", "source": "github.com/shykes/daggerverse/hello@<commit sha>"}` (the page's example records the source with a commit sha in place of the tag) and adds the module to code generation. Access it through the pre-initialised `dag` client:
- Go: `dag.Hello().Hello(ctx)`
- Python: `await dag.hello().hello()`
- TypeScript: `await dag.hello().hello()`
- PHP: `dag()->hello()->hello()`
- Java: `dag().hello().hello()`

Chaining example: `dagger install github.com/kpenfound/dagger-modules/golang@v0.2.0`, then
```go
func (m *MyModule) Example(buildSrc *dagger.Directory, buildArgs []string) *dagger.Directory {
	return dag.Golang().Build(buildArgs, dagger.GolangBuildOpts{Source: buildSrc}).Terminal()
}
```
Call: `dagger call example --build-src=https://github.com/golang/example#master:/hello --build-args=.`

## Local modules
`dagger install ./path/to/module` works only if the module is inside the repository root (git) or inside the directory containing the `dagger.json` (otherwise).

## Private modules
Authentication works over HTTPS (git credential managers) or SSH (`SSH_AUTH_SOCK`). These install the same private module; the plain ref is preferred because any available auth method may be used:
```shell
dagger install github.com/username/private-repo/module
dagger install https://github.com/username/private-repo/module
dagger install ssh://git@github.com/username/private-repo/module
```
See remote-repositories-authentication.

## Uninstall and update
- `dagger uninstall hello` or `dagger uninstall github.com/shykes/daggerverse/hello` (name or remote ref).
- `dagger update hello` (or the full ref) updates to the latest version; the target module must be local.
- Given `github.com/path/name@branch/tag`: `dagger update github.com/path/name` moves to the latest commit of the branch/tag; `dagger update github.com/path/name@version` updates to the latest commit for that `version` branch/tag.

Related: third-party-packages (language-native deps are separate from Dagger modules), daggerverse-publish-examples.

## Checked

2026-11-07

Read extending/modules/module-dependencies.mdx in full (live slug /extending/module-dependencies matches the cited URL) and the Go chaining snippet. The Python, TypeScript, PHP and Java chaining snippet tabs were not opened; the per-language dag access lines come from the page's inline tabs, which I read. Confirmed the reference format and its parts, the .git exception for GitLab, the dagger install example and the dependencies entry, the dag client usage per SDK, the chaining example and dagger call command, the local module note, the private module ref styles, uninstall, and update (including the target-must-be-local note and the branch/tag note). Softened the claim that the version is resolved to a commit: the page only shows a commit sha in its example. The pointers to other skills are not from this page.

Method: documentation only; no commands were run.
