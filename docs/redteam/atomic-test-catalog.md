# Atomic Red Team Test Catalog

**Project:** CyGRC Module 2 - VAPT & Red Team
**Owner:** Alakati Rithesh Chandra
**Git branch:** feature/redteam-atomic

## Test Catalog

| Field | Value |
|---|---|
| Test ID | RT-AT-001 |
| Test name | NTFS Alternate Data Stream Access |
| Atomic test GUID | 8e5c5532-1181-4c1d-bb79-b3a9f5dbd680 |
| ATT&CK tactic | Execution |
| ATT&CK technique ID | T1059.001 |
| ATT&CK technique | Command and Scripting Interpreter: PowerShell |
| Target operating system | Windows 11 |
| Objective | Generate controlled PowerShell activity for telemetry validation |
| Elevation required | No |
| Execution status | PASS |
| Execution evidence | Stored outside repository |
| Cleanup status | PASS |
| Telemetry status | NOT OBSERVED by the targeted query |
| Detection status | INCOMPLETE - intended activity detection not confirmed |
| Reviewer status | Pending |

## Findings

- The Atomic test returned exit code 0.
- The expected output, `Stream Data Executed`, was observed.
- The cleanup command completed.
- The test-created temporary file was absent after cleanup.
- The PowerShell Operational log was enabled and contained events in the selected window.
- The initial query found no matching events for the selected terms and event IDs.
- Event ID 4104 records were present in the broader event query, but test-specific telemetry was not confirmed.
- Detection or alert validation remains incomplete.

## Execution Rules

1. Confirm authorization and scope before each test.
2. Review the upstream Atomic test definition and prerequisites.
3. Execute only the approved test.
4. Record actual commands, timestamps, outputs, and errors.
5. Map executed actions to MITRE ATT&CK.
6. Validate event generation, collection, detection, and alerting separately.
7. Perform and verify cleanup.
8. Store sensitive execution evidence outside the repository.
9. Report unexpected effects or cleanup failures.
10. Submit changes through a pull request.

## Status Definitions

- PROPOSED: Candidate identified; not yet approved.
- APPROVED: Scope and test approved.
- PASS: Defined execution criteria met.
- FAIL: An expected criterion was not met.
- NOT OBSERVED: Expected telemetry was not identified by the documented check.
- NOT CHECKED: Validation has not been performed.
- BLOCKED: A prerequisite or approval is missing.
- CLEANED: Cleanup completed and the documented restoration checks passed.

A successful command alone does not prove that a security detection worked.

## Workstream Deliverables

| Deliverable | Location | Purpose |
|---|---|---|
| Atomic test catalog | `docs/redteam/atomic-test-catalog.md` | Inventory and status of approved tests |
| Execution record template | `docs/redteam/templates/execution-record.md` | Standardized authorization, execution, and validation records |
| Cleanup checklist | `docs/redteam/templates/cleanup-checklist.md` | Reusable cleanup and restoration verification |
| ATT&CK technique mapping | `docs/redteam/attack-technique-mapping.md` | Maps tests to ATT&CK techniques and validation outcomes |
| Evidence index | `docs/redteam/evidence-index.md` | Central index of execution and validation evidence |
| Engagement scope | `docs/redteam/engagement-scope.md` | Scope, authorization, and outstanding approvals |

## End-to-End Record Lifecycle

1. **Authorize:** Confirm the approved environment, target, test, and testing window.
2. **Prepare:** Review the Atomic test definition, prerequisites, expected behavior, and cleanup procedure.
3. **Execute:** Run only the approved test and record exact commands, timestamps, exit codes, outputs, and errors.
4. **Map:** Link the observed behavior to the relevant ATT&CK technique.
5. **Validate:** Assess event generation, event collection, security detection, and alerting separately.
6. **Clean up:** Remove approved test-created artifacts and document restoration checks and residual artifacts.
7. **Review:** Link the evidence, record limitations, obtain reviewer decisions, and document follow-up actions.

## Current Workstream Gate

- RT-AT-001 execution: PASS.
- Temporary-file cleanup: PASS for the checked file only.
- Test-specific telemetry: NOT OBSERVED by the targeted query.
- Detection validation: INCOMPLETE.
- Defender findings: Awaiting team-lead review.
- Engagement authorization: Pending confirmation.
- Further Atomic execution: PAUSED pending review and approval.

Do not interpret successful execution or temporary-file removal as proof
of successful detection or complete system restoration.
