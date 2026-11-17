---
id: computing-software.cloud-infrastructure-engineering.azure.cosmos-db-sdk-best-practices
name: cosmos-db-sdk-best-practices
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, cosmos-db, cosmos-sdk, direct-mode, preferred-regions, singleton-client, retry-429]
level: advanced
status: docs-checked
description: "Configure Cosmos DB SDK clients for performance and resilience: singleton client, direct mode, preferred regions, 429 handling, bulk mode and diagnostics."
sources: ["https://learn.microsoft.com/azure/cosmos-db/nosql/best-practice-dotnet", "https://learn.microsoft.com/azure/cosmos-db/nosql/sdk-connection-modes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cosmos DB SDK best practices

**Goal:** low latency and correct behaviour under throttling and regional outages.

## Client setup (.NET v3)
```csharp
var options = new CosmosClientOptions {
    ConnectionMode = ConnectionMode.Direct,                       // direct mode for best performance
    ApplicationPreferredRegions = new[] { "West Europe", "North Europe" },
    HttpClientFactory = () => new HttpClient(sharedSocketsHandler, disposeHandler: false)
};
var client = new CosmosClient("<connection-string>", options);   // keep one instance for the app lifetime
```
- **One client per account for the lifetime of the application** (singleton, DI). A single client can talk to every database, container and partition key in the account.
- Set `ApplicationPreferredRegions` or `ApplicationRegion`: reads go to the first region in the list and writes go to the current write region; enable service-managed failover for production accounts and run the app in the same region as the account.
- Customise `SocketsHttpHandler.PooledConnectionLifetime` (Microsoft suggests starting at 5 minutes) so HTTP connections react to DNS changes.
- In Gateway mode, raise the connection limit with `CosmosClientOptions.GatewayModeMaxConnectionLimit`.
- For direct mode on sparse workloads, tune `IdleTcpConnectionTimeout` (at least 10 minutes) and `PortReuseMode` (`PrivatePortPool`) to control ephemeral port use.

## Request patterns
- Avoid blocking calls (`Task.Result`, `Task.Wait`); keep the whole call stack async.
- Always pass the partition key; cross-partition queries fan out. Set `MaxConcurrency` in the query request options to the number of partitions (or start high and reduce).
- Enable **bulk support** for loading large volumes of data when latency is not the priority.
- Set `EnableContentResponseOnWrite` to `false` on write-heavy workloads so the service doesn't return the written item (this also disables the response from a trigger operation).
- Exclude unused paths from the indexing policy for faster writes; smaller documents cost less per operation.
- Cache database and container names or read them from configuration; metadata calls (`ReadDatabaseAsync`, `CreateIfNotExists`) consume the system-reserved RU limit.
- In performance tests, back off by the `RetryAfter` interval on 429 responses.
- Use `RequestTimeout` together with a `CancellationToken` for end-to-end timeouts.

## Diagnostics
- Every response and `CosmosException` carries a `Diagnostics` property; log it when elapsed time exceeds a threshold. Don't parse the string, as its format changes between versions.
- Monitor client CPU: lack of client resources causes connectivity and availability problems; Microsoft recommends at least 4 cores and 8 GB for latency-sensitive direct-mode workloads, and Accelerated Networking on VMs.
- Add an explicit `Newtonsoft.Json` reference (13.0.3 or higher) in .NET projects, as the SDK does not manage it for you.

## Verify
- [ ] One `CosmosClient` per account; diagnostics show direct mode and the preferred region.
- [ ] Load test: 429 rate, per-partition RU consumption and client CPU stay within your targets.

## Checked

2026-10-24, against the Azure Cosmos DB .NET SDK v3 best-practices article (updated 2026-06-15): singleton client, direct mode, ApplicationPreferredRegions and ApplicationRegion behaviour, service-managed failover, PooledConnectionLifetime guidance, GatewayModeMaxConnectionLimit, IdleTcpConnectionTimeout and PortReuseMode, async guidance, MaxConcurrency, bulk support, EnableContentResponseOnWrite, metadata call caching, RetryAfter backoff, end-to-end timeouts, Diagnostics usage, 4-core 8 GB hosting advice, Newtonsoft.Json requirement. Removed the unconfirmed Java builder calls, default retry settings, the 10000-20000 port range, the ~1 RU per KB point-read figure, the p99 latency target and the Azure Monitor metric names.

Method: documentation only; no commands were run.
