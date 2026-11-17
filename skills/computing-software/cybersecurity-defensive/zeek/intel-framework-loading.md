---
id: computing-software.cybersecurity-defensive.zeek.intel-framework-loading
name: intel-framework-loading
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, intel-framework, intel-read-files, intel-seen, intel-log]
level: practitioner
status: docs-checked
description: "Load threat intelligence into Zeek: the tab-separated feed format, Intel::read_files, frameworks/intel/seen, do_notice, intel.log matches and CPU cost of seen data."
sources: ["https://docs.zeek.org/en/current/frameworks/intel.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# intel framework loading

Three parts: loading data into an in-memory store, reporting seen data, and handling matches.

Feed format: tab-separated, a hyphen means null.

```
#fields	indicator	indicator_type	meta.source	meta.desc	meta.url
1.2.3.4	Intel::ADDR	source1	Sending phishing email	http://source1.com/badhosts/1.2.3.4
a.b.com	Intel::DOMAIN	source2	Name used for data exfiltration	-
```

Types are listed in `Intel::Type`. Load in `local.zeek`:

```
redef Intel::read_files += { "/somewhere/feed1.txt", "/somewhere/feed2.txt" };
@load frameworks/intel/seen
```

In a cluster the files only need to exist on the manager, which distributes the data. Matches go to `intel.log`, with fields such as `seen.indicator`, `seen.indicator_type`, `seen.where`, `matched` and `sources`.

`@load frameworks/intel/do_notice` adds a `do_notice` bool field: when T for an item, a notice of type `Intel::Notice` is raised on a match.

Matching only happens for data reported through `Intel::seen`. The shipped scripts report IPs only from established TCP connections, so UDP and one-sided traffic do not match by default. Reporting more costs CPU; for example, reporting every connection:

```
event new_connection(c: connection)
    {
    Intel::seen([$host=c$id$orig_h, $conn=c, $where=Conn::IN_ORIG]);
    Intel::seen([$host=c$id$resp_h, $conn=c, $where=Conn::IN_RESP]);
    }
```

This can hurt performance noticeably. Loading only selected scripts from the `seen` directory also limits load.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
