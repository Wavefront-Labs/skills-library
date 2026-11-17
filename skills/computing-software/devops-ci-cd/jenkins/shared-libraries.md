---
id: computing-software.devops-ci-cd.jenkins.shared-libraries
name: shared-libraries
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, shared-libraries, pipeline-libraries, library-annotation, vars, global-variables, custom-steps, def-call, src-classes, resources, libraryresource, global-trusted-library, folder-library, groovy-sandbox, script-security, noncps, cps, serializable, steps-reference, jenkinspipelineunit, unit-testing, library-versioning, implicit-load, dynamic-library, groovy]
level: advanced
status: docs-checked
description: "Build Jenkins shared libraries that scale: vars vs src layout, typed config steps, CPS/@NonCPS rules, trusted vs folder libraries, versioning and JenkinsPipelineUnit tests."
sources: ["https://www.jenkins.io/doc/book/pipeline/shared-libraries/", "https://www.jenkins.io/doc/book/pipeline/cps-method-mismatches/", "https://github.com/jenkinsci/JenkinsPipelineUnit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared libraries

**Goal:** Jenkinsfiles in app repos shrink to ~10 lines calling org-wide steps, and the
library itself is versioned, tested and can't be used to escalate privileges.

## 1. Layout
```
(repo root)
├── vars/
│   ├── buildService.groovy     # step: buildService(...)
│   └── buildService.txt        # help text shown in Pipeline Syntax
├── src/org/acme/ci/
│   ├── Docker.groovy           # classes; package org.acme.ci
│   └── Semver.groovy
├── resources/org/acme/ci/
│   └── pod-template.yaml       # libraryResource 'org/acme/ci/pod-template.yaml'
└── test/groovy/...             # JenkinsPipelineUnit tests
```
- `vars/*.groovy` file basename = step name; a Groovy identifier, conventionally camelCased. The matching `.txt` is help text.
- `src/` is plain Groovy classes on the classpath; good for logic, but classes don't get
  pipeline steps for free — pass the script context in (`new Docker(this)`) and call
  `script.sh(...)`.

## 2. A config-map step that whole pipelines call
```groovy
// vars/buildService.groovy
def call(Map cfg = [:]) {
  def c = [jdk: '21', deploy: false] + cfg          // defaults
  if (!c.name) error 'buildService: name is required'
  pipeline {
    agent { label "jdk${c.jdk}" }
    options { timeout(time: 30, unit: 'MINUTES') }
    stages {
      stage('Build') { steps { sh './gradlew build' } }
      stage('Deploy') {
        when { beforeAgent true; expression { c.deploy && env.BRANCH_NAME == 'main' } }
        steps { deployTo(env: 'staging', service: c.name) }
      }
    }
  }
}
```
App Jenkinsfile:
```groovy
@Library('acme-ci@v4') _
buildService name: 'orders', deploy: true
```
- A step may declare a whole `pipeline {}` (only in `vars/*.groovy`, in `call`) — only one
  Declarative Pipeline can run per build.
- Validate inputs and fail with clear `error` messages; this is your API.
- The `_` after `@Library` is needed when you don't import anything.

## 3. CPS rules (where library bugs come from)
Pipeline Groovy is CPS-transformed so builds survive controller restarts. Consequences:
- Local variables must be serializable at every step boundary. Iterators, `Matcher`,
  `JsonSlurper` results (`LazyMap`) are not → `NotSerializableException`.
  Use `readJSON` (Pipeline Utility Steps) or convert to plain maps/lists.
- Mark pure-computation helpers `@NonCPS` (sorting, regex, parsing). A `@NonCPS` method
  **must not call pipeline steps** (`sh`, `echo`, `node`) — behaviour is undefined/broken.
- Closures passed to `.each`, `.collect` etc. historically misbehaved under CPS; plain
  `for` loops are safest in CPS code.

## 4. Trusted vs untrusted
- **Global Trusted Pipeline Libraries** (*Manage Jenkins › System*) are **trusted**: they
  can run any Java/Groovy method and Jenkins internal APIs. Anyone who can push to that
  repo is effectively a Jenkins admin → protect the branch/tags, require review. With only
  Overall/Manage permission a user can configure only untrusted (sandboxed) global libraries.
- **Folder-scoped libraries** are always untrusted (sandboxed) — appropriate for team-owned libraries.
- Prefer putting privileged operations in a small trusted library and keeping the rest sandboxed.

## 5. Versioning
- Default version + "Allow default version to be overridden" in the library config (the default is used for implicit load or name-only references);
  pin in Jenkinsfiles: `@Library('acme-ci@v4.2.0')`.
- "Load implicitly" saves the annotation but makes every pipeline track the default
  version — one bad commit breaks all builds. Use implicit load only with a tag as default.
- Release with semver tags; keep a changelog; test a library branch on a real job with
  `@Library('acme-ci@feature-x')` (if override allowed) before tagging.
- `library('acme-ci@v4')` (step form) loads dynamically, mid-pipeline — useful when the version comes from a parameter. It cannot override the version of an implicitly loaded library.
- On GitHub-hosted libraries, `@Library('lib@pull/<n>/head') _` tests a library PR in place (see the docs for the SCM requirement).

## 6. Testing
- **JenkinsPipelineUnit** (Gradle/Maven): load `vars/` scripts, mock steps
  (`helper.registerAllowedMethod('sh', [Map], { m -> 'ok' })`), assert the call stack.
  Catches logic and wiring bugs; does **not** reproduce CPS serialization issues.
- Add an integration job on a staging Jenkins that runs a sample Jenkinsfile against each library PR.

## Uncertainty
CPS closure support has improved across workflow-cps versions; the `@NonCPS` rules above
are the conservative reading. Not hands-on verified here.

## Verify
- [ ] App Jenkinsfiles pin a tagged library version; implicit load (if used) defaults to a tag.
- [ ] Trusted library repo has protected branches/tags and mandatory review.
- [ ] No `@NonCPS` method calls a pipeline step.
- [ ] Steps validate their config map and have a `vars/*.txt` help file.
- [ ] JenkinsPipelineUnit suite runs on every library PR, plus one real-Jenkins smoke job.

## Checked
2026-11-02. Confirmed against the Jenkins Shared Libraries handbook page and the JenkinsPipelineUnit README: directory layout (vars, src, resources, vars/*.txt), naming, libraryResource, trusted vs untrusted and folder-scoped libraries, @Library forms with _, version pinning and default/override options, library step limits, one Declarative Pipeline per build, Serializable state, registerAllowedMethod. Corrected trusted-library wording. The @NonCPS and closure advice is not stated on that page and stays under the existing Uncertainty note (conservative guidance, not a documented figure).
Method: documentation only; no commands were run.
