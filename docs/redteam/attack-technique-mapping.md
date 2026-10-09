# MITRE ATT&CK Technique Mapping

**Project:** CyGRC Module 2 - VAPT & Red Team
**Workstream:** Atomic Red Team & Technique Execution
**Branch:** feature/redteam-atomic
**Mapping status:** Draft - pending review

## Purpose

Map each approved Atomic Red Team test to its corresponding MITRE
ATT&CK technique, simulated behavior, expected telemetry, and
validation evidence.

A technique mapping documents the behavior being tested. It does not
by itself prove that the behavior was detected by a security control.

## Technique Mapping

| Field | RT-AT-001 |
|---|---|
| Test name | NTFS Alternate Data Stream Access |
| Atomic test GUID | 8e5c5532-1181-4c1d-bb79-b3a9f5dbd680 |
| ATT&CK tactic | Execution |
| ATT&CK technique ID | T1059.001 |
| ATT&CK technique | Command and Scripting Interpreter: PowerShell |
| Platform | Windows |
| Test objective | Generate controlled PowerShell activity for telemetry validation |
| Execution result | PASS |
| Telemetry result | NOT OBSERVED by the targeted query |
| Detection result | INCOMPLETE |
| Cleanup result | PASS for the checked temporary file |
| Review status | PENDING |

## Validation Matrix

| Validation stage | Evidence required | Current result |
|---|---|---|
| Test execution | Command, timestamp, exit code, and observed output | PASS |
| Event generation | Test-specific event or trace | NOT CONFIRMED |
| Event collection | Relevant event present in collected logs | PARTIAL |
| Security detection | Detection attributable to the intended test behavior | NOT CONFIRMED |
| Alert validation | SIEM or centralized alert evidence, if applicable | NOT CHECKED |
| Cleanup | Evidence that expected test-created artifacts were removed | PASS for the checked file |
| System restoration | Evidence that relevant system state returned to baseline | NOT FULLY ASSESSED |

## Evidence References

Raw evidence is stored outside the Git repository.

- Execution record: `docs/redteam/execution-records/RT-AT-001.md`
- Telemetry record: `docs/redteam/telemetry-records/RT-AT-001-telemetry.md`
- Cleanup record: `docs/redteam/cleanup-records/RT-AT-001-cleanup.md`
- Evidence directory: `C:\Users\alaka\cygrc-security\evidence\redteam`

Refer to the execution record and external evidence files for the
actual commands, timestamps, outputs, and collected event data.

## Defender Findings

Microsoft Defender reported two detections during the recorded
evidence window. Their relationship to RT-AT-001 has not been
established. They must not be counted as confirmed detection of the
intended test activity.

Further Atomic execution remains paused pending team-lead review.

## Mapping and Review Rules

1. Map only the behavior actually represented by the approved test.
2. Record the technique ID and tactic with the source test identifier.
3. Separate execution success from event generation, collection,
   detection, and alert validation.
4. Link each conclusion to evidence.
5. Record unverified results as NOT CHECKED, NOT CONFIRMED, or PARTIAL
   as appropriate; do not infer success from missing errors.
6. Record the reviewer and review date when review actually occurs.
7. Confirm authorization and scope before adding or executing tests.

## Future Test Entries

Add a new mapping row only after the candidate test has been reviewed.
Record its test ID, Atomic test identifier, ATT&CK technique, approved
scope, expected telemetry, evidence reference, cleanup result, and
review status.

Do not execute additional tests while the current Defender findings
and testing authorization remain unresolved.
