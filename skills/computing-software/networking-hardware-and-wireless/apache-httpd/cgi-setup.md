---
id: computing-software.networking-hardware-and-wireless.apache-httpd.cgi-setup
name: cgi-setup
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, cgi, scriptalias, execcgi, mod-cgid, suexec, troubleshooting]
level: intro
status: docs-checked
description: "Run CGI programs: choose mod_cgi or mod_cgid, ScriptAlias or Options +ExecCGI with a handler, script output headers, permissions and error-log diagnosis."
sources:
  - https://httpd.apache.org/docs/2.4/howto/cgi.html
  - https://httpd.apache.org/docs/2.4/misc/security_tips.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CGI setup
## Module
`mod_cgid` for threaded MPMs (event, worker); `mod_cgi` for prefork or Windows.

## Enable
```apache
ScriptAlias "/cgi-bin/" "/usr/local/apache2/cgi-bin/"
```
Everything in a ScriptAlias directory is CGI. Elsewhere you need both `ExecCGI` and a handler:
```apache
<Directory "/usr/local/apache2/htdocs/somedir">
    Options +ExecCGI
    AddHandler cgi-script .cgi .py
</Directory>
```

## Program
Output starts with a MIME header, a blank line, then the body:
```python
#!/usr/bin/env python3
print("Content-type: text/html\n")
print("Hello, World.")
```
The server runs unprivileged, so make it executable (`chmod a+x`). Test from the command line first.

## Troubleshooting
| Symptom | Cause |
|---|---|
| source shown | CGI not configured |
| Forbidden | permissions |
| Premature end of script headers | missing headers, bad interpreter, program error |

Check the error log first. PATH may differ, so use full paths. If a suexec binary is installed, any policy violation also gives "Premature end of script headers".

## Security
CGI runs with the server user's permissions. ScriptAliased CGI is safer if only trusted users can write there.

## Checked

2026-11-08. mod_cgid vs mod_cgi, ScriptAlias, ExecCGI with AddHandler, the example program and header rule, chmod, PATH caveat, symptom causes, suexec and Premature end of script headers, and the security notes confirmed against the CGI how-to and security tips pages.

Method: documentation only; no commands were run.
