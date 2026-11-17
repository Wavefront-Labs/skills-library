---
id: computing-software.devops-ci-cd.jenkins.testing-job-dsl-scripts-with-gradle
name: testing-job-dsl-scripts-with-gradle
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, job-dsl-testing, job-dsl, seed-job]
level: advanced
status: docs-checked
description: "Unit test Job DSL scripts before the seed job runs them: a Gradle/Spock harness with JenkinsRule that executes every DSL file and fails on errors."
sources: ["https://github.com/sheehan/job-dsl-gradle-example", "https://github.com/jenkinsci/job-dsl-plugin/wiki/Testing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Job DSL scripts with Gradle

A broken DSL script fails the seed job. Test DSL in CI first.

## Harness (based on job-dsl-gradle-example)
```
build.gradle
jobs/**/*.groovy          # DSL scripts
src/test/groovy/JobScriptsSpec.groovy
```
```groovy
// build.gradle: copy the dependency and plugin configuration from job-dsl-gradle-example
// and pin plugin versions to match production.
```
```groovy
class JobScriptsSpec extends Specification {
  @Shared @ClassRule JenkinsRule jenkins = new JenkinsRule()
  @Unroll def 'script #file.name'(File file) {
    when:
    new DslScriptLoader(new JenkinsJobManagement(System.out, [:], new File('.')))
        .runScript(file.text)
    then:
    noExceptionThrown()
    where:
    file << new FileNameFinder().getFileNames('jobs', '**/*.groovy').collect { new File(it) }
  }
}
```
Plugins providing auto-generated DSL must be added to the build dependencies (see the example repo's build.gradle), otherwise dynamic DSL methods are missing. Match production plugin versions.

## Extras
- The example harness writes generated XML to `build/debug-xml`; inspect it before check-in.
- Run on every PR touching `jobs/`.

## Verify
- [ ] Introducing a typo in a DSL file fails `./gradlew test` with the file name in the report.

## Checked

2026-10-28. Confirmed against the job-dsl-gradle-example README: JobScriptsSpec loops through all DSL files and fails on exceptions, XML output goes to build/debug-xml, plugins providing auto-generated DSL must be build dependencies. Removed: hard-coded dependency coordinates and versions (not verifiable here) and the removed-job-action claim.

Method: documentation only; no commands were run.
