---
name: systematic-debugging
description: Investigate bugs, failing tests, build or integration failures, and unexpected behavior using reproduction and evidence before fixes. Also use for diagnosis-only requests; apply a fix only when implementation is authorized.
---

# Systematic debugging

Follow [AGENTS.md](../../../AGENTS.md). Establish what is failing and why before selecting a fix; keep the investigation proportionate to the issue.

## Locate the failure

Record expected versus observed behavior, the input or action sequence, environment, and exact error. Reproduce with the smallest safe case; when intermittent, collect evidence that separates plausible causes. Check recent relevant changes and compare a working path.

Trace the failing value or state through the components that actually participate in the failure. Depending on the system, these may include input handling, application state, storage, process boundaries, external calls, or output validation. Use sanitized diagnostic data and avoid exposing secrets or private user content.

If reproduction is unavailable, identify the strongest evidence and remaining uncertainty. Report a hypothesis as a hypothesis, with the next check that would confirm it.

## Test a cause

State a specific hypothesis, the evidence supporting it, and an observation that would falsify it. Run one focused experiment at a time. Prefer read-only checks; temporary instrumentation must stay within the authorized diagnostic scope.

Isolate external dependencies with controlled inputs or test doubles where useful, then check the real boundary if the hypothesis depends on it. For state or data-loss failures, inspect ordering, transactions, concurrency, and recovery. For AI failures, distinguish application or input defects from variable model output before changing prompts.

When an experiment fails, revise the hypothesis instead of stacking speculative patches. Repeated failure or conflicting evidence calls for re-examining the boundary or architecture assumption.

## Fix and verify when authorized

Capture a regression case that demonstrates the failure, following [testing](../testing/SKILL.md). Fix the confirmed cause with the smallest coherent change. Keep unrelated cleanup separate and remove temporary diagnostics introduced by the investigation.

Rerun the reproducer and the relevant dependent checks. For persistence or retry bugs, verify the resulting records and side effects, not just the returned status.

Report the failure, supported cause, fix if applied, checks, and remaining uncertainty. A diagnosis-only request ends with the diagnosis and proposed remedy.

Workflow inspiration: [Superpowers systematic debugging](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md).
