---
name: planning
description: Plan requirements, business workflows, features, or implementation increments using project evidence and observable acceptance criteria. Use for requested plans or nontrivial design work; a plan-only request does not authorize product implementation.
---

# Planning

Follow [AGENTS.md](../../../AGENTS.md). Scale the plan to the decision; a small understood change needs only a brief approach.

## Establish the business outcome

Locate the project's authoritative requirements, relevant design documents, and affected implementation if present. Identify the user or consumer, their problem, requested outcome, and existing requirement IDs when available. Distinguish observed behavior, approved decisions, draft proposals, assumptions, and unresolved questions. Missing documentation is a knowledge gap, not permission to invent it.

Describe the business or user workflow before domain-specific rules and technical design. Make actors, inputs, state changes, permissions or approval points, failure recovery, and non-goals explicit where they affect the task. Derive those rules from the project rather than assuming every application uses an approval workflow.

## Choose a bounded implementation

Trace the affected UI, application, persistence, and provider boundaries that actually exist. Consider a simpler option before adding a new layer. Explain alternatives only when they materially change effort, behavior, compatibility, or cost.

Break work into runnable increments tied to acceptance scenarios. For each, name the likely files or components, observable result, verification, and dependencies. Mark new paths as proposed rather than claiming they already exist. Include migration and recovery when stored data or contracts change.

When AI or external services are involved, plan deterministic contract checks separately from live quality or integration evaluation. Identify required inputs, external failure modes, cost where relevant, and how affected user data survives failures.

## Deliver a usable plan

Include the following only to the depth the task needs:

- Outcome, business reason, scope, and non-goals.
- Sources and decisions, with material assumptions or blocking questions.
- User flow and acceptance scenarios, including relevant failure cases.
- Ordered increments: change -> observable result -> verification.
- Risks, dependencies, and unresolved validation.

Return the plan in chat unless a durable artifact is requested or needed for the authorized handoff. Use the specified destination or the project's existing documentation convention; if neither exists, `docs/` is a reasonable default. Link authoritative sources, label new proposals as draft, and preserve existing formats.

Update an existing knowledge artifact before creating a duplicate. Preserve confirmed decisions and their rationale; record an authorized replacement and link the superseded decision when useful. Mark completed work only from verified results, and approval only from actual user authority.

Proceed with implementation when it is already requested. If the user asks for a plan to approve, deliver the plan and wait before implementing. Use [testing](../testing/SKILL.md) when selecting behavioral checks.
