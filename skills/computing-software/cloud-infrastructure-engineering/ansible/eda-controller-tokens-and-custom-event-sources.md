---
id: computing-software.cloud-infrastructure-engineering.ansible.eda-controller-tokens-and-custom-event-sources
name: eda-controller-tokens-and-custom-event-sources
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, event-driven-ansible, eda-controller-token, custom-event-source, rulebooks]
level: advanced
status: docs-checked
description: "Give ansible-rulebook controller access for run_job_template and write a custom event source plugin as an asyncio main function shipped in a collection."
sources: ["https://docs.ansible.com/projects/rulebook/en/latest/sources.html", "https://github.com/ansible/ansible-rulebook/blob/main/docs/actions.rst", "https://github.com/ansible/ansible-rulebook/blob/main/docs/usage.rst", "https://github.com/ansible/event-driven-ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EDA: controller tokens and custom event sources

## Controller access for run_job_template
Rulebook actions `run_job_template` / `run_workflow_template` call automation controller.
- ansible-rulebook needs `--controller-url` and either `--controller-token` or `--controller-username` with `--controller-password` to use these actions. `--controller-ssl-verify` controls certificate checking.
- The URL is the API endpoint; if you give only a host and port, `api` is appended for backward compatibility.
- For an EDA controller activation, how the controller connection is configured (credentials or tokens) differs between AAP releases: follow the Red Hat documentation for your version.
- Use a dedicated service user with only the permissions the triggered templates need (least privilege).
- Local example: `ansible-rulebook -r rulebook.yml -i inventory.yml --controller-url https://aap.example.com --controller-token "$TOKEN"`.

## Custom event source plugin
```python
# extensions/eda/plugins/event_source/queue_depth.py  (collection acme.eda)
"""Poll a queue depth API and emit events."""
import asyncio
import aiohttp

async def main(queue: asyncio.Queue, args: dict):
    url = args["url"]
    interval = int(args.get("interval", 30))
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url, timeout=10) as resp:
                data = await resp.json()
            await queue.put({"queue": data["name"], "depth": data["depth"]})
            await asyncio.sleep(interval)

if __name__ == "__main__":
    class MockQueue:
        async def put(self, event):
            print(event)
    asyncio.run(main(MockQueue(), {"url": "http://localhost:8080/depth", "interval": 5}))
```
Rulebook:
```yaml
sources: []
  - acme.eda.queue_depth:
      url: https://mq.corp/api/depth
      interval: 15
rules:
  - name: Scale workers
    condition: event.depth > 1000
    action:
      run_job_template: {name: Scale workers, organization: Platform}
```
- Contract: `async def main(queue: asyncio.Queue, args: dict)`; the `args` are the options from the rulebook; put event dicts on the queue with `await queue.put(...)`. Keep it asynchronous so it does not block the loop.
- Plugins ship in a collection under `extensions/eda/plugins/event_source/` (the layout of ansible.eda).
- Reliable delivery: for message buses, the docs describe an optional feedback mechanism (`feedback: true`, `eda_feedback_queue` in `args`, `feedback_timeout` default 120 s) that needs persistence enabled and a unique `meta.uuid` on every event; it gives at-least-once delivery.
- The docs rank plugin patterns: event-bus plugins (recommended), callback/webhook plugins (risk of lost events, exposed endpoint; they recommend AAP Event Streams instead) and scraper plugins (polling, like this example, may miss or duplicate data).

## Gotchas
- Catch transient polling errors inside the loop and retry with backoff, so one failed request does not end the source.
- Event filters (`filters:`) can reshape your events instead of adding logic to the source.

## Verify
```bash
ansible-rulebook -r rulebook.yml -i inventory.yml --print-events -S extensions/eda/plugins/event_source
```
(`-S` is `--source-dir`, a local directory of source plugins.)

## Checked
2026-10-28. Confirmed in the ansible-rulebook docs (sources, actions, usage) and the ansible.eda repository layout: the `main(queue, args)` contract, plugin patterns and their trade-offs, feedback options, `-S`, `--print-events`, controller CLI options and the `api` suffix behaviour. Removed because not confirmed: the AAP 2.4 and 2.5 credential and token screens, the `EDA_CONTROLLER_URL`/`EDA_CONTROLLER_TOKEN` variables, the claim that an exception stops the activation and the `requirements.txt` inclusion claim. The Red Hat EDA controller pages returned no readable text.
Method: documentation only; no commands were run.
