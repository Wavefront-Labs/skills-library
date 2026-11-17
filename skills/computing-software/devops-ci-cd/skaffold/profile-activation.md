---
id: computing-software.devops-ci-cd.skaffold.profile-activation
name: profile-activation
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [profiles, activation, kubecontext, env, command]
level: advanced
status: docs-checked
description: "Activate profiles automatically from an environment variable, kube-context or Skaffold command, and know the any/all rules."
sources:
  - "https://skaffold.dev/docs/environment/profiles/"
  - "https://skaffold.dev/docs/environment/kube-context/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Besides the `-p` flag, a profile can auto-activate from its `activation` list:

```yaml
profiles:
- name: dev
  activation:
  - env: MAGIC_VAR=1337
  - kubeContext: minikube
    command: dev
- name: not-local
  activation:
  - kubeContext: "!minikube"
```

Criteria:

- `env`: a `key=pattern` pair; the profile activates if the environment variable matches the pattern. A pattern starting with `!` activates when the remaining pattern is not matched.
- `kubeContext`: a string or regular expression; prefixing with `!` negates the match.
- `command`: the Skaffold command (the profiles page lists dev, run, build, deploy).

Rules:

- A profile auto-activates if any one of its activation entries is triggered, and an entry is triggered if all of its criteria (`env`, `kubeContext`, `command`) are triggered. The `dev` profile above therefore activates when `MAGIC_VAR=1337`, or when running `skaffold dev` with the context `minikube`.
- The schema also has `requiresAllActivations` (default false). When true, the profile auto-activates only when all of its activation entries are triggered.
- Disable auto-activation with `--profile-auto-activation=false` (default true, per the CLI reference). Deactivate a profile by prefixing its name with `-`, as in `skaffold dev -p hello,-world`; this applies even if the configuration would have activated it.

Kube-context rules (Kube-context Activation page): profile activation uses the original kube-context. If a profile is auto-activated by a matching `kubeContext`, the resulting kube-context must remain unchanged; activating such a profile together with one that sets `deploy.kubeContext` is illegal, though it is allowed when `--kube-context` is passed on the command line. The context of a running `skaffold dev` cannot be changed.

## Checked

2026-11-04. Read the whole Skaffold Profiles page, the Kube-context Activation page, the `Profile` and `Activation` schema definitions and the `--profile-auto-activation` flag in the CLI reference. Confirmed criteria, the any/all rules, deactivation and kube-context constraints. Added `requiresAllActivations`. Replaced the earlier `env: ENV=dev` example with the page's `MAGIC_VAR` form. Removed: the claim that `kubeContext` is always a regex (the page says string or regexp) and that `command` accepts "and so on" values.
Method: documentation only; no commands were run.
