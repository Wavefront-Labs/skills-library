---
id: computing-software.systems-network-administration.icinga-2.templates-and-multiple-inheritance
name: templates-and-multiple-inheritance
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, templates, import, inheritance, generic-host, generic-service, vars]
level: practitioner
status: docs-checked
description: Use Icinga 2 template objects and import - shared attributes, multiple templates with ordering, vars += merging, overriding on the object, and the shared name space rule.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# templates and multiple inheritance
Templates apply a set of identical attributes to many objects:
```
template Service "generic-service" {
  max_check_attempts = 3
  check_interval = 5m
}
apply Service "ping4" {
  import "generic-service"
  check_command = "ping4"
  assign where host.address
}
```
Objects and templates can import any number of other templates, and attributes can be overridden in the object. You can also import existing non-template objects.

Templates and objects share one name space, so a template cannot have the same name as an object.

**Multiple templates.** Order matters: imports are applied in sequence. Use `+=` on `vars` to add dictionary items without overriding the earlier `vars`:
```
template Host "wp-server" {
  vars += { application_type = "wordpress" }
}
object Host "wp1.example.com" {
  import "web-server"
  import "wp-server"
  vars.webserver_type = "nginx" //overrides attribute from base template
  address = "192.168.56.201"
}
```
Here `web-server` is the base template (it imports `generic-host`, which supplies `check_command`), then `wp-server` adds attributes, and the object overrides `webserver_type`.

## Checked

2026-11-04. Confirmed against the Icinga 2 monitoring basics chapter: template import order, += on vars, shared name space for templates and objects.

Method: documentation only; no commands were run.
