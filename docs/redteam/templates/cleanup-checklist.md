# Atomic Red Team Cleanup Checklist

## Test Identification

- Test ID:
- Test name:
- Operator:
- Approval reference:
- Target:
- Cleanup start timestamp with timezone:
- Cleanup end timestamp with timezone:
- Reviewer:
- Status: NOT STARTED / IN PROGRESS / PASS / FAIL / PARTIAL / BLOCKED

## 1. Before Cleanup

- [ ] Confirm the approved test and cleanup scope.
- [ ] Review the test-specific cleanup instructions.
- [ ] Record the artifacts and changes created by the test.
- [ ] Preserve execution evidence before changing system state.
- [ ] Identify pre-existing files and configuration that must not be altered.

## 2. Perform Cleanup

- [ ] Run the approved test-specific cleanup procedure.
- [ ] Check whether expected temporary files were removed.
- [ ] Check whether test-created configuration changes were reversed.
- [ ] Check test-created accounts, processes, services, and scheduled tasks, if applicable.
- [ ] Record cleanup command, timestamp, output, and exit code.
- [ ] Preserve cleanup evidence.

## 3. Verify Cleanup and Restoration

- [ ] Verify each expected test-created artifact.
- [ ] Compare relevant system state against the recorded baseline.
- [ ] Record residual artifacts and restoration limitations.
- [ ] Confirm unrelated and pre-existing system state was not intentionally changed.
- [ ] Record evidence references for completed checks.
- [ ] Escalate incomplete or unexpected cleanup results to the project lead.

## 4. Closure Record

- Cleanup command or procedure:
- Cleanup exit code:
- Artifacts verified:
- Artifacts removed:
- Residual artifacts:
- Baseline comparison:
- Restoration status: VERIFIED / PARTIAL / NOT VERIFIED / NOT APPLICABLE
- Evidence references:
- Escalation reference:
- Reviewer decision:
- Review date:

## Status Rules

- PASS: All required, documented cleanup checks passed.
- PARTIAL: Some checks passed, but restoration or residual-artifact checks remain.
- FAIL: A required cleanup check failed.
- BLOCKED: Cleanup cannot safely proceed without approval or intervention.

Do not remove pre-existing files or alter unrelated system state.
Do not claim full restoration based only on removal of one temporary file.
