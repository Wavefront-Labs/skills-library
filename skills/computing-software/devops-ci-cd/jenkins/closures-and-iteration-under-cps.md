---
id: computing-software.devops-ci-cd.jenkins.closures-and-iteration-under-cps
name: closures-and-iteration-under-cps
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, cps, cps-closures, cps-iteration, groovy-cps, noncps, each-closure, collect, sort-comparator, notserializableexception, parallel-map, scripted-pipeline, groovy]
level: advanced
status: docs-checked
description: "Write loops and closures that survive Jenkins CPS: which Groovy collection methods misbehave, building parallel branch maps, @NonCPS rules and NotSerializableException fixes."
sources: ["https://www.jenkins.io/doc/book/pipeline/cps-method-mismatches/", "https://www.jenkins.io/doc/book/pipeline/scaling-pipeline/", "https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closures and iteration under CPS

Pipeline Groovy is transformed into continuation-passing style (CPS) so a run can be
paused, serialised to disk and resumed. Most surprises come from code that crosses the
CPS / non-CPS boundary.

## 1. Loops that work
```groovy
def services = ['api', 'web', 'worker']
for (int i = 0; i < services.size(); i++) { echo services[i] }   // always fine
for (s in services) { echo s }                                  // fine
```
The Pipeline CPS method-mismatch guide says many standard-library methods that take a closure work
since the JENKINS-26481 fix, but some remain unfixed, notably `Iterable.toSorted { a, b -> ... }`
with a comparator closure: the CPS-transformed closure is passed to non-CPS Java, the call
returns the first closure result (`-1` in the guide's example), and the log shows
`expected to call java.util.ArrayList.toSorted but wound up catching ...CpsClosure2.call`.
Fix it by wrapping the problematic call in a `@NonCPS` method, or by an explicit class whose
methods are all `@NonCPS`. The same warning shape appears for `@NonCPS` methods that call steps,
constructors that call CPS methods, overrides of non-CPS methods (such as `toString`), and
closures inside a `GString` (use a closure that returns a GString instead).

## 2. Building parallel branches
```groovy
def branches = [:]
for (svc in ['api', 'web']) {
  def name = svc                     // capture a fresh variable per iteration
  branches["test-${name}"] = {
    node('linux') { sh "make test SERVICE=${name}" }
  }
}
parallel branches
```
Capturing a fresh variable per iteration keeps each branch's closure bound to its own value
rather than to the shared loop variable.

## 3. @NonCPS: pure data crunching only
```groovy
@NonCPS
def parseVersions(String json) {
  new groovy.json.JsonSlurperClassic().parseText(json).collect { it.version }.sort()
}
```
Rules (Pipeline scaling guide and CPS method-mismatch guide): do not use Pipeline steps
inside (`node`, `sh` and similar give anomalous behaviour; store a step's result in a variable
and pass it in instead), parameters and return types should stay Serializable, and the body may
use non-serialisable types such as regex matchers internally and a broader subset of Groovy.
Use it for comparator sorting and regex matching. Prefer a `sh` step that does the parsing
over `JsonSlurper`: the Pipeline best-practices guide lists `JsonSlurper` among Groovy
methods to avoid because Groovy always runs on the controller.

## 4. NotSerializableException
A `NotSerializableException` for a type such as `java.util.regex.Matcher` means a
non-serialisable object was a local variable when the Pipeline had to save state. Normal
Pipeline code is restricted to serialisable local variables (Pipeline scaling guide). Fix it by
doing the work in a @NonCPS method that returns plain String/List/Map values, so the
non-serialisable object never lives in Pipeline code.

## 5. Keep logic out of Groovy
Pipeline Groovy always executes on the controller using its memory and CPU, so the best-practices
guide says to reduce the amount of Groovy executed. Push data processing into a `sh` step on an
agent and read back a small result.

## Verify
Run the loop with `echo` in each branch and confirm distinct values; check the build log
for `expected to call` CPS mismatch warnings; resume test: restart the controller mid-run
and confirm the pipeline continues (catches serialisation bugs).

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed: CPS method-mismatch guide (`@NonCPS` methods must not call steps, `Iterable.toSorted` with a closure, warning text `expected to call ... but wound up catching ...`, constructor, override and GString cases); Pipeline scaling guide (`@NonCPS` functions may use non-serialisable types internally, parameters and return types should be Serializable); best-practices guide (Groovy runs on the controller, avoid `JsonSlurper`). Removed per-method support lists and plugin-version claims that no documentation read confirmed.
Method: documentation only; no commands were run.
