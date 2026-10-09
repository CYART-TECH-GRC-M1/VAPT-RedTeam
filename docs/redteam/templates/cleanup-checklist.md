# Atomic Red Team Cleanup Checklist

- Test ID:
- Test name:
- Operator:
- Cleanup start timestamp with timezone:
- Cleanup end timestamp with timezone:
- Reviewer:
- Status: NOT STARTED / IN PROGRESS / PASS / FAIL / BLOCKED

## Pre-cleanup

- [ ] Confirm the test-specific cleanup instructions.
- [ ] Record the pre-execution baseline.
- [ ] Record artifacts and changes created by the test.
- [ ] Confirm the approved cleanup scope.

## Cleanup

- [ ] Run the approved cleanup procedure.
- [ ] Check whether temporary files were removed.
- [ ] Check whether configuration changes were reversed.
- [ ] Check whether temporary accounts, processes or services require restoration.
- [ ] Preserve execution and cleanup evidence.

## Verification

- [ ] Verify the target against the expected baseline.
- [ ] Document residual artifacts or cleanup failures.
- [ ] Record evidence supporting each completed check.
- [ ] Notify the project lead if cleanup is incomplete.
- [ ] Record final cleanup status and reviewer decision.

## Notes

- Remaining artifacts:
- Restoration limitations:
- Evidence references:
- Escalation reference:

Do not remove pre-existing files or alter unrelated system state.
Only perform cleanup actions relevant to the approved test.
