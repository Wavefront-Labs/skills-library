---
id: computing-software.cloud-infrastructure-engineering.azure.image-builder-customization-log-troubleshooting
name: image-builder-customization-log-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-images, aib-troubleshooting, customization-log, image-builder, staging-resource-group]
level: advanced
status: docs-checked
description: "Debug Azure VM Image Builder failures: run status, the customization.log in the staging resource group, identity and network errors, timeouts, VM size and sysprep issues."
sources: ["https://learn.microsoft.com/azure/virtual-machines/linux/image-builder-troubleshoot", "https://learn.microsoft.com/azure/virtual-machines/linux/image-builder-json", "https://learn.microsoft.com/azure/virtual-machines/linux/image-builder-permissions-cli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image Builder troubleshooting

**Goal:** find the failing step in an Image Builder run in minutes.

## Status first
```bash
az image builder show -g rg-img -n tpl-web2022 --query "{state:provisioningState,last:lastRunStatus}"
az image builder show-runs -g rg-img -n tpl-web2022 -o table
```
- For image build failures, get the error from `lastRunStatus` (`runState`), then read `customization.log`.

## The customization log
Each template has a staging resource group `IT_<rg>_<template>_<guid>` containing a storage account; container
`packerlogs` holds `<run>/customization.log`. Search for `error`, the failing customizer name, and the last customizer that ran (`(telemetry)` lines). You can set `stagingResourceGroup` in the template to a group you choose.

## Common failures
| Symptom | Cause / fix |
|---|---|
| Customization times out | Raise `buildTimeoutInMinutes` (default 4 hours) if the customizations need more time |
| Windows restart takes too long | Increase `restartTimeout` (the troubleshooting page raises it from 15 to 30 minutes) |
| Out of disk or memory (large downloads) | The service uses a small default build VM (Standard_D1_v2); set a larger `vmSize` in the template's VM profile |

## Re-run and clean up
```bash
az image builder run -g rg-img -n tpl-web2022 --no-wait
az image builder cancel -g rg-img -n tpl-web2022
```
Search the log for `(telemetry)` from the bottom to find the last customizer that ran.

## Verify
- [ ] `lastRunStatus.runState` Succeeded; gallery image version exists and replicates to target regions.

## Checked

Date: 2026-10-28.

Confirmed against Learn (VM Image Builder troubleshooting and template reference): lastRunStatus/runState, customization.log in the `packerlogs` container of the staging resource group, `IT_` staging group name and `stagingResourceGroup` property, buildTimeoutInMinutes default of 4 hours, restartTimeout 15 to 30 minutes, default build VM size Standard_D1_v2, searching for (telemetry). CLI commands via check_commands.py.
Removed: provisioningState meaning, the identity/authorization, script download, sysprep and private networking rows, Standard_D4s_v5/128 GB advice, template immutability and failed-run cost claims.

Method: documentation only; no commands were run.
