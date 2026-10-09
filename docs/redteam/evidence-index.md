# Atomic Red Team Execution Evidence Index

**Project:** CyGRC Module 2 — VAPT & Red Team  
**Workstream:** Atomic Red Team & Technique Execution  
**Evidence Storage Location:** External (`C:\Users\alaka\cygrc-security\evidence\redteam\`)  
**Index Status:** Active — Verified Evidentiary Baseline  
**Branch:** `feature/redteam-atomic`  

---

## 1. Purpose & Evidence Handling Standards

This index serves as the central audit register for test authorization, execution artifacts, raw transcripts, event logs, telemetry validations, and cleanup records.

### Evidence Integrity & Security Standards:
1. **External Repository Segregation:** In accordance with project policy, raw execution logs, terminal transcripts, and telemetry exports are stored outside the Git repository at `C:\Users\alaka\cygrc-security\evidence\redteam\` to prevent accidental leakage of sensitive tokens, user identities, or internal network topology.
2. **Cryptographic Integrity:** All verified evidence files are indexed with their exact byte sizes, modification timestamps, and SHA-256 cryptographic hashes to ensure non-repudiation.
3. **No Fabrication Policy:** Missing or inconclusive evidence is explicitly reported as `NOT OBSERVED` or `PARTIAL`. Results are never embellished.

---

## 2. Master Test Evidence Register

| Test ID | Technique ID | Test Name | Execution Status | Internal Documentation | Raw External Evidence Artifacts | Telemetry Status | Detection Status | Review Status |
|---|---|---|---|---|---|---|---|---|
| **RT-AT-001** | T1059.001 / T1564.004 | NTFS Alternate Data Stream Access | **PASS** (Executed) | `docs/redteam/execution-records/RT-AT-001.md` | Baseline, Transcripts, Start/End, Event CSV, Defender Log | NOT OBSERVED (Targeted query) | INCOMPLETE | PENDING LEAD REVIEW |
| **RT-AT-002** | T1082 | System Information Discovery | **APPROVED CANDIDATE** | Catalog entry in `atomic-test-catalog.md` | *Planned: RT-AT-002-transcript.txt, sec-events.csv* | Model Ready | Pending Execution | Awaiting Lab Gate |
| **RT-AT-003** | T1033 | System Owner/User Discovery | **APPROVED CANDIDATE** | Catalog entry in `atomic-test-catalog.md` | *Planned: RT-AT-003-transcript.txt, sec-events.csv* | Model Ready | Pending Execution | Awaiting Lab Gate |
| **RT-AT-004** | T1057 | Process Discovery | **APPROVED CANDIDATE** | Catalog entry in `atomic-test-catalog.md` | *Planned: RT-AT-004-transcript.txt, sec-events.csv* | Model Ready | Pending Execution | Awaiting Lab Gate |
| **RT-AT-005** | T1070.004 | Indicator Removal: File Deletion | **APPROVED CANDIDATE** | Catalog entry in `atomic-test-catalog.md` | *Planned: RT-AT-005-transcript.txt, sysmon-events.csv* | Model Ready | Pending Execution | Awaiting Lab Gate |
| **RT-AT-006** | T1112 | Modify Registry (HKCU Test Key) | **APPROVED CANDIDATE** | Catalog entry in `atomic-test-catalog.md` | *Planned: RT-AT-006-transcript.txt, sysmon-events.csv* | Model Ready | Pending Execution | Awaiting Lab Gate |
| **RT-AT-007** | T1059.001 | PowerShell Encoded Command | **APPROVED CANDIDATE** | Catalog entry in `atomic-test-catalog.md` | *Planned: RT-AT-007-transcript.txt, ps-events.csv* | Model Ready | Pending Execution | Awaiting Lab Gate |
| **RT-AT-008** | T1016 | Network Configuration Discovery | **APPROVED CANDIDATE** | Catalog entry in `atomic-test-catalog.md` | *Planned: RT-AT-008-transcript.txt, sec-events.csv* | Model Ready | Pending Execution | Awaiting Lab Gate |

---

## 3. Cryptographic Evidence Manifest for Verified Executions

### RT-AT-001 Execution Artifacts (Host: `ALAKATI`, Windows 11)
Location: `C:\Users\alaka\cygrc-security\evidence\redteam\`

| File Name | File Size (Bytes) | Timestamp (Local) | SHA-256 Cryptographic Hash | Description |
|---|---|---|---|---|
| `environment-baseline.txt` | 739 | 2026-10-09 20:02:24 | `E56330B34FC5F048B38185B6AE695AB04F3C79657C981D7A18B24DE4D72E0B34` | System state baseline: OS build, active user, running processes, elevation check |
| `RT-AT-001-start.txt` | 31 | 2026-10-09 20:28:22 | `15E37DB9DEDB47A1E84A531FFF0E8E926FC54FEA55F8F1E5582F2F1E55238048` | High-precision start timestamp: `2026-10-09T20:28:22.855+05:30` |
| `RT-AT-001-end.txt` | 31 | 2026-10-09 20:29:26 | `69125CF0557CB9452CF04D2B8FA642DC5E3C85BEA543EB1E85E57934FE23A56F` | High-precision end timestamp: `2026-10-09T20:29:26.488+05:30` |
| `RT-AT-001-transcript.txt` | 2,495 | 2026-10-09 20:29:26 | `4BBCA7AFD0B7FC66B191F0FBE6376AEB23DED3A7186274C43F0215ACA7D40638` | Full PowerShell session transcript showing command execution and output `Stream Data Executed` |
| `RT-AT-001-event-window.csv` | 432,674 | 2026-10-09 20:31:48 | `756CEF0A419B620A0C921FB6B6D0E29E4EDEF58D5E762BA2732ED2C2CC7D11B3` | Raw export of 42 PowerShell Operational events captured during the execution time window |
| `RT-AT-001-telemetry-summary.txt` | 715 | 2026-10-09 20:31:48 | `4A53B6EE9B7689F00E5F0362C9038DC937B2CDADC0453187A5E83851C929E8B8` | Summary of targeted query showing zero matches for specific ADS keywords |
| `RT-AT-001-defender-findings.txt` | 5,078 | 2026-10-09 20:47:13 | `785E7562C7EE4EEF7180AD2DA337A655900BAEABE6C390BEB78B697302441C4C` | Export of Defender Operational Event IDs 1116/1117 (quarantine of adjacent repo files) |

---

## 4. Evidence Review & Audit Checklist

The following audit items must be validated before closing any test record:
- [x] Execution transcript captures exact command line, operator, timestamp, and standard output.
- [x] Process exit code is captured accurately (`0` for RT-AT-001).
- [x] Telemetry query time window is recorded and exported to CSV.
- [x] Negative or missing telemetry findings are honestly documented (`NOT OBSERVED`).
- [x] Antivirus / Defender quarantine actions are investigated and segregated from test-specific detection.
- [x] Cleanup command execution and post-cleanup verification (`Test-Path`) are confirmed.
- [ ] Team Lead formal review and sign-off recorded.

---

## 5. Reviewer Status & Next Action Gate

- **Reviewer:** Aviral Mishra (Team Lead)
- **Review Date:** Pending Review
- **Approval Status:** **PAUSED** pending evaluation of Defender quarantine findings and lab environment provisioning.
