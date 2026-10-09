# RT-AT-001 - Atomic Red Team Execution Record

## Identification
- Test ID: RT-AT-001
- Test name: NTFS Alternate Data Stream Access
- Atomic test GUID: 8e5c5532-1181-4c1d-bb79-b3a9f5dbd680
- ATT&CK technique: T1059.001 - PowerShell
- Operator: ALAKATI\alaka
- Approval: Team lead approval reported; approval reference not recorded

## Scope
- Target: Local Windows laptop
- Operating system: Windows 11 (baseline recorded separately)
- Start timestamp: 2026-10-09T20:28:22.855+05:30
- End timestamp: 2026-10-09T20:29:26.488+05:30
- Atomic test number: 11

## Execution Results
- Result: PASS
- Exit code: 0
- Expected output observed: Stream Data Executed
- Transcript: RT-AT-001-transcript.txt
- Unexpected behavior: None reported

## Telemetry Validation
- PowerShell Operational log enabled: YES
- Events in selected time window: 42
- Matching events in initial targeted query: 0
- Event ID 4104 records present in broader query: YES
- Test-specific telemetry confirmed: NO
- Telemetry status: NOT OBSERVED
- Detection or alert validation: NOT CHECKED
- Event export: RT-AT-001-event-window.csv
- Telemetry summary: RT-AT-001-telemetry-summary.txt

## Cleanup
- Cleanup command: Atomic Red Team cleanup for T1059.001, test 11
- Cleanup command completed: YES
- Temporary file absent after cleanup: YES
- Cleanup result: PASS
- Restoration verification: Temporary test file absence confirmed
- Remaining artifacts: Not fully assessed

## Evidence Location
Evidence is stored outside the repository at:
C:\Users\alaka\cygrc-security\evidence\redteam

## Reviewer
- Reviewer: Pending
- Review status: Pending

## Notes
Execution and cleanup passed. Test-specific telemetry was not identified by
the query used. This does not establish that no telemetry exists. Detection
validation remains incomplete.
