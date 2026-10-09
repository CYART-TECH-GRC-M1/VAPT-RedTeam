# RT-AT-001 — Telemetry Validation Record

## 1. Test Information

- Record ID: RT-AT-001
- Test: NTFS Alternate Data Stream Access
- Atomic Test Number: 11
- ATT&CK Technique: T1059.001 — PowerShell
- Test Execution Status: PASS
- Cleanup Status: PASS
- Telemetry Validation Status: PARTIAL
- Detection Validation Status: INCOMPLETE
- Review Status: PENDING

## 2. Evidence Window

- Start: 2026-10-09 20:28:22.855 +05:30
- End: 2026-10-09 20:29:26.488 +05:30
- Evidence Location: Stored outside the Git repository at
  `C:\Users\alaka\cygrc-security\evidence\redteam`

Relevant evidence files:

- `RT-AT-001-event-window.csv`
- `RT-AT-001-telemetry-summary.txt`
- `RT-AT-001-defender-findings.txt`
- `RT-AT-001-transcript.txt`

## 3. PowerShell Telemetry

- PowerShell Operational log records were collected for the test window.
- Event IDs 4104, 40962, 40961, and 53504 were present in the exported window.
- A targeted search for `NTFS_ADS`, `Stream Data Executed`,
  `streamCommand`, `Invoke-Expression`, and `Add-Content` returned
  no matching records in the exported event data.
- Therefore, the collected events do not establish that the intended
  test activity was detected by the queried telemetry.
- The presence of PowerShell events alone is not proof of test-specific
  detection.
- Script-block logging policy configuration has not been fully validated.

## 4. Microsoft Defender Findings

During the same evidence window, Microsoft Defender Operational events
reported the following detections:

- `Trojan:Script/Wacatac.H!ml`
  - Resource: `T1059.001/src/Invoke-DownloadCradle.ps1`
  - Event IDs: 1116 and 1117
- `VirTool:MSIL/SoapHound!rfn`
  - Resource: `T1059.001/bin/SOAPHound.exe`
  - Event IDs: 1116 and 1117

Defender reported quarantine actions for both resources, and the
collected threat-detection data reported `ActionSuccess: True`.

These resources are different from the temporary `NTFS_ADS.txt` file
used by the documented Test 11 commands. The documented Test 11
commands do not reference these two resources. The detections occurred
during the same time window, but a causal relationship with Test 11
has not been established.

The detections are recorded as separate Defender findings and must not
be treated as proof that Test 11 was detected.

## 5. Validation Results

| Validation Item | Result | Notes |
| --- | --- | --- |
| Test command execution | PASS | Expected output was observed |
| Temporary test-file cleanup | PASS | File was absent after cleanup |
| PowerShell events collected | PARTIAL | Events exist, but no test-specific match was found |
| Intended test activity detected | NOT CONFIRMED | No matching event found in the targeted query |
| Defender findings reviewed | PENDING | Lead review required |
| SIEM or centralized alert validation | NOT CHECKED | No validation recorded |
| Remaining artifacts fully assessed | NOT CONFIRMED | Further assessment pending review |

## 6. Conclusion

The test executed successfully and the documented temporary file was
removed. However, the collected evidence does not confirm test-specific
PowerShell telemetry or detection of the intended activity.

Defender reported two separate detections and quarantine actions during
the evidence window. Their relationship to Test 11 has not been
established.

No further Atomic tests should be executed on this workstation until
the Defender findings and next testing steps have been reviewed by
the team lead.

## 7. Review and Follow-up

- Reviewer: Pending
- Review date: Pending
- Approval reference: Not recorded
- Follow-up: Review Defender findings, verify logging configuration,
  and agree on an approved test environment before further execution.
