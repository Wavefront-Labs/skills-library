---
id: computing-software.devops-ci-cd.argo-cd.config-management-plugins-sidecar
name: config-management-plugins-sidecar
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, config-management-plugin, cmp, cmp-sidecar, plugin-sidecar, plugin-yaml, configmanagementplugin, repo-server, discover, generate, init, parameters-announcements, plugin-env, argocd-env, var-run-argocd, cmp-server, argocd-vault-plugin, avp, cue, tanka, jsonnet-bundler, ytt, helmfile, kustomize-helm, custom-rendering, repo-server-sidecar, plugin-security, gitops, kubernetes]
level: advanced
status: docs-checked
description: "Render with tools Argo CD lacks (helmfile, ytt, cue, argocd-vault-plugin) via sidecar Config Management Plugins: plugin.yaml discover/init/generate, repo-server patch, parameters, security."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/config-management-plugins/", "https://argo-cd.readthedocs.io/en/stable/user-guide/config-management-plugins/", "https://argo-cd.readthedocs.io/en/stable/user-guide/build-environment/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/2.7-2.8/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Config Management Plugins (sidecar)

**Goal:** Argo CD renders with your tool of choice, isolated in its own container, without
patching the repo-server image or using the removed `argocd-cm` plugin config.

## 1. The model
Each plugin is a **sidecar container** in the `argocd-repo-server` pod whose entrypoint is
`/var/run/argocd/argocd-cmp-server` (a lightweight gRPC service), configured by a `plugin.yaml`
at `<ARGOCD_HOME>/cmp-server/config/plugin.yaml` in the sidecar (`<ARGOCD_HOME>` is the `argocd` user's home directory). The sidecar must run as user 999
and must not share the repo-server's `/tmp` volume (separate volume mitigates path traversal).

## 2. plugin.yaml
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ConfigManagementPlugin
metadata: { name: helmfile }          # unique per Argo CD instance; Application refers to "helmfile" (or helmfile-v1.0 if `spec.version` is set)
spec:
  version: v1.0
  init:                               # optional: runs in the source directory right before generate; output is not treated as manifests
    command: [sh, -c]
    args: ["helmfile deps"]
  generate:                           # stdout must be ONLY valid Kubernetes objects (YAML or JSON); log to stderr
    command: [sh, -c]
    args: ["helmfile -e ${ARGOCD_ENV_ENVIRONMENT:-default} template --quiet"]
  discover:                           # how Argo picks this plugin automatically (when Application omits plugin.name)
    fileName: "helmfile.yaml"         # glob; or find: { glob: "**/helmfile.yaml" } / find: { command: [...] } (only the first of these set is evaluated)
  parameters:
    static:
      - { name: environment, title: Environment, string: "default" }
    dynamic:
      command: [sh, -c, "echo '[{\"name\":\"release\",\"string\":\"\"}]'"]   # announce params per Application (JSON on stdout)
  preserveFileMode: false             # true passes original file modes; only for trusted plugins
```
`discover` lets apps without `spec.source.plugin.name` be matched; when `name` is set only that plugin is used (if its discovery matches), so prefer **explicit** `plugin.name`. Without `discover` the plugin can only be invoked by name.
Everything on stdout must be manifests, so send tool progress output to stderr (`>&2`).
Parameter announcements only inform the UI Parameters tab; they are not sent to the plugin.

## 3. Repo-server patch (Kustomize/Helm values)
```yaml
# kustomization patch on deployment/argocd-repo-server
spec:
  template:
    spec:
      containers:
        - name: helmfile
          image: <image containing your tool>          # off-the-shelf or custom image
          command: [/var/run/argocd/argocd-cmp-server]
          securityContext: { runAsNonRoot: true, runAsUser: 999 }
          volumeMounts:
            - { name: var-files, mountPath: /var/run/argocd }
            - { name: plugins, mountPath: <ARGOCD_HOME>/cmp-server/plugins }
            - { name: helmfile-plugin-config, mountPath: <ARGOCD_HOME>/cmp-server/config/plugin.yaml, subPath: plugin.yaml }
            - { name: cmp-tmp, mountPath: /tmp }
      volumes:
        - { name: helmfile-plugin-config, configMap: { name: helmfile-cmp } }
        - { name: cmp-tmp, emptyDir: {} }
```
The sidecar `image` can be off-the-shelf or custom-built; the plugin config can instead be baked into the image at `<ARGOCD_HOME>/cmp-server/config/plugin.yaml`.
If `plugin.yaml` comes from a ConfigMap, restart the repo-server pod to pick up changes.

## 4. Using it from an Application
```yaml
spec:
  source:
    repoURL: https://git.example.com/k8s/apps.git
    path: services/web
    plugin:
      name: helmfile                    # or helmfile-v1.0 when versioned
      env:
        - { name: ENVIRONMENT, value: production }   # exposed as ARGOCD_ENV_ENVIRONMENT (prefix added for safety)
      parameters:
        - { name: environment, string: production }  # JSON in ARGOCD_APP_PARAMETERS and env var PARAM_ENVIRONMENT
```
Build environment variables available to the plugin include `ARGOCD_APP_NAME`, `ARGOCD_APP_NAMESPACE`, `ARGOCD_APP_PROJECT_NAME`,
`ARGOCD_APP_REVISION`, `ARGOCD_APP_SOURCE_PATH`, `ARGOCD_APP_SOURCE_REPO_URL`,
`ARGOCD_APP_SOURCE_TARGET_REVISION`, `KUBE_VERSION`, `KUBE_API_VERSIONS`. User `env` is
prefixed `ARGOCD_ENV_` so users cannot set sensitive variables directly. Array parameters become `PARAM_<NAME>_0`, `PARAM_<NAME>_1`; map keys become `PARAM_<NAME>_<KEY>`. Only parameters set in the Application spec are sent, not announced defaults.

## 5. Common plugins
- **Secret-injection plugins (for example argocd-vault-plugin)**: follow that project's own documentation for its sidecar image and configuration; a plugin sidecar that holds credentials has access to everything it can render, so scope its credentials narrowly.
- **Kustomize + Helm**: not a plugin; see the Kustomize page for `--enable-helm` build options.
- **ytt/cue/tanka/helmfile/cdk8s**: all follow the same plugin.yaml template.

## 6. Operations and gotchas
- Check the sidecar's logs with `kubectl logs deploy/argocd-repo-server -c helmfile` (container name as you named it).
- Timeouts: a CMP command that runs too long is killed. The CMP server respects `server.repo.server.timeout.seconds` and `controller.repo.server.timeout.seconds` (default 60 s) in `argocd-cmd-params-cm`, and each command also times out on `ARGOCD_EXEC_TIMEOUT` set on the sidecar (default 90 s); a command that does not exit gracefully is killed after a further `ARGOCD_EXEC_FATAL_TIMEOUT`.
- A CMP that renders blank manifests with `prune: true` makes Argo CD remove resources: make failures part of the exit code (`set -o pipefail` for piped commands).
- Each Application can use only one plugin.
- Plugins configured in `argocd-cm` stopped working in v2.8; migrate to sidecars.

## Verify
- [ ] `argocd app manifests <app>` returns rendered YAML via the plugin; sidecar logs show the generate call.
- [ ] A `plugin.env` change triggers a re-render; `ARGOCD_ENV_*` visible to the command.
- [ ] Tool version is pinned by image tag and upgradable via a repo-server rollout only.
- [ ] Plugin sidecar runs non-root and cannot write outside `/tmp`.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: sidecar entrypoint and mounts, `<ARGOCD_HOME>/cmp-server/config/plugin.yaml` location, user 999, separate `/tmp` volume, plugin.yaml field semantics (`version`, `init`, `generate`, `discover` precedence, `parameters`, `preserveFileMode`), naming rule `<name>-<version>`, `ARGOCD_ENV_` prefix, `ARGOCD_APP_PARAMETERS` and `PARAM_*` naming, build environment variables, timeouts (60 s, `ARGOCD_EXEC_TIMEOUT` 90 s), blank-manifest and prune warning, argocd-cm plugins unsupported from v2.8. Removed unconfirmed claims (working directory path, sidecar match order, pinned image, Helm chart values, error text, size and caching remarks) and the third-party argocd-vault-plugin details.

Method: documentation only; no commands were run.
