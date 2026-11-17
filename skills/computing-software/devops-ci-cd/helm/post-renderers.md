---
id: computing-software.devops-ci-cd.helm.post-renderers
name: post-renderers
category: computing-software
field: devops-ci-cd
product: helm
tags: [post-renderer, kustomize, postrender, manifest-rewrite, plugin, post-renderer-args]
level: advanced
status: docs-checked
description: "Pipe rendered manifests through an external post-renderer; Helm 4 plugin form, filename annotation and hook strategies."
sources:
  - https://helm.sh/docs/topics/advanced/
  - https://helm.sh/docs/helm/helm_install/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A post-renderer lets an installer manipulate, configure or validate rendered manifests before Helm installs them, for example applying Kustomize changes without forking a public chart, injecting sidecars, or analysing manifests. It needs Helm 3.1 or later.

Contract: the post-renderer is any executable that accepts the rendered manifests on stdin and returns valid Kubernetes manifests on stdout, with a non-zero exit code on failure. That is the only API between the two.

```bash
helm install mychart stable/wordpress --post-renderer ./path/to/executable
```

- It works with `install`, `upgrade` and `template`.
- A path without separators is searched in `$PATH`; a relative path is resolved to a fully qualified one.
- In the Helm 3 reference `--post-renderer` takes the path of an executable. In the Helm 4 reference the value is the name of a post-renderer type plugin; `--post-renderer-args` passes an argument (repeatable) in both.
- Several renderers: chain them in one script, for example `renderer1 | renderer2 | renderer3`.

Filenames: each manifest sent to the post-renderer carries a temporary annotation `postrenderer.helm.sh/postrender-filename: <original-template-filename>`. Helm uses it to map the output back to filenames, generates `generated-by-postrender-<id>.yaml` if it is missing, and removes it before sending to Kubernetes.

Hooks in Helm 4: chart hooks are processed by post-renderers along with templates. The `combined` strategy (default) sends hooks and templates as one stream; `separate` invokes the renderer once for hooks and once for templates (useful when the same resource appears in both); `nohooks` sends only templates and matches Helm 3 behaviour. The page presents the choice as a Go SDK option (`PostRenderStrategy`), not as a command-line flag. For Kustomize patches that target template-only resources, use `nohooks`, because `separate` runs the patches against the hook stream too and they fail.

Caveats from the docs:

- Everyone modifying a release must use the same renderer for repeatable builds; switching or dropping it should be deliberate to avoid accidental modification or data loss.
- A renderer sees the full rendered templates, which often contain secrets, so use only trusted renderers.
- Go SDK users can implement the `PostRenderer` interface, `Run(*bytes.Buffer) (*bytes.Buffer, error)`.

Preview the final YAML with `helm template --post-renderer ...`.

## Checked

2026-11-08. Checked against the Helm 4 post-renderer documentation and install page: --post-renderer takes a plugin name and --post-renderer-args exists. Removed the invented --post-renderer-strategy CLI flag (the strategy is a Go SDK option) and other unsourced claims.

Method: documentation only; no commands were run.
