# Atomic Red Team Execution Evidence Index

**Project:** CyGRC Module 2 - VAPT & Red Team
**Workstream:** Atomic Red Team & Technique Execution
**Evidence storage:** Outside the Git repository
**Index status:** Draft - pending review

## Purpose

Provide a central index for test authorization, execution records,
raw evidence, ATT&CK mapping, telemetry validation, and cleanup.

## Test Evidence Register

| Field | RT-AT-001 |
|---|---|
| Test name | NTFS Alternate Data Stream Access |
| Approval reference | Not recorded |
| Execution record | `docs/redteam/execution-records/RT-AT-001.md` |
| ATT&CK mapping | `docs/redteam/attack-technique-mapping.md` |
| Telemetry record | `docs/redteam/telemetry-records/RT-AT-001-telemetry.md` |
| Cleanup record | `docs/redteam/cleanup-records/RT-AT-001-cleanup.md` |
| Evidence directory | `C:\Users\alaka\cygrc-security\evidence\redteam` |
| Baseline evidence | `environment-baseline.txt` |
| Start evidence | `RT-AT-001-start.txt` |
| End evidence | `RT-AT-001-end.txt` |
| Command transcript | `RT-AT-001-transcript.txt` |
| PowerShell event window | `RT-AT-001-event-window.csv` |
| Telemetry summary | `RT-AT-001-telemetry-summary.txt` |
| Defender findings | `RT-AT-001-defender-findings.txt` |
| Execution result | PASS |
| Telemetry validation | PARTIAL |
| Detection validation | INCOMPLETE |
| Cleanup result | PASS for the checked temporary file |
| Full restoration | NOT ASSESSED |
| Reviewer status | PENDING |

## Evidence Handling Requirements

1. Preserve original evidence files and their timestamps.
2. Do not place credentials, tokens, personal data, or sensitive raw
   logs in the Git repository.
3. Reference evidence by filename and record its collection time.
4. Record any missing, inaccessible, or incomplete evidence explicitly.
5. If evidence integrity is required, record a SHA-256 hash and the
   collection method in the evidence manifest.
6. Restrict access to evidence according to project requirements.
7. Do not modify original evidence to make results appear complete.

## Review Checklist

- [ ] Confirm the test's approval reference and authorized scope.
- [ ] Confirm execution commands and timestamps against the transcript.
- [ ] Confirm the ATT&CK mapping matches the test behavior.
- [ ] Confirm telemetry conclusions against the collected event data.
- [ ] Review Defender findings separately from intended test detection.
- [ ] Verify cleanup evidence and document restoration limitations.
- [ ] Record reviewer, review date, and follow-up actions.

## Outstanding Items

- Record the relevant approval reference.
- Complete team-lead review of Defender findings.
- Confirm the approved environment for future Atomic tests.
- Complete any additional restoration assessment only after review.
- Keep further Atomic execution paused until approval is confirmed.

## Review

- Reviewer: Pending
- Review date: Pending
- Status: PENDING
