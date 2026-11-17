---
id: computing-software.devops-ci-cd.jenkins.waituntil-and-sleep-steps
name: waituntil-and-sleep-steps
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, waituntil, sleep-step, pipeline-steps]
level: practitioner
status: docs-checked
description: "Poll for external conditions in Jenkins pipelines with waitUntil (initialRecurrencePeriod, quiet) wrapped in timeout, instead of shell loops; when sleep is the right tool."
sources: ["https://www.jenkins.io/doc/pipeline/steps/workflow-basic-steps/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# waitUntil and sleep steps

```groovy
timeout(time: 15, unit: 'MINUTES') {
  waitUntil(initialRecurrencePeriod: 15000, quiet: true) {
    def code = sh(script: 'curl -s -o /dev/null -w "%{http_code}" https://app.example.com/healthz',
                  returnStdout: true).trim()
    return code == '200'
  }
}
```

## Semantics (from the step reference)
- The body runs repeatedly until it returns `true`; on `false` the step waits and tries again.
- **If the body throws an error, it propagates immediately; it is not treated as false.** Catch
  errors inside the body (for example `sh(returnStatus: true)`, or `try`/`catch` returning
  `false`) if a failing probe should just retry.
- `initialRecurrencePeriod` (milliseconds, default 250) is the first wait; each failure slows
  the delay, up to a maximum of 15 seconds.
- There is no limit to the number of retries, so **always wrap in `timeout`**.
- `quiet: true` stops the step logging a message each time the condition is checked (default false).

## sleep
```groovy
sleep time: 90, unit: 'SECONDS'
```
`unit` defaults to `SECONDS`; other values: NANOSECONDS, MICROSECONDS, MILLISECONDS, MINUTES,
HOURS, DAYS. The docs describe it as pausing the build, equivalent to `sh 'sleep ...'` on Unix, and
usable to pause one `parallel` branch while another proceeds. Use it for fixed bake times (a
canary soak) rather than polling.

## Prefer waitUntil over shell loops
- A shell loop such as `sh 'while ...; do sleep 5; done'` hides the polling in one opaque step;
  `waitUntil` retries at the Pipeline level with its own backoff and logging control.

## Verify
- [ ] A simulated unhealthy endpoint makes the build time out after 15 minutes as intended.

## Checked
2026-10-31. Confirmed on the Jenkins Pipeline Basic Steps reference: `waitUntil` repeat semantics, errors thrown immediately, `initialRecurrencePeriod` in ms default 250, 15 s maximum delay, no retry limit, `quiet` default false; `sleep` `time`, `unit` default SECONDS and values, equivalence to `sh 'sleep'`. Fixed: errors inside the body are not counted as false. Removed unconfirmed claims: 1.2x growth factor, resumability across controller restarts, executor and abort behaviour of shell loops, and `httpRequest` advice.
Method: documentation only; no commands were run.
