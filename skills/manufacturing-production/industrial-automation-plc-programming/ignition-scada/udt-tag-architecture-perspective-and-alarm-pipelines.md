---
id: manufacturing-production.industrial-automation-plc-programming.ignition-scada.udt-tag-architecture-perspective-and-alarm-pipelines
name: udt-tag-architecture-perspective-and-alarm-pipelines
category: manufacturing-production
field: industrial-automation-plc-programming
product: ignition-scada
tags: [ignition-scada, ignition, inductive-automation, scada, hmi, udt, tag-provider, tag-groups, scan-class, opc-ua, mqtt, sparkplug-b, mqtt-engine, perspective, vision, view-parameters, indirect-binding, alarm-pipeline, alarm-notification, tag-historian, historian, deadband, gateway, gateway-network, redundancy, project-inheritance, jython, scripting, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Design an Ignition project that scales: UDT-based tag model, OPC-UA vs MQTT sources, parameterised Perspective views, alarm pipelines that page the right people, and historian settings."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UDT tag architecture, Perspective and alarm pipelines in Ignition

**Goal:** an Inductive Automation Ignition (8.1-era) system where adding the 40th
machine is a copy-and-parameter job, screens are generated from the tag model, and
alarms reach a human who can act.

*Draft: from Ignition 8.1 practice. Ignition 8.3 reorganises the gateway web UI and
config storage; verify menu paths on your version.*

## 1. Tag model first, screens second
- Build a **UDT definition** per device type (Motor, Valve, Filler) with **parameters**
  (`{PLC}`, `{BaseAddr}`, `{Area}`), member tags using them in their OPC item path,
  e.g. `ns=1;s=[{PLC}]{BaseAddr}.Running`.
- Instances live in a folder path that mirrors the plant (ISA-95 style):
  `Site/Area/Line/Machine`. Screens and alarm routing will key off this path.
- Put alarm configuration, history settings and engineering units **on the UDT**,
  not on instances; override per instance only when necessary (overrides show bold).
- Use **tag groups** (scan classes in 7.x) deliberately: `Fast` 250 ms for live
  screens, `Default` 1 s, `Slow` 10 s for config. A leased/driven group polls fast only
  while a screen needs it — big PLC load savings.

## 2. Data sources
- **OPC-UA device connections** (built-in Logix, Siemens S7, Modbus drivers) poll the
  PLC. Many tags at fast rates can overload older PLC comm buffers — watch the device's
  diagnostics (request count, overload %).
- **MQTT / Sparkplug B** (Cirrus Link modules): edge nodes publish on change, the
  central gateway subscribes. Report-by-exception scales better across sites; tags
  appear automatically from birth certificates. Requires the third-party modules
  (licensed separately).

## 3. Perspective views from parameters
- Create one view per device type with a **view parameter** (e.g. `tagPath`). Bind
  components with **indirect tag bindings** (`{view.params.tagPath}/Running`).
- Use embedded views / flex repeaters to generate a line overview from a list of tag
  paths (a script or a tag browse returns the list) — no hand-placed objects.
- Keep scripts in the **project library** (gateway-scoped functions), not in component
  events, so they're testable and reused.
- **Project inheritance:** a parent "global" project holds shared views/scripts; site
  projects inherit. Changing the parent changes every child — treat as a release.

## 4. Alarm pipelines
1. Alarm config on the UDT: priority, setpoint, **deadband**, **on-delay** (stops
   chattering), **associated data** (area, shift group) and a **notification pipeline**.
2. Pipeline: *Notification* block → *Delay* (e.g. 5 min) → *Expression* "still active
   and unacknowledged?" → escalate to the next roster.
3. **On-call rosters** and schedules decide who gets SMS/voice/email; the voice/SMS
   modules are separate licences.
4. Test with a simulated alarm and confirm acknowledgement from the phone closes the loop.

Alarm content follows hmi-design guidance — an alarm with no operator action is
not an alarm. See `manufacturing-production.industrial-automation-plc-programming.hmi-design.alarm-rationalisation-and-high-performance-screens`.

## 5. Historian
- Enable history on the UDT member, choose **Deadband style**: Analog (with a sensible
  deadband in engineering units) for process values, Discrete for states.
- **Max time between samples** guarantees a periodic point so a flat line isn't a gap.
- Size the database: tags × samples/day × ~row bytes; set partitioning and pruning.

## Gotchas
- Gateway backups (`.gwbk`) hold everything including credentials — store securely;
  restore on a fresh install of the **same or newer** version.
- Quality codes matter: a tag reading `Bad_NotConnected` must show as such on screens
  (overlay), not as the last good value.
- Gateway scripts run on the server; client/session scripts run per session — a
  timer script in the wrong scope runs N times.

## Verify
- [ ] Adding a new machine = one UDT instance + parameters; screen and alarms appear.
- [ ] No device connection shows sustained overload.
- [ ] A test alarm escalates and an acknowledgement stops escalation.
- [ ] Historical trend of a slow-changing value shows regular points, no false gaps.
- [ ] A recent `.gwbk` backup exists off the gateway server.
