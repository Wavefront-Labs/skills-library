---
id: computing-software.devops-ci-cd.jenkins.snippet-and-directive-generators
name: snippet-and-directive-generators
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, directive-generator, snippet-generator, pipeline-syntax, global-variables-reference, steps-reference, jenkinsfile-authoring, plugin-steps]
level: intro
status: docs-checked
description: "Write correct Jenkinsfile syntax fast with the controller's Snippet Generator, Declarative Directive Generator and Global Variable Reference, matched to your installed plugins."
sources: ["https://www.jenkins.io/doc/book/pipeline/getting-started/", "https://www.jenkins.io/doc/pipeline/steps/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snippet and Directive generators

Every controller serves syntax helpers populated from *its* installed plugins, at
`$JENKINS_URL/pipeline-syntax` (also linked as *Pipeline Syntax* in the sidebar of any
configured Pipeline job). Use them rather than copying snippets from the internet, which
often target other plugin versions.

## Snippet Generator (steps)
1. Pick a step in the *Sample Step* dropdown (`withCredentials`, `checkout`, `junit`, `archiveArtifacts`, `slackSend`...). The list depends on which installed plugins expose steps.
2. Fill the form below the dropdown; the help icon shows the step's documentation.
3. Click *Generate Pipeline Script* and paste the result into your Pipeline.

Most valuable for complex `checkout`, `withCredentials` bindings, and plugin steps whose
parameter names are hard to guess.

## Declarative Directive Generator
Reached from the *Declarative Directive Generator* link in the Pipeline Syntax sidebar, or
directly at `$JENKINS_URL/directive-generator`. It covers the sections and directives that
define a Declarative Pipeline (which the Snippet Generator does not); choose a directive,
fill the form, click *Generate Directive*.
- It can generate nested directives (for example conditions inside `when`) but not steps.
  For directives that contain steps (a `stage`'s `steps`, or `always`/`failure` in `post`) it
  emits a placeholder comment; add the steps by hand.

## Reference pages
- *Global Variable Reference* (`$JENKINS_URL/pipeline-syntax/globals`): documents `env`
  (`env.PATH`, `env.BUILD_ID`), `params` (read-only Map) and `currentBuild`
  (`currentBuild.result`, `currentBuild.displayName`), plus variables added by plugins.
- Public Pipeline Steps Reference across plugins in the Update Center:
  https://www.jenkins.io/doc/pipeline/steps/ (may list steps you do not have installed).

## Gotchas
- Generate on the controller that will run the Pipeline: available steps and parameters depend on its plugins and their versions.

## Verify
Paste the generated snippet into a scratch pipeline job and run; run the declarative
linter (`computing-software.devops-ci-cd.jenkins.linting-jenkinsfiles`) on the full
Jenkinsfile.

## Checked
2026-10-31. Confirmed against the Jenkins "Getting started with Pipeline" page (Snippet Generator, Global Variable Reference, Declarative Directive Generator sections): `/pipeline-syntax`, `/directive-generator`, `/pipeline-syntax/globals`, the generation steps, `env`/`params`/`currentBuild` and the placeholder-comment limitation; and the public Pipeline Steps Reference. Removed unconfirmed claims: job-specific `pipeline-syntax` path, `pipeline-syntax/html` and `gdsl` pages, `vars/*.txt` help, "emits only non-default arguments", `scmGit` versus `$class` and `@Symbol` notes.
Method: documentation only; no commands were run.
