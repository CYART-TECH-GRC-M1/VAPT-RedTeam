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
