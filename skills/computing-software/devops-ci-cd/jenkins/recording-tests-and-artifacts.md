---
id: computing-software.devops-ci-cd.jenkins.recording-tests-and-artifacts
name: recording-tests-and-artifacts
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, test-reporting, junit-step, junit-plugin, test-results, test-result-trend, unstable-build, allow-empty-results, skip-publishing-checks, warnings-ng, record-issues, static-analysis, quality-gates, coverage-plugin, record-coverage, jacoco, cobertura, archiveartifacts, artifact-archiving, fingerprint, copyartifact, publish-html, htmlpublisher, build-discarder, artifact-manager-s3, test-stability, flaky-test-handler, checks-api]
level: practitioner
status: docs-checked
description: "Record Jenkins build outputs: junit unstable semantics, warnings-ng recordIssues, the Coverage plugin, archiveArtifacts with fingerprints, copyArtifact and retention."
sources: ["https://www.jenkins.io/doc/pipeline/tour/tests-and-artifacts/", "https://plugins.jenkins.io/junit/", "https://plugins.jenkins.io/warnings-ng/", "https://plugins.jenkins.io/coverage/", "https://plugins.jenkins.io/copyartifact/", "https://plugins.jenkins.io/htmlpublisher/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recording tests and artifacts

**Goal:** the build page tells you *which* test failed, *how* coverage and warnings
trended, and gives you the exact binary — without hoarding gigabytes forever.

## 1. junit
```groovy
post {
  always {
    junit testResults: '**/target/surefire-reports/*.xml, **/junit-*.xml',
          skipPublishingChecks: false    // true disables the junit check
  }
}
```
Semantics: with at least one test failure `junit` marks the build UNSTABLE unless
`skipMarkingBuildUnstable: true` (reporting only); `skipMarkingStageUnstable` does the same
for the stage. The `sh 'mvn test'` step itself fails the build if Maven returns non-zero, so
make the test command not fail the step (for example `mvn -Dmaven.test.failure.ignore=true`
or `sh(returnStatus: true)`) and let `junit` decide. Tag flaky tests and quarantine them in a
separate non-blocking stage.

## 2. Static analysis: warnings-ng
```groovy
recordIssues tools: [java()]      // pick parsers for your tools; generate the exact syntax with the Snippet Generator
```
The plugin has built-in support for more than a hundred report formats, shows new, fixed and
outstanding issues and trends, and lets you define custom Groovy parsers. See the
*Pipeline Step Reference* for `recordIssues` options (quality gates, reference build).

## 3. Coverage
```groovy
recordCoverage tools: [[parser: 'JACOCO']],
  sourceCodeRetention: 'EVERY_BUILD',
  qualityGates: [[threshold: 60.0, metric: 'LINE', baseline: 'PROJECT', unstable: true],
                 [threshold: 60.0, metric: 'BRANCH', baseline: 'PROJECT', unstable: true]]
```
The **Coverage** plugin computes coverage of the project, the modified files and the modified
lines, and reports to GitHub checks. Quality gate `baseline` is `PROJECT`, `MODIFIED_FILES`
or `MODIFIED_LINES` (or their `_DELTA` forms). Parsers include JaCoCo, Cobertura, OpenCover,
Go, LCOV and Open Clover.

## 4. Artifacts and fingerprints
```groovy
archiveArtifacts artifacts: 'target/*.jar, build/reports/**', fingerprint: true
```
- Big artifacts belong in an artifact repository rather than on the controller's disk.
- **Fingerprints** let Jenkins track which builds used a given file across jobs.
- `copyArtifacts projectName: 'build/app/main', filter: 'target/*.jar', target: 'input/', fingerprintArtifacts: true, flatten: true`
  (Copy Artifact plugin; `selector` defaults to the latest stable build; the plugin checks
  permissions on the source job, see its README "Permissions to copy artifact"). Prefer
  `stash`/`unstash` within a run; copy across jobs only for deploy-from-last-good flows.
- `stash` is for small, same-run transfer.

## 5. HTML reports
`publishHTML target: [reportDir: 'build/reports/e2e', reportFiles: 'index.html', reportName: 'E2E Report', keepAll: true, allowMissing: false]`.
Jenkins' Content Security Policy restricts scripts and styles in served reports; see the
HTML Publisher plugin page before relaxing it, and prefer serving reports from elsewhere.

## 6. Retention
```groovy
options { buildDiscarder(logRotator(numToKeepStr: '50', artifactNumToKeepStr: '10')) }
```
Artifacts are usually the disk hog: keep `artifactNumToKeepStr` far smaller than the builds
kept, and watch per-job disk usage under `$JENKINS_HOME/jobs`.

## Verify
- [ ] A failing test turns the build yellow with the test name and stdout on the build page.
- [ ] warnings-ng shows 0 NEW on a clean PR and flags an injected `TODO`/lint error as NEW.
- [ ] Coverage page shows modified-line coverage for a PR; gate turns unstable below threshold.
- [ ] The fingerprint page for a jar lists the producing build and the builds that used it.
- [ ] Disk usage per job stays bounded after discarder settings.

## Checked
2026-11-02. Confirmed against the JUnit, Coverage, Warnings Next Generation, Copy Artifact and HTML Publisher plugin pages: junit skipPublishingChecks, skipMarkingBuildUnstable/skipMarkingStageUnstable and the UNSTABLE-on-failure default; recordCoverage tools/parsers/sourceCodeRetention/quality-gate properties and baselines; Copy Artifact parameters (projectName, selector default, filter, target, flatten, fingerprintArtifacts) and permission checking; warnings-ng built-in parser count. Corrected: coverage quality gates use unstable: true (not criticality) and LCOV is a native parser. Removed: junit keepLongStdio/AttachmentPublisher/allowEmpty claims and log messages, recordIssues tool list and gate types, archive path, S3 artifact manager, stash size, CSP and resource-root advice, retention days figure.
Method: documentation only; no commands were run.
