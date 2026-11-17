---
id: computing-software.messaging-and-integration.apache-pulsar.broker-rolling-upgrade
name: broker-rolling-upgrade
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [rolling-upgrade, broker-shutdown, bundle-unload, graceful-shutdown, load-shedding, termination-grace-period]
level: advanced
status: docs-checked
description: "Roll Pulsar brokers with minimal disruption: what happens on SIGTERM, rate-limited brokers shutdown, SIGKILL lease risk and pausing load shedding and bundle splitting."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/administration-rolling-upgrade.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restart or replace brokers one at a time while keeping client disruption small.

The controlled procedures are optional. On Kubernetes the Helm chart default `RollingUpdate` strategy works; the main setting to tune is `terminationGracePeriodSeconds` (`broker.gracePeriod` in the chart), long enough for the broker to drain bundles. Default rollouts can cause client micro-outages from seconds to minutes. Use the controlled approach when that is unacceptable.

Shutdown sequence on `SIGTERM` or `pulsar-admin brokers shutdown`:
1. The broker disables itself in the load manager so it takes no new bundles.
2. It releases its bundles. Modular load manager: unloads bundles one after another (topics of a bundle closed in parallel), then releases ownership in the metadata store. Extensible load manager: picks new owners and transfers ownership through the ownership channel.
3. It closes remaining services and exits; `brokerShutdownTimeoutMs` (60 seconds) bounds only this last step.
Measure both the disable phase and the unload phase when sizing the grace period.

Leases: with the modular manager bundle ownership is a lease tied to the metadata-store session (ephemeral znode or record). A `SIGKILL` (`kill -9`) skips shutdown hooks, so the session can linger and the bundles stay unavailable until it expires. A replacement with the same advertised ownership information can reclaim the lease early.

Rate-limited drain (modular manager):
```shell
pulsar-admin --admin-url http://broker-0.example.com:8080 brokers shutdown --max-concurrent-unload-per-sec 5
```
Target the individual broker's admin URL; sending it through a shared Service or proxy can shut down a different broker. `--forced-terminate-topic` closes topics without waiting for clients to disconnect. With the extensible manager the option does not throttle transfers, which happen earlier.

Pause automatic rebalancing during the roll:
```shell
pulsar-admin brokers update-dynamic-config --config loadBalancerSheddingEnabled --value false
pulsar-admin brokers update-dynamic-config --config loadBalancerAutoBundleSplitEnabled --value false
```
Wait for the settings to apply before stopping the first broker; re-enable afterwards. Pausing does not stop graceful-shutdown transfers, manual unloads or crash recovery, and does not stop assignment of unowned bundles.

Before stopping the next broker, wait for the restarted one to appear in `pulsar-admin brokers list <cluster-name>` and for `pulsar-admin --admin-url http://broker-0.example.com:8080 brokers healthcheck` to pass against its own admin URL (a check through a shared Service or proxy can succeed on another broker).

## Checked

2026-11-03. Confirmed against the Pulsar rolling upgrade page: default RollingUpdate and `terminationGracePeriodSeconds`/`broker.gracePeriod`, shutdown phases, `brokerShutdownTimeoutMs` (60 seconds) scope, ownership leases and forced termination, `brokers shutdown --max-concurrent-unload-per-sec` and `--forced-terminate-topic`, pausing `loadBalancerSheddingEnabled` and `loadBalancerAutoBundleSplitEnabled`, and the brokers list/healthcheck wait steps. Removed: the generic watch-reconnects Verify line, replaced with the page's two wait checks.

Method: documentation only; no commands were run.
