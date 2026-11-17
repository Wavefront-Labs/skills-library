---
id: computing-software.cybersecurity-defensive.falco.program-and-http-outputs
name: program-and-http-outputs
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [program-output, http-output, slack-webhook, jq, xargs]
level: practitioner
status: docs-checked
description: "Pipe Falco alerts to a program or HTTP endpoint, with keep_alive, xargs wrapping, a Slack webhook example and the HTTPS limits."
sources:
  - https://falco.org/docs/concepts/outputs/channels/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`program_output` starts a program and writes each alert to its standard input. Only one program output can be configured. The program runs via a shell, so pipelines work.

```yaml
json_output: true
program_output:
  enabled: true
  keep_alive: false
  program: "jq '{text: .output}' | curl -d @- -X POST https://hooks.slack.com/services/XXX"
```

With `keep_alive: false` (default) Falco runs the program once per alert. With `true` it spawns it before the first alert and keeps the pipe open, with output flushed only on close unless `--unbuffered` is set. A persistent network stream: `program: "nc host.example.com 1234"` with `keep_alive: true`.

For programs that do not read stdin, wrap with xargs:
`program: "xargs -I {} aws --region ${region} sns publish --topic-arn ${falco_sns_arn} --message {}"`

HTTP:

```yaml
json_output: true
http_output:
  enabled: true
  url: http://some.url/some/path/
```

Only unencrypted HTTP and HTTPS with valid certificates are supported; invalid or self-signed certificates are not.

Gotcha: the spawned program is in Falco's process group and receives every signal Falco receives. To survive SIGTERM for a clean flush, override the handler yourself.

## Checked

2026-11-08. Read the Output Channels page in full; claims match.

Method: documentation only; no commands were run.
