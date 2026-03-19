# Phase 4: Automated Tests and Test Report (20-30 mins)

## Goal of Phase 4
By the end of this phase you should have:
- Run your automated tests and captured the results (pass/fail)
- Triage any failures using a simple, repeatable approach
- Written a short test report (5-8 bullets) that explains what you tested and what you changed
- Reflected on AI usage and what decisions you still had to make yourself
- Done a final gap analysis: what is still not fully proven

This is about **evidence**. You are proving your validator works, and you can explain it.

## Timebox (suggested)
- 0:00-0:10 Prepare and run tests
- 0:10-0:15 Fix or adjust (only if needed) and re-run tests
- 0:15-0:25 Write test report + reflection
- 0:25-0:30 Final gap analysis

## Step-by-step guidance

### 1) Choose your test approach (0:00-0:05)
Use plain Python `assert`s (simple and reliable for this exercise).

For this exercise, it should:
- Cover at least 10 cases
- Include happy path, negative tests, and edge/risk cases
- Assert expected `decision` and expected `reason` codes

### 2) Final check before running (0:05-0:08)
Before you run:
1. Make sure your tests import the validator you wrote
   - example: your tests should call `validate_payment(...)`
2. Ensure your assertions are stable
   - reason codes are short stable strings
   - do not assert large free-text messages
3. Ensure reason-code ordering matches your design
   - for example: functional invalid reasons first, then risk reasons

If anything is unclear, fix it now rather than after the first failing run.

### 3) Run the tests (0:08-0:10)
Run your test script (example for the starter files):
- `python test_validator.py`

Record what happened:
- Did all tests pass?
- If not, which test failed first?

### 4) Triage failures with the “code vs expectation” rule (0:10-0:15)
When tests fail, do not guess. Use this approach:
1. Identify the first failing test
2. Ask:
   - Is the **requirement** wrong (your test expectations do not match the scenario)?
   - Or is the **code** wrong (your implementation does not match your own expectations)?
3. Only then decide:
   - If the scenario/requirements are clear: prefer changing the code
   - If you made an incorrect assumption in Phase 1: update your assumptions and adjust tests/implementation consistently

After changing anything:
- Re-run the tests
- Confirm the same failure is gone

### 5) Write the Test Report (0:15-0:22)
Your test report must be short but specific.

Include these 5-8 bullets:
1. What you tested (briefly describe happy path, negative, and edge/risk coverage)
2. What failed first (if anything)
3. What you changed (code changes, test expectation changes, or both)
4. Any remaining risks or gaps (what you still do not fully prove)
5. What you would do next in a real bank project
   - examples: more fraud rules, performance, logging, audit trail

Template you can copy:
```text
Test report
- Coverage: happy path, negative tests, boundary tests, refer risk gates
- First failure: <test name or short description>
- Fix applied: <what changed and why>
- Remaining gaps: <rule ids not fully proven or missing edge cases>
- Next steps: <one or two improvements for a real release>
```

### 6) Reflect on AI usage (0:22-0:25)
Write a short reflection:
- Where did AI help most (planning, coding, debugging, or test design)?
- Where did you still need to decide yourself?
- Did you validate AI output with your own reasoning and tests?

### 7) Final gap analysis (0:25-0:30)
Answer these questions:
1. Which rule IDs are still not fully proven by tests, and why?
2. If you had more time, what is the single most valuable extra test to add?

Mermaid diagram (optional): triage and re-run flow

```mermaid
flowchart TD
  A[Run tests] --> B[Triage first failure]
  B --> C[Decide code or expectation change]
  C --> D[Re-run tests]
  D --> E[Write test report]
  E --> F[Final gap analysis]
```

## End-of-Phase 4 checklist
- [ ] I ran the automated tests and recorded results
- [ ] Any failures were triaged using a code vs expectation decision
- [ ] I re-ran tests after changes
- [ ] My test report contains what I tested, what failed first, what I changed, and what gaps remain
- [ ] I included a short reflection on AI use
- [ ] I listed the single most valuable extra test I would add next

