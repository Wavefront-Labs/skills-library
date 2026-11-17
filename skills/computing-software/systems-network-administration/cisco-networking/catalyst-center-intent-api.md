---
id: computing-software.systems-network-administration.cisco-networking.catalyst-center-intent-api
name: catalyst-center-intent-api
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst-center, dnac, intent-api, rest-api, python, network-automation, command-runner]
level: practitioner
status: draft
description: "Use the Catalyst Center (DNA Center) intent API: token auth, device inventory queries, async tasks and command runner, with curl and the dnacentersdk."
sources:
  - https://developer.cisco.com/docs/dna-center/
  - https://github.com/cisco-en-programmability/dnacentersdk
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Catalyst Center intent API

Catalyst Center (formerly DNA Center) exposes REST under `/dna/intent/api/v1/`.

## Auth
```bash
TOKEN=$(curl -sk -u "$CC_USER:$CC_PASS" -X POST https://cc.example.com/dna/system/api/v1/auth/token | jq -r .Token)
curl -sk -H "X-Auth-Token: $TOKEN" "https://cc.example.com/dna/intent/api/v1/network-device?family=Switches%20and%20Hubs" | jq '.response[] | {hostname, managementIpAddress, softwareVersion, reachabilityStatus}'
```
Tokens last about an hour.

## Async pattern
Writes (and command runner) return a `taskId`; poll it:
```bash
curl -sk -H "X-Auth-Token: $TOKEN" https://cc.example.com/dna/intent/api/v1/task/$TASK_ID | jq .response
```
When `progress` contains a `fileId`, download results from `/dna/intent/api/v1/file/{fileId}`.

## Python SDK
```python
from dnacentersdk import api
cc = api.DNACenterAPI(base_url="https://cc.example.com", username=u, password=p, verify=False, version="2.3.7.6")
devs = cc.devices.get_device_list(family="Switches and Hubs")
task = cc.command_runner.run_read_only_commands_on_devices(
    commands=["show version"], deviceUuids=[d.id for d in devs.response][:5])
```
Match `version` to your Catalyst Center release.

## Practice
- Read-only first: inventory, health (`/site-health`, `/device-health`), compliance.
- Pagination: `offset`/`limit` (max 500 for devices); loop until fewer results return.
- Rate limits exist per API; back off on 429.
- Use a dedicated API account with the least role needed (Observer for reads).
- Changes made through templates/intent are tracked in Catalyst Center; direct CLI changes cause compliance drift.

## Verify
- [ ] Script authenticates, lists all devices with pagination, and handles task polling to completion.
