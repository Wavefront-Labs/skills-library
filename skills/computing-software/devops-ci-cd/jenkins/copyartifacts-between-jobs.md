---
id: computing-software.devops-ci-cd.jenkins.copyartifacts-between-jobs
name: copyartifacts-between-jobs
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, copyartifacts-selector, copyartifact, fingerprint]
level: practitioner
status: docs-checked
description: "Pass build outputs between Jenkins jobs with copyArtifacts: selectors (last successful, specific build, upstream), permissions, fingerprints and parameterised builds."
sources: ["https://github.com/jenkinsci/copyartifact-plugin/blob/master/README.adoc", "https://plugins.jenkins.io/copyartifact/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# copyArtifacts selectors between jobs

```groovy
copyArtifacts(
  projectName: 'app/build/main',          // full path incl. folders / multibranch branch
  selector: lastSuccessful(),
  filter: 'dist/**/*.tar.gz',
  target: 'incoming',
  fingerprintArtifacts: true,
  optional: false
)
```

## Selectors
| Selector | Use |
|---|---|
| `lastSuccessful()` | latest successful build (when `selector` is omitted the plugin uses the latest stable build) |
| `lastCompleted()` | completed build, ignoring build status |
| `latestSavedBuild()` | latest build marked "keep forever" |
| `specific("${params.BUILD_NUMBER}")` | promote a chosen build (pair with a build parameter) |
| `upstream()` | the upstream build that triggered this job |
| `permalink('<name>')` | a build named by a permalink |
| `buildParameter('BUILD_SELECTOR')` | selector chosen at run time via a "Build selector for Copy Artifact" parameter |

`parameters` takes comma-separated `name=value` pairs (for example `'ENV=prod,REGION=eu'`) to filter which build is copied; `excludes`, `flatten` and `includeBuildNumberInTargetPath` are also available.

## Permissions
The source job must allow copying: in the source Jenkinsfile
```groovy
options { copyArtifactPermission('app/deploy/*') }
```
(comma-separated job names; `*` wildcards allowed; scripted pipelines use
`properties([copyArtifactPermission('...')])`). Without it you may see "Unable to find project
for artifact copy ... This may be due to incorrect project name or permission settings". The
message is not shown if the "Authenticated" group has `Job/Read`; the Authorize Project plugin is
the alternative.

## Fingerprints
`fingerprintArtifacts: true` fingerprints the copied artifacts to track which builds used them. The
parameter defaults to false when omitted (the Snippet Generator sets it to true).

## When not to use
The plugin documentation recommends storing artifacts as archive files (`tar` or the `zip` step) so
file attributes survive. For large artifacts or other controllers, publish to an artifact
repository and reference by version; artifacts disappear when old builds are discarded.

## Verify
- [ ] The deploy build copies the intended files and, with fingerprinting on, the fingerprint page links both builds.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in the Copy Artifact README: `copyArtifacts` parameters (`projectName`, `selector`, `parameters`, `filter`, `excludes`, `target`, `flatten`, `optional`, `fingerprintArtifacts`), the selector list, default of latest stable build, `copyArtifactPermission` syntax and the "Unable to find project" message, archive recommendation. Removed the unconfirmed `upstream(fallbackToLastSuccessful)` argument and `lastStableBuild` permalink example.
Method: documentation only; no commands were run.
