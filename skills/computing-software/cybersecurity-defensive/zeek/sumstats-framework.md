---
id: computing-software.cybersecurity-defensive.zeek.sumstats-framework
name: sumstats-framework
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, sumstats, observations, reducers, epoch-threshold]
level: advanced
status: docs-checked
description: "Summary Statistics framework: observations, reducers, sumstats with epochs and thresholds, cluster-transparent counting, connection example."
sources: ["https://docs.zeek.org/en/current/frameworks/sumstats.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# sumstats framework

SumStats measures unbounded data sets on clustered and non-clustered Zeek alike. Cluster complications from flow-based load balancing are handled transparently.

Concepts:

- **Observation**: one data point in a named observation stream, with a key (what it is about) and the value.
- **Reducer**: applies calculations (such as `SumStats::SUM`) to a stream. Results are kept per key, so keep the number of keys reasonable.
- **Sumstat**: one or more reducers collected over an epoch, with threshold callbacks and an `$epoch_result` callback for each key at epoch end.

```
@load base/frameworks/sumstats

event connection_established(c: connection)
    {
    SumStats::observe("conn established", SumStats::Key(), SumStats::Observation($num=1));
    }

event zeek_init()
    {
    local r1 = SumStats::Reducer($stream="conn established", $apply=set(SumStats::SUM));
    SumStats::create([$name = "counting connections",
                      $epoch = 1min,
                      $reducers = set(r1),
                      $epoch_result(ts: time, key: SumStats::Key, result: SumStats::Result) =
                        {
                        print fmt("Number of connections established: %.0f", result["conn established"]$sum);
                        }]);
    }
```

The `$sum` value is a double, hence the `%f` style format. Thresholding is demonstrated in a toy scan detector built on the `connection_attempt` event, which flags hosts crossing a threshold of attempts.

## Checked

2026-11-08. Read the Summary Statistics page in full; every claim confirmed.

Method: documentation only; no commands were run.
