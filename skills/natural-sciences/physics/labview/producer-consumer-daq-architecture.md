---
id: natural-sciences.physics.labview.producer-consumer-daq-architecture
name: producer-consumer-daq-architecture
category: natural-sciences
field: physics
product: labview
tags: [labview, physics, producer-consumer, queues, daqmx, data-acquisition, tdms, qmh, queued-message-handler, event-structure, error-handling, clean-shutdown, buffer-overflow, design-pattern, dqmh, actor-framework, instrument-control]
level: practitioner
status: docs-checked
description: "Structure a LabVIEW measurement app as producer/consumer loops: queues, a separate logging loop, error handling and clean shutdown without data loss."
sources: [https://www.ni.com/en/support/documentation/supplemental/21/producer-consumer-architecture-in-labview0.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Producer/consumer DAQ architecture in LabVIEW

**Goal:** a continuous acquisition that never drops samples, logs everything,
stays responsive to the UI, and shuts down cleanly, instead of one giant while
loop that acquires, plots and writes to disk in series.

## 1. The pattern
Two (or more) parallel while loops on the block diagram, joined by a queue:
- **Producer (acquisition) loop:** only reads from hardware and enqueues data.
  Nothing slow in here: no file I/O, no heavy plotting, no dialogs.
- **Consumer (processing/logging) loop:** dequeues and does the slow work: file
  write, analysis, chart updates. It works at its own pace, so a fast producer is
  not slowed by slow processing.
- Queues are first-in/first-out, so the consumer handles items in the order the
  producer sent them, and they can be created outside both loops.
- A queue is bound to one data type: wrap different data items in a cluster.
- The pattern is not based on synchronisation, so starting one loop before the
  other can cause problems. NI suggests adding an event structure to solve this.
- The **queued message handler (QMH)** is a specialised version of the same
  architecture; use it for a UI that sends commands (start, stop, change settings).
  LabVIEW 2016 and later also offer channel wires as an alternative to queues.

## 2. Building it
1. Outside the loops: create the queue, create and configure the acquisition task
   (sample rate, continuous mode), start it.
2. Producer: read a fixed number of samples per iteration, then enqueue. Pick the
   read size and buffer from the NI-DAQmx help for your hardware.
3. Consumer: dequeue, write to the log file (open it once, outside the loop) and
   update a graph, decimating before plotting.
4. Wire the **error cluster** through every node; a producer error should
   stop the producer and tell the consumer to finish.
5. For logging only, check whether your DAQ driver can stream to disk itself
   (see the NI-DAQmx help).

## 3. Clean shutdown (the part everyone gets wrong)
- Stop the producer first (stop button via a notifier or a UI message).
- After the producer exits, stop and clear the acquisition task, then send an explicit
  **stop message** (a sentinel) on the queue.
- Consumer drains until it sees the stop message, closes the file, then exits.
- Only then release the queue reference (Release Queue closes the queue reference). Avoid using the release itself as
  the stop signal: anything still queued is lost.
- Merge errors and report once at the end.

## 4. Sizing and monitoring
- Watch the queue's element count. Growing steadily means the
  consumer is too slow: write bigger chunks, plot less often, or move analysis offline.
- A bounded queue protects memory but makes the producer block when full, which can
  then overflow the DAQ buffer.
- If the driver reports that you attempted to read samples that are no longer available,
  the producer fell behind the hardware buffer: look up the error in NI's documentation
  for your version.

## Gotchas
- Front-panel charts with full-rate data are the commonest bottleneck.
- Local variables used for data passing create race conditions; use queues for data,
  notifiers or user events for "latest value only".
- Take time stamps from the acquisition (waveform t0 and dt), not the PC clock per loop.
- A slow instrument query in the producer stalls acquisition; give slow instruments their
  own loop.

## Verify
- [ ] Producer contains only acquisition and enqueue.
- [ ] Queue length stays bounded over a long test run.
- [ ] Sample count in the log file equals rate times run time (no gaps in timestamps).
- [ ] Pressing stop leaves no data in the queue and closes the file properly.
- [ ] Errors from either loop stop both loops and are reported once.

## Checked
2026-11-01. Confirmed in NI's "Producer/Consumer Architecture in LabVIEW": producer and
consumer roles, FIFO queues created outside the loops, one data type per queue (wrap in a
cluster), lack of synchronisation and the event-structure fix, QMH as a specialised
version, channel wires from LabVIEW 2016, Release Queue closes the reference. Removed: the Get Queue Status name,
DAQmx VI names and the 1/10-rate read size, timeout figures, TDMS specifics, error -200279
and error 1 statements, instrument latency figures, DQMH and Actor Framework claims, and
the course-material and DAQmx help sources (not read). The shutdown order is design advice,
not a sourced fact.
Method: documentation only; no commands were run.
