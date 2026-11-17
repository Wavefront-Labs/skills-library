---
id: computing-software.software-engineering.code-review.review-comment-tone-and-courtesy
name: review-comment-tone-and-courtesy
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, review-tone, courtesy, explaining-why, conventional-comments, psychological-safety]
level: practitioner
status: docs-checked
description: "Write review comments that are courteous, about the code not the person, explain why, label severity, and avoid the patterns that make reviews feel hostile."
sources: ["https://google.github.io/eng-practices/review/reviewer/comments.html", "https://conventionalcomments.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Courtesy and explaining why in comments

## Google's rules
- **Be kind.** Comment on the code, never the developer.
  - Bad: "Why did you use threads here when there's obviously no benefit?"
  - Good: "The concurrency model here adds complexity without a performance benefit I can see.
    Since there's no gain, it's best for this code to be single-threaded rather than use threads."
- **Explain your reasoning**: the why helps the author learn and lets them push back with facts.
- **Balance direction and guidance**: point out problems and let the author decide the fix, unless
  a direct suggestion is clearly more helpful.
- **Encourage simpler code or comments** rather than explanations in the review tool: future
  readers won't see the review thread.

## Label severity (Conventional Comments style)
```
nitpick (non-blocking): prefer `enumerate` over manual index here
suggestion: extract the retry loop into a helper so the worker and the API share it.
issue (blocking): this query runs inside the loop: N+1 against the orders table.
question: does `cancel()` need to release the reservation too?
praise: nice use of the table-driven test here.
```
Labels like `Nit:`, `Optional:`, `FYI:` (Google) tell the author what must change before approval.

## Other points from the Google page
- Direct a comment at the code, never the developer; this matters most when the point might
  be upsetting or contentious.
- It is the developer's job to fix the change, not yours: you need not design the solution
  or write the code, but balance pointing out problems with giving direct guidance when that
  helps more. The goal is the best change, and secondarily improving developer skills.
- If you ask for an explanation of code you do not understand, the usual outcome should be
  clearer code; explanations that live only in the review tool do not help future readers.
- Where you like something in the change, comment on it too, and say why.

## Self-check before posting
Does each comment say what to change, why, and whether it is required?

## Checked

2026-11-08. Read in full: Google eng-practices "How to write code review comments" and the Conventional Comments home page. Confirmed: the courtesy example, explaining why, balancing direction and guidance, the Nit, Optional or Consider, and FYI labels, accepting explanations, and the `praise`, `question`, `suggestion` labels with `(blocking)` and `(non-blocking)` decorations. Removed: the phrasing habits (we/you wording, banned words, one comment per issue) and the mtlynch.io source, none of which were confirmed, and the label examples are illustrative usage only.

Method: documentation only; no commands were run.
