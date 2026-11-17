---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-scenario-start-time-and-per-scenario-options
name: k6-scenario-start-time-and-per-scenario-options
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [starttime, k6-scenarios, scenario-tags, scenario-env, exec-function]
level: practitioner
status: verified
description: "Sequence and overlay k6 scenarios with startTime, and give each scenario its own exec function, env vars and tags so results can be sliced per scenario."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/
  - https://grafana.com/docs/k6/latest/using-k6/scenarios/advanced-examples/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduling scenarios with startTime and per-scenario env and tags

```js
export const options = {
  scenarios: {
    warmup: {
      executor: 'constant-arrival-rate', rate: 10, timeUnit: '1s', duration: '2m', preAllocatedVUs: 10,
      exec: 'browse', tags: { phase: 'warmup' },
    },
    peak_browse: {
      executor: 'ramping-arrival-rate', startTime: '2m30s', startRate: 10, timeUnit: '1s',
      stages: [{ target: 200, duration: '5m' }, { target: 200, duration: '10m' }],
      preAllocatedVUs: 100, maxVUs: 400,
      exec: 'browse', tags: { phase: 'peak' },
    },
    batch_job: {
      executor: 'per-vu-iterations', vus: 1, iterations: 1, startTime: '8m', maxDuration: '10m',
      exec: 'runReport', env: { REPORT_SIZE: 'large' }, tags: { phase: 'peak', flow: 'report' },
    },
  },
  thresholds: {
    'http_req_duration{phase:peak}': ['p(95)<400'],
    'http_req_duration{scenario:batch_job}': ['p(95)<5000'],
  },
};
export function browse() { /* ... */ }
export function runReport() { const size = __ENV.REPORT_SIZE; /* ... */ }
```

## Notes
- `startTime` is relative to test start. Overlapping scenarios model concurrent workloads (browse + batch job during peak).
- Every metric gets an automatic `scenario` tag; custom `tags` add more dimensions.
- `env` values are per scenario and override global `__ENV` keys for that scenario (run: `-e REPORT_SIZE=small` on the command line, `batch_job` saw `large`; other `-e` keys such as `G=global` stayed visible).
- `exec` defaults to `default`.

## Gotchas
- Thresholds on sub-metrics need the tag to exist; a typo yields a threshold over no data that passes vacuously with no warning: `http_req_duration{phase:typo}` with `p(95)<1` reported `p(95)=0s` and passed on k6 2.3.0 (also in the custom-metrics skill's check). Confirm each sub-metric threshold shows a real value in the summary.
- Remember gracefulStop when sequencing; otherwise the tail of one phase overlaps the next.
- Total test duration = max(startTime + duration + gracefulStop) across scenarios (for `per-vu-iterations` use `maxDuration`, default 10m). k6 prints it at start: `10m34s max duration (incl. graceful stop)` for `startTime: 4s` + `maxDuration: 10m` + 30 s grace. `startTime` accepts `2s500ms` (printed as `startTime: 2.5s`).

## Verify
Per-phase thresholds appear in the end summary; Grafana panels filtered by `phase` show the expected timeline.
