---
id: computing-software.game-programming.godot.threads-and-workerthreadpool
name: threads-and-workerthreadpool
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-performance, workerthreadpool, threads, mutex, thread-safety, call-deferred, game-programming]
level: advanced
status: docs-checked
description: "Run work off the main thread in Godot 4: WorkerThreadPool tasks and group tasks, Thread with Mutex/Semaphore, thread-safe APIs, and returning results with call_deferred."
sources: ["https://docs.godotengine.org/en/stable/tutorials/performance/using_multiple_threads.html", "https://docs.godotengine.org/en/stable/classes/class_workerthreadpool.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threads and WorkerThreadPool

**Goal:** procedural generation, pathfinding batches and file processing without frame hitches.

## WorkerThreadPool (preferred)
```gdscript
var chunk_results: Array = []
func generate_chunks(coords: Array[Vector2i]) -> void:
    chunk_results.resize(coords.size())
    var gid := WorkerThreadPool.add_group_task(
        func(i: int): chunk_results[i] = _generate_chunk_data(coords[i]),   # pure data work only
        coords.size(), -1, true, "chunk gen")
    # later (e.g. polling in _process) or blocking:
    while not WorkerThreadPool.is_group_task_completed(gid):
        await get_tree().process_frame
    WorkerThreadPool.wait_for_group_task_completion(gid)     # must be called once to release the task
    for i in coords.size(): _build_chunk_nodes(coords[i], chunk_results[i])   # main thread: touch the tree
```
- `add_task(callable, high_priority, description)` for single jobs; always `wait_for_task_completion(id)` eventually.
- Group tasks run the callable with indices 0..n-1 across cores: ideal for per-chunk/per-item work.
- Writing to distinct indices of a preallocated array from different tasks is fine; resizing it isn't.

## Thread (long-running workers)
```gdscript
var thread := Thread.new()
var mutex := Mutex.new()
var queue: Array = []
var sem := Semaphore.new()
var quit := false
func _ready() -> void: thread.start(_worker)
func _worker() -> void:
    while true:
        sem.wait()
        mutex.lock(); var job = queue.pop_front() if queue else null; var q := quit; mutex.unlock()
        if q: return
        if job: var r = _process_job(job); _on_done.call_deferred(r)   # back to main thread
func _exit_tree() -> void:
    mutex.lock(); quit = true; mutex.unlock(); sem.post(); thread.wait_to_finish()  # must join
```

## Thread-safety rules
- **Scene tree is not thread-safe**: don't add/remove/modify nodes in the tree from threads. Build nodes
  off-tree in a thread, then `add_child.call_deferred(node)`.
- Servers: check the thread-safety section of the Using multiple threads page per API.
- Resources: loading via `ResourceLoader.load_threaded_request` is the safe path; don't share mutable
  Resources between threads without a Mutex.
- GDScript arrays/dictionaries aren't synchronised; guard shared ones with a Mutex.
- Use `call_deferred` / `Callable.call_deferred` to hand results to the main thread.

## Debugging
Keep thread code small: data in, data out.

## Verify
- [ ] Generating a large world shows no main-thread hitch in the profiler.
- [ ] Quitting during generation exits cleanly (threads joined with `wait_to_finish`).

## Checked
Godot docs (stable) pages and godotengine/godot master doc/classes XML fetched 2026-10-28.
Confirmed: WorkerThreadPool class (`add_task`, `add_group_task`, `is_group_task_completed`, `wait_for_group_task_completion`) and the Using multiple threads page (scene tree not thread-safe, `call_deferred`, Mutex, Semaphore, Thread).
Removed: the threaded-server safety statement, the debugger-break-in-threads remark and the warning text.
Method: documentation only; no commands were run.
