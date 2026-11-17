---
id: computing-software.systems-network-administration.windows-server.event-triggered-scheduled-tasks
name: event-triggered-scheduled-tasks
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, event-logs, event-viewer, event-triggered-task, attach-task-to-event, task-scheduler, eventtrigger, valuequeries]
level: practitioner
status: docs-checked
description: "Attach tasks to events: Event Viewer Attach Task, schtasks /sc onevent with XPath, passing EventData to scripts with ValueQueries, and avoiding storm loops."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/taskschd/eventtrigger
  - https://learn.microsoft.com/en-us/windows/win32/taskschd/eventtrigger-valuequeries
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4698
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attach tasks to events

## Create with schtasks
`schtasks /create` has `/sc onevent` and `/ec <channel>` options, but the documented parameters give no way to pass the
event criteria, so define the event trigger in task XML and import it:
```
schtasks /create /tn "Alert-TaskCreated" /xml task.xml /ru SYSTEM
```
(`/xml` can be combined with `/ru` and `/rp`.)

## Pass event data to the script
An event trigger holds a `Subscription` (an XPath query in a QueryList) and optional `ValueQueries`: up to 32 named
XPath queries applied to the last matching event. The names become `$(name)` variables in action properties such as
`ExecAction.Arguments`. Task XML or the COM/script API only; not schtasks flags. Example using event 4698 (task created),
whose event data has `SubjectUserName` and `TaskName` fields:
```xml
<EventTrigger>
  <Enabled>true</Enabled>
  <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="Security"&gt;&lt;Select Path="Security"&gt;*[System[EventID=4698]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
  <ValueQueries>
    <Value name="User">Event/EventData/Data[@Name='SubjectUserName']</Value>
    <Value name="Task">Event/EventData/Data[@Name='TaskName']</Value>
  </ValueQueries>
</EventTrigger>
...
<Exec><Command>powershell.exe</Command>
  <Arguments>-NoProfile -File "<SCRIPTS_DIR>\alert.ps1" -User "$(User)" -Task "$(Task)"</Arguments></Exec>
```
The XPath for each value depends on the event's XML. At most 500 tasks with event subscriptions can exist.
Alternative: have the script read the newest matching event itself with `Get-WinEvent`.

## Avoid storms
- Set MultipleInstances (IgnoreNew or Queue) so bursts of events do not start overlapping runs.
- Do not write to the same log with the same event ID from the action (self-trigger loop).
- For fleet-wide alerting use event forwarding or a SIEM; event tasks suit local automation.
## Verify
- [ ] Generate the event; task history shows the run and the script logged the passed values.

## Checked

2026-10-26 against the Task Scheduler docs (win32 EventTrigger, EventTrigger.ValueQueries, schema Value element and schtasks create; last commit 2026-10-08) and the event 4698 reference: Subscription XPath query, ValueQueries semantics and `$(name)` substitution in ExecAction arguments, the 32-value and 500-subscription limits, schtasks /sc onevent, /ec and /xml, and the 4698 field names. Removed the Event Viewer attach-task walkthrough, the schtasks /mo XPath example (not documented), the 4740 and 7034 examples and the eventcreate suggestion as unconfirmed.

Method: documentation only; no commands were run.
