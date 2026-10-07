---
name: code-review
description: Review diffs, pull requests, commits, or scoped existing code for actionable correctness, compatibility, data, and trust-boundary defects. Use for review or audit requests; review alone does not authorize fixes.
---

# Code review

Follow [AGENTS.md](../../../AGENTS.md). Prioritize supported failures and user impact over stylistic preferences.

## Establish scope and intent

Identify the requested diff, base, commit range, or audit scope. Inspect status, changed and new files, relevant callers, contracts, and tests. Read the applicable product requirements and document status before judging intended behavior. Separate introduced defects from pre-existing issues.

## Trace the changed behavior

Derive the affected invariants from project requirements and trace the relevant paths:

- Inputs, outputs, and state transitions satisfy their contracts, including relevant empty, invalid, or boundary cases.
- Permissions are enforced where actions execute; stale state, retries, or concurrency cannot create unauthorized or duplicate effects.
- Storage and schema changes preserve required data, history, consistency, and compatibility; failure recovery follows the intended contract.
- External failures, partial completion, and cancellation produce accurate outcomes and release affected resources.
- Untrusted content is validated and rendered safely. For AI features, check output contracts, supported factual claims, and separation of data from executable instructions.
- User-facing success and error states reflect actual outcomes and support the recovery required by the product.

Also inspect compatibility, cleanup, privacy, and resource use on the touched paths. Flag complexity or scope creep only when it has a concrete maintenance cost, conflicts with requirements, or hides a supported failure.

Use focused safe diagnostics to test uncertain findings. Label unconfirmed concerns and state what evidence is missing; do not manufacture a defect to fill a review.

## Return actionable findings

Present findings first, ordered by impact. Each finding needs a concise title and priority, the smallest useful file/line location, triggering input or sequence, concrete consequence, and a focused remedy or regression check.

Use P0 for immediate widespread critical failure, P1 for high-impact failure, P2 for a meaningful bounded defect, and P3 for a low-impact defect. Explain the affected conditions; severity follows demonstrated impact, not the importance of the component.

Group symptoms sharing a cause. End with checks performed and material coverage gaps. If no actionable defect is found, say so; a clean review does not prove full-system correctness or the quality of untested external behavior.

If fixes are also requested, use [systematic-debugging](../systematic-debugging/SKILL.md) for unresolved causes and [testing](../testing/SKILL.md) for regression coverage.
