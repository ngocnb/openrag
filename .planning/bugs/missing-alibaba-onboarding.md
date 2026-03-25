# Bug: Missing Alibaba Provider in Onboarding Card

## Summary

The Alibaba provider option is missing from the onboarding card page. Users cannot select Alibaba as their LLM or embedding provider during the onboarding flow.

## Evidence

- **Spec**: `.planning/specs-done/2026-03-25-add-alibaba-provider.md` explicitly lists acceptance criteria:
  - "Alibaba appears as a provider option in onboarding"
  - Create `alibaba-onboarding.tsx` component

- **Current implementation**: `frontend/app/onboarding/_components/onboarding-card.tsx` has hardcoded tabs for:
  - Anthropic (LLM only)
  - OpenAI
  - IBM watsonx
  - Ollama

- **Missing**: No Alibaba tab, no `alibaba-onboarding.tsx`, no Alibaba logo icon

## Missing Components

1. **Tab trigger** in `onboarding-card.tsx` - needs `TabsTrigger value="alibaba"`
2. **Tab content** - needs `TabsContent value="alibaba"` with AlibabaOnboarding component
3. **Onboarding component** - `frontend/app/onboarding/_components/alibaba-onboarding.tsx` doesn't exist
4. **Icon** - `frontend/components/icons/alibaba-logo.tsx` doesn't exist
5. **Provider order logic** in `handleSetModelProvider` and auto-select effect needs Alibaba

## Root Cause

**GSD Workflow Gap** - The spec-to-plan handoff had no verification that all spec requirements become plan tasks.

1. CONTEXT.md correctly captured "Add Alibaba to onboarding flow" in `<decisions>` section
2. But 03-PLAN.md didn't create a task for it - just a note
3. AGENT_LOOPS Step 7-8 (Review Agents) was marked "optional but recommended" and was skipped
4. No automated check verified all CONTEXT.md decisions were covered by plan tasks

## Workflow Fix Applied

1. **AGENT_LOOPS.md**: Step 7-8 now marked as **MANDATORY — cannot be skipped**
2. **plan-phase.md**: Added new Step 12 "Context Decisions Coverage Gate" that:
   - Extracts all decisions from CONTEXT.md `<decisions>` section
   - Verifies each decision appears in at least one plan task
   - Blocks proceed until all decisions are covered or explicitly deferred

## Related Files

- `frontend/app/onboarding/_components/onboarding-card.tsx` - main file to update
- `frontend/app/settings/page.tsx` - has Alibaba integration in settings (working)
- `.planning/specs-done/2026-03-25-add-alibaba-provider.md` - original spec

## Priority

Medium - Users who want to use Alibaba Cloud cannot complete onboarding.

## Reported

2026-03-25

## Root Cause Fixed

2026-03-25 - GSD workflow updated to prevent future occurrences