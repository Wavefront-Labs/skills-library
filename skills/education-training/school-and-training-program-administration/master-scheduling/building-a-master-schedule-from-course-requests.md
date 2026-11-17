---
id: education-training.school-and-training-program-administration.master-scheduling.building-a-master-schedule-from-course-requests
name: building-a-master-schedule-from-course-requests
category: education-training
field: school-and-training-program-administration
product: master-scheduling
tags: [master-scheduling, master-schedule, timetabling, school-timetable, timetable-construction, course-requests, conflict-matrix, singletons, doubletons, section-balancing, teacher-load, room-allocation, bell-schedule, block-schedule, period-schedule, scheduler, powerschool, infinite-campus, timetabler, edval, asc-timetables, conflict-resolution, class-size, staffing]
level: practitioner
status: draft
description: "Build a school master schedule: clean course requests, compute sections, read the conflict matrix, place singletons first, balance sections and teacher loads, then load students and fix conflicts."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building a master schedule from course requests

**Goal:** a timetable that lets the maximum number of students get their requested
courses, within staffing, room and contract limits, finished early enough for staff
and families to plan. The sequence below is common to secondary schools and
multi-track training programmes; tool names (PowerSchool, Infinite Campus, Edval,
aSc, Timetabler, etc.) only change where you click.

## 0. Fix the constraints first (spring, or ~4–6 months before start)
- **Bell schedule / structure:** periods per day, block vs traditional, A/B days,
  lunch waves. Changing this after the build means starting again.
- **Staffing:** FTE per subject, each teacher's certification/qualification to teach
  each course, part-timers' available periods, contractual maximum teaching periods,
  minimum prep/planning periods, max class sizes (by contract, law or room).
- **Rooms:** labs, gyms, specialist rooms and their capacities.
- **Policies:** priorities (e.g. graduation requirements beat electives; seniors first),
  co-requisites, and how many alternates students list.

## 1. Clean the course requests
- Collect requests with 1–2 ranked alternates. Run validation: prerequisites met,
  graduation requirements present, no duplicate requests, full load requested.
- Fix data errors *now*. Bad requests produce phantom conflicts and wrong section counts.

## 2. Compute sections
`sections = ceil(requests ÷ target class size)`, then sanity-check against staffing.
If staffing can't cover the sections, decide now: cap, merge levels, cut a course, or
hire. Courses with tiny demand become decisions, not surprises.

## 3. Read the conflict matrix
The scheduler produces a matrix: for each pair of courses, how many students requested
both. High numbers mean those courses must **not** run in the same period.
- **Singletons** (one section) and **doubletons** are the hard part — a student taking two
  singletons in the same period gets one.
- Place them first, spreading high-conflict singletons across different periods.
  Specialist teachers who teach several singletons constrain this further.

## 4. Build the board
1. Place singletons and doubletons, respecting teacher and room availability.
2. Place multi-section courses, spreading sections across periods so students have
   options (e.g. 6 sections of Grade 10 English across 6 periods, not 3 in period 1).
3. Assign teachers: check load (periods and preps — number of different courses), planning
   periods, and qualifications. Avoid giving one person five preps.
4. Assign rooms: specialist courses first.

## 5. Load students and resolve conflicts
- Run the student loader. Review the results report: % of students fully scheduled,
  % of requests fulfilled, section-size spread.
- Typical targets people aim for are ~95%+ of requests met, but local norms vary — set yours.
- Fix by: moving a section to another period, swapping teachers, opening/closing a
  section, honouring an alternate. Re-run the loader after each round of moves.
- **Balance sections** so no section is at cap while another of the same course has 12.
- Hand-schedule the remaining students individually and record why.

## 6. Freeze, publish, and manage change
- Freeze the board on a date; after that, changes go through a request form with
  criteria (errors, prerequisites failed, level changes), not preference.
- Keep a change log; check class sizes against contractual limits after every batch.

## Gotchas
- Building the master before requests are clean is the number-one cause of rework.
- Specialist/inclusion supports (co-taught classes, resource periods, EAL/ESOL classes)
  must be placed with the singletons, not squeezed in at the end.
- Uncertain: target fulfilment %s and contractual limits are local; confirm.

## Verify
- [ ] Bell schedule, staffing, rooms and policies fixed before building.
- [ ] Requests validated; section counts match staffing.
- [ ] No high-conflict singletons in the same period.
- [ ] Every teacher within load, prep and planning-period limits.
- [ ] Loader report meets your fulfilment target; sections balanced.
