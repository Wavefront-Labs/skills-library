---
id: computing-software.systems-network-administration.apache-tomcat.rewrite-valve-url-rewriting
name: rewrite-valve-url-rewriting
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, rewrite, rewritevalve, rewrite-config, rewritecond, rewriterule, rewritemap, url-rewriting, redirect]
level: practitioner
status: docs-checked
description: "Use Tomcat 10.1 RewriteValve (mod_rewrite style): rewrite.config at Host or Context level, RewriteCond/RewriteRule/RewriteMap, flags, variables, ReDoS caution."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/rewrite.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RewriteValve

```xml
<Valve className="org.apache.catalina.valves.rewrite.RewriteValve"/>
```
- In a Host: put `rewrite.config` in the Host configuration folder.
- In a Context's `context.xml`: Tomcat reads `WEB-INF/rewrite.config` of that app.

Directives: `RewriteCond TestString CondPattern [flags]` (ANDed unless `[OR]`), `RewriteRule Pattern Substitution [flags]` (in order), `RewriteMap name class [params]` (custom class in a jar under `$CATALINA_BASE/lib`, or built-ins `int:toupper`, `int:tolower`, `int:escape`, `int:unescape`). `#` starts a comment.

Rule flags: `L` stop; `R[=code]` external redirect (default 302; symbolic names temp, permanent, seeother); `NC` ignore case; `QSA` append query; `F` 403; `G` 410; `N` restart; `C` chain; `S=n` skip n rules; `NE` no escape; `E=VAR:VAL`; `CO=...` cookie; `H=Host`; `T=mime`; `VS` skip next valve. Cond flags: `NC`, `OR`. The `P` proxy flag is not documented.

Variables include `%{HTTP_HOST}`, `%{REQUEST_URI}`, `%{QUERY_STRING}`, `%{HTTPS}`, `%{REMOTE_ADDR}`, `%{HTTP:header}`, `%{ENV:name}`, `%{SSL:name}`. Backreferences: `$N` (rule), `%N` (cond), `${map:key|default}`.

Examples:
```
RewriteRule ^/old-page$ /new-page [R=permanent,L]
RewriteCond %{HTTPS} =off
RewriteRule ^/(.*)$ https://%{HTTP_HOST}/$1 [R=permanent,L]
```

Caveats: patterns are Perl-compatible regex (poorly written ones allow ReDoS); a `!`-negated pattern cannot use `$N` in the substitution; absolute URLs in the substitution need the `R` flag.

Verify: `curl -I http://localhost:8080/old-page` returns a redirect with a `Location` header.

## Checked

2026-11-04. Read the Tomcat 10.1 Rewrite Valve page (rewrite.html): confirmed class name, Host versus Context rewrite.config placement, RewriteCond/RewriteRule/RewriteMap syntax, the int: maps, rule and condition flags (including VS and the R symbolic names), server variables, ENV, SSL and HTTP lookups, backreferences, the ReDoS warning, the negated-pattern limit and the absolute-URL note. Removed the conf/Catalina/localhost location, the no-RewriteBase remark and the numeric 301 for permanent, which the page does not state.

Method: documentation only; no commands were run.
