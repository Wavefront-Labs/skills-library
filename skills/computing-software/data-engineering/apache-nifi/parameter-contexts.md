---
id: computing-software.data-engineering.apache-nifi.parameter-contexts
name: parameter-contexts
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, parameter-context, parameters, configuration, process-groups]
level: practitioner
status: docs-checked
description: "Create Parameter Contexts from the Global Menu, name rules, set-empty-string option, reference syntax #{Name}, escaping, group assignment and required policies."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameter contexts

- Create: Global Menu > Parameter Contexts > + button; the Settings tab takes a name and optional description, the Parameters tab adds parameters.
- Parameter names allow only letters, digits, hyphens, underscores, periods and spaces.
- Add Parameter fields: Name, Value, "Set empty string" (unchecked by default; ignored if a value is set), Sensitive Value (default No), Description.
- Reference with `#{Parameter.Name}`; an extra leading `#` escapes it (`##{abc}` yields the literal `#{abc}`). A `/` is not valid in a parameter name.
- A process group can be assigned only one Parameter Context; a context can be assigned to many groups. Unsetting a group's context does not inherit the parent's: components referencing parameters become invalid.
- Policies: seeing contexts needs the "access the controller" or "access parameter contexts" view policy, and modifying needs the matching modify policy; the parameter-context policies are inherited from the controller policies unless overridden. Per-context view/modify policies can also be set.
- To assign a context to a group, a user needs the view policy on that context and the modify policy on the group.
- To modify a parameter, a user needs view and modify policies on every component that references it.
- Assigning, creating, modifying or deleting parameter contexts (and variables) does not count as a local change for flow versioning.

Verify: the processor property resolves and shows the parameter value when the group runs.

## Checked

Confirmed against the NiFi user guide (Parameters, Parameter Contexts, Using a Parameter in a Property, Parameter Context Access Policies, Managing Local Changes).

Method: docs-only read of cited pages, 2026-11-08
