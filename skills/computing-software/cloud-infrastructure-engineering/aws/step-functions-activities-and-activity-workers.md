---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-activities-and-activity-workers
name: step-functions-activities-and-activity-workers
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, activity-worker, activities, getactivitytask, task-token, heartbeat]
level: practitioner
status: docs-checked
description: "Run Step Functions activity tasks with your own workers: CreateActivity, GetActivityTask long polling, heartbeats and timeouts, and when callbacks are the better choice."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html", "https://docs.aws.amazon.com/step-functions/latest/dg/procedure-cw-metrics.html", "https://docs.aws.amazon.com/step-functions/latest/dg/service-quotas.html", "https://docs.aws.amazon.com/step-functions/latest/apireference/API_GetActivityTask.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step Functions activities and activity workers

**Goal:** have a state machine hand work to code you run anywhere (EC2, on-premises, a
container) that pulls tasks, and get results and heartbeats back.

## Create and use
```bash
aws stepfunctions create-activity --name resize-video
# -> arn:aws:states:eu-west-1:111122223333:activity:resize-video
```
```json
"Resize": {"Type":"Task",
  "Resource":"arn:aws:states:eu-west-1:111122223333:activity:resize-video",
  "TimeoutSeconds":3600, "HeartbeatSeconds":120, "Next":"Done"}
```
Standard workflows only; Express workflows do not support activities.

## Worker loop
```python
sfn = boto3.client("stepfunctions", config=Config(read_timeout=70))
while True:
    t = sfn.get_activity_task(activityArn=ARN, workerName=socket.gethostname())
    if not t.get("taskToken"):      # long poll returned no task
        continue
    try:
        result = work(json.loads(t["input"]), heartbeat=lambda: sfn.send_task_heartbeat(taskToken=t["taskToken"]))
        sfn.send_task_success(taskToken=t["taskToken"], output=json.dumps(result))
    except Exception as e:
        sfn.send_task_failure(taskToken=t["taskToken"], error=type(e).__name__, cause=str(e)[:32000])
```
- `GetActivityTask` is a long poll: keep the client read timeout longer than the poll (see "Avoiding latency when polling for activity tasks" in the Step Functions best practices).
- Send heartbeats more often than `HeartbeatSeconds`; a missed heartbeat fails the task with `States.HeartbeatTimeout` (also matched by `States.Timeout`).
- Without `TimeoutSeconds` a task can wait up to the execution limit (one year) for a worker.
- After a task times out, its task token is invalidated and calls with it fail with `TaskTimedOut`; the worker should handle that and go back to polling.
- Worker IAM: allow the `GetActivityTask`, `SendTaskSuccess`, `SendTaskFailure` and `SendTaskHeartbeat` actions for the worker's identity.

## Scaling
- Metrics (namespace `AWS/States`, dimension `ActivityArn`): `ActivitiesScheduled`, `ActivitiesStarted`, `ActivityScheduleTime` (ms in the scheduled state, waiting for a
  worker). Scale workers on schedule time, like queue age. Activity tasks can also wait up to a year when `TimeoutSeconds` and heartbeats are set.
- Many pollers per activity are fine; each task goes to one worker.

## Prefer callbacks for new designs
`arn:aws:states:::sqs:sendMessage.waitForTaskToken` puts the task in SQS with the token; workers use
normal SQS tooling, DLQs and autoscaling. Activities remain useful when workers cannot reach SQS but can reach the Step Functions endpoint.

## Gotchas
- Polls left open when a worker stops can grab a task and then die; keep `HeartbeatSeconds` short so it is rescheduled via Retry.
- `GetActivityTask` is rate limited (a token bucket per account and Region, see the service quotas page); do not run hundreds of idle pollers.
- Add `Retry` on `States.Timeout` and `States.TaskFailed` in the state.

## Verify
- [ ] Execution reaches the activity state and the history shows the activity scheduled and then started.
- [ ] Killing the worker mid-task fails the task after `HeartbeatSeconds` and Retry reschedules it.
- [ ] `ActivityScheduleTime` alarm exists for backlog.

## Checked
Checked 2026-10-24 against the Step Functions developer guide (activities, service quotas, CloudWatch metrics, workflow type comparison, error handling).
Confirmed: activities are Standard-only, GetActivityTask/SendTaskSuccess/SendTaskFailure/SendTaskHeartbeat flow, timeouts and heartbeats up to one year, token invalidation and TaskTimedOut after timeout, activity metric names and ActivityArn dimension, GetActivityTask throttling quota exists, sqs:sendMessage.waitForTaskToken integration.
Removed as unconfirmed: the 60 s poll duration and 65 s client timeout figures, exact worker IAM resource scoping, history event names.

Method: documentation only; no commands were run.
