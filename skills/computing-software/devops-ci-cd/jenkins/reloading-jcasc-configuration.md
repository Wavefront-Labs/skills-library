---
id: computing-software.devops-ci-cd.jenkins.reloading-jcasc-configuration
name: reloading-jcasc-configuration
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, jcasc, configuration-as-code, jcasc-reload, casc-reload-token, reload-configuration-as-code, config-reload-sidecar, jenkins-helm-chart, hot-reload, gitops-jenkins]
level: advanced
status: docs-checked
description: "Apply JCasC changes without restarting Jenkins: UI reload, the reload endpoint with casc.reload.token, Helm config-reload sidecar, CLI, and what reload can't change."
sources: ["https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/README.md", "https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/docs/features/configurationReload.md", "https://github.com/jenkinsci/helm-charts/blob/main/charts/jenkins/VALUES.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reloading JCasC configuration

## Ways to trigger
1. UI: *Manage Jenkins -> Configuration -> Reload existing configuration* (path as written in the plugin docs).
2. CLI: `java -jar jenkins-cli.jar -s $JENKINS reload-jcasc-configuration` plus your authentication options
   (the command exists only while the plugin is installed; an `apply-configuration` command also exists).
3. Authenticated HTTP: `curl -X POST -u "$U:$TOKEN" "$JENKINS/configuration-as-code/reload"`.
4. **Token endpoint** for automation without a user: start Jenkins with system property
   `-Dcasc.reload.token=<random>` (or env `CASC_RELOAD_TOKEN`, which wins if both are set), then
   ```bash
   curl -X POST "$JENKINS/reload-configuration-as-code/?casc-reload-token=$CASC_RELOAD_TOKEN"
   ```
   The token is a bearer secret; keep it in a K8s Secret, only reachable in-cluster.
5. **Helm chart sidecar** (`controller.sidecars.configAutoReload.enabled`, `true` by default in the chart values)
   enables Jenkins Config as Code auto-reload for the controller, so `helm upgrade` with new
   `controller.JCasC.configScripts` can be applied without restarting the pod.

## What to know
- Reload re-reads the sources in `CASC_JENKINS_CONFIG`.
- Only one reload or apply runs at a time: HTTP endpoints answer 409 Conflict and the CLI commands exit with code 4, so automation (such as the sidecar) should retry later.
- The `/configuration-as-code/configure` endpoint accepts YAML in the POST body (admin user and API token).
- Reloading from a Groovy script in a pipeline can leave the plugin unable to reload until Jenkins restarts (plugin docs, issue 1227).

## Safety
- Validate before reloading (see `computing-software.devops-ci-cd.jenkins.jcasc-export-and-schema-validation`) and try changes on a staging controller first.

## Verify
Change `systemMessage`, trigger reload, and confirm the banner updates.

## Checked

2026-10-28. Confirmed in the JCasC configurationReload page and the Helm chart values: UI path, reload-configuration-as-code endpoint with casc-reload-token, CASC_RELOAD_TOKEN and casc.reload.token (env wins, disabled by default), /configuration-as-code/reload with crumb and admin credentials, reload-jcasc-configuration CLI command, apply-configuration, /configuration-as-code/configure, 409 and exit code 4 on concurrent reloads, controller.sidecars.configAutoReload.enabled default true, controller.JCasC.configScripts. Removed: ConfigMap label name, one-minute timing, the reset/replace semantics, Job DSL removedJobAction, secret re-resolution, and log line claims.
Method: documentation only; no commands were run.
