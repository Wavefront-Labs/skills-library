---
id: computing-software.digital-forensics-incident-response.log-analysis.velociraptor-server-artifacts-and-automation
name: velociraptor-server-artifacts-and-automation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [velociraptor-server-artifacts, velociraptor, vql, automation, server-event-monitoring, dfir]
level: advanced
status: draft
description: "Automate Velociraptor with server artifacts: SERVER and SERVER_EVENT types, reacting to flow completions, auto-collecting on new clients, post-processing results and sending alerts."
sources: ["https://docs.velociraptor.app/docs/server_automation/", "https://docs.velociraptor.app/docs/server_automation/server_monitoring/", "https://docs.velociraptor.app/vql_reference/server/", "https://docs.velociraptor.app/artifact_references/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Velociraptor server artifacts and automation

Artifacts have a `type`: `CLIENT` (run on endpoints), `CLIENT_EVENT`, `SERVER` (run once on the server) and `SERVER_EVENT` (run continuously on the server, reacting to events). Server artifacts use server-only VQL plugins to schedule collections, read results and integrate with other tools.

## Useful server VQL
- `collect_client(client_id=..., artifacts=[...], env=dict(...))`: schedule a collection.
- `hunt(artifacts=[...], description=..., ...)`: create a hunt.
- `watch_monitoring(artifact='System.Flow.Completion')`: stream events as flows finish (also `System.Hunt.Creation`, `Server.Internal.ClientInfo`, `System.Upload.Completion`, and client event artifacts' results).
- `source(client_id=..., flow_id=..., artifact=...)`: read a flow's results.
- `clients(search='label:Compromised')`, `label(client_id=..., labels=[...], op='set')`.
- `http_client()` (webhooks to Slack/Teams/SOAR), `mail()` (SMTP), `execve()` on the server (use with care).

## Example: auto-triage new clients with a label
```yaml
name: Custom.Server.AutoTriageOnLabel
type: SERVER_EVENT
sources:
  - query: |
      SELECT collect_client(client_id=ClientId,
               artifacts=['Windows.KapeFiles.Targets'],
               env=dict(KapeTriage='Y')) AS Scheduled
      FROM watch_monitoring(artifact='Server.Internal.Label')
      WHERE Operation = 'Add' AND Label = 'Triage'
```
(`Server.Internal.Label` emits label changes; check event names in your version.)

## Example: alert when a flow finds YARA hits
```yaml
name: Custom.Server.AlertOnYaraHits
type: SERVER_EVENT
sources:
  - query: |
      LET completions = SELECT * FROM watch_monitoring(artifact='System.Flow.Completion')
        WHERE Flow.artifacts_with_results =~ 'Yara'
      SELECT * FROM foreach(row=completions, query={
        SELECT http_client(url='https://hooks.example/ir', method='POST',
               data=serialize(item=dict(client=ClientId, flow=FlowId))) FROM scope()
      })
```

## Enabling
Server event artifacts run when added in **Server Events** (GUI: Server Events > Update server monitoring table). Server artifacts (non-event) run from **Server Artifacts** on demand. Built-in examples: `Server.Monitor.Health`, `Server.Utils.CreateCollector`, `Server.Alerts.*`, notification integrations.

## Gotchas
- Automation can schedule many collections quickly; add guards (labels, rate limits) to avoid overloading clients or the server.
- Secrets (webhook URLs, SMTP passwords) belong in server secrets/configuration, not hard-coded in artifacts.
- Server artifacts run with server privileges; restrict who can create or edit them (`artifact_writer`, `server_admin` roles).

## Verify
Triggering the condition on a test client (adding the label, running a YARA hunt) produces the expected scheduled collection or alert, visible in the server artifact's results.
