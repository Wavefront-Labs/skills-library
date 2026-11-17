---
id: computing-software.collaboration-platform-administration.matrix-synapse.workers-media-repository-and-background-tasks
name: workers-media-repository-and-background-tasks
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, workers, media-repository, enable-media-repo, run-background-tasks-on, user-directory, appservices, notify-appservices]
level: advanced
status: docs-checked
description: "Run the media repository, background tasks, user directory updates and appservice notification on dedicated Synapse workers, with the shared-config switches and restart caveats."
sources:
  - https://element-hq.github.io/synapse/latest/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Media repository worker.** A `synapse.app.media_repository` worker handles `/_matrix/media/`, `/_matrix/client/v1/media/`, `/_matrix/federation/v1/media/` and the media admin APIs (`purge_media_cache`, `room/.*/media`, `user/.*/media`, `media/.*`, `quarantine_media`, `users/.*/media`). Set `enable_media_repo: False` in the shared config so the main process stops running media background jobs; this also means the main process can no longer handle those endpoints. The worker's listener must expose the `media` resource. If you run several media repositories they must be on the same server, and exactly one runs the background jobs:

```yaml
media_instance_running_background_jobs: "media-repository-1"
```

With a reverse proxy, `/_matrix/media/` must be routed for both inbound client and federation requests if they are handled separately.

**Background tasks.** A worker with a unique `worker_name` can run periodic and replication-started tasks (which ones depends on config, for example whether stats is enabled). It handles no REST endpoints. Select it in the shared configuration:

```yaml
run_background_tasks_on: background_worker
```

**User directory.** Designate one generic worker with `update_user_directory_from_worker: worker_name`. This cannot be load-balanced, and the main process must be restarted after setting it. The `user_directory/search` endpoint can then go to any worker. It supersedes the deprecated `synapse.app.user_dir`, which used `update_user_directory: false`; with that legacy setup and no running worker, search results may be outdated.

**Application services.** `notify_appservices_from_worker: worker_name` picks one generic worker to send output traffic to appservices. It handles no REST endpoints, cannot be load-balanced, and needs a main process restart. It supersedes `synapse.app.appservice` (deprecated as of Synapse v1.59), which used `notify_appservices: False`.

## Checked

Method: docs-checked 2026-11-09 against docs/workers.md (Synapse develop branch, raw markdown, read in full).
