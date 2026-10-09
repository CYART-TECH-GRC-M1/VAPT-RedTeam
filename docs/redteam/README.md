# Atomic Red Team & Technique Execution Workstream

**Project:** CyGRC Platform — Module 2 (VAPT & Red Team)  
**Workstream:** Atomic Red Team & Technique Execution  
**Workstream Owner:** Alakati Rithesh Chandra  
**Team Lead:** Aviral Mishra  
**Git Branch:** `feature/redteam-atomic`  
**Git Workflow:** All changes submitted via Pull Request targeting `main`. Direct commits to `main` are prohibited.  

---

## 1. Executive Overview

This directory contains the documentation, test catalog, execution records, MITRE ATT&CK mappings, telemetry validations, and cleanup procedures for the **Atomic Red Team & Technique Execution** workstream.

### The Problem It Solves:
Traditional vulnerability assessments (VAPT) identify security weaknesses in code, APIs, and infrastructure, but they do not validate whether security operations centers (SOC) or endpoint detection mechanisms actually detect adversarial techniques in real time. The Atomic Red Team workstream fills this gap by executing small, controlled, single-technique units of adversarial activity mapped to the MITRE ATT&CK framework, enabling detection engineers to verify and fine-tune telemetry generation, collection, and alerting.

### Core Tenets:
- **Safety First:** Tests are non-destructive and limited strictly to safe discovery, execution, and defense evasion techniques requiring standard user privileges.
- **Strict Evidence Integrity:** A command succeeding with exit code `0` is never equated with defensive detection. Every claim of detection requires corroborating event logs.
- **External Evidence Segregation:** Raw execution transcripts, event CSVs, and screen captures are stored outside the Git repository at `C:\Users\alaka\cygrc-security\evidence\redteam\` to prevent accidental exposure of tokens or sensitive telemetry.
- **Guaranteed Cleanup:** Every executed test has an associated rollback and post-cleanup verification check to guarantee zero unintended persistence.

---

## 2. Directory Architecture & Deliverables Index

```
docs/redteam/
├── README.md                      # Workstream overview, navigation, and PR guidelines (this document)
├── atomic-test-catalog.md         # Deliverable A: Curated catalog of Atomic tests with full technical specifications
├── attack-technique-mapping.md    # Deliverable C: MITRE ATT&CK mapping, detection logic, Sigma rules & gaps
├── cleanup-checklist.md           # Deliverable D: Master operational cleanup matrix and verification protocol
├── execution-guide.md             # Deliverable E: Step-by-step SOP for environment prep, execution & telemetry check
├── evidence-index.md              # Deliverable B: Master evidence register and SHA-256 manifest of raw artifacts
├── engagement-scope.md            # Rules of engagement, authorization boundaries, and stop conditions
├── completion-report.md           # Deliverable G: Workstream audit, deliverables summary, and completion report
│
├── execution-records/             # Individual execution records for completed tests
│   └── RT-AT-001.md               # Execution record for NTFS Alternate Data Stream Access (Test 11)
│
├── telemetry-records/             # Individual telemetry and detection validation records
│   └── RT-AT-001-telemetry.md     # Telemetry analysis and Defender quarantine findings for RT-AT-001
│
├── cleanup-records/               # Test-specific cleanup and restoration records
│   └── RT-AT-001-cleanup.md       # Restoration verification record for RT-AT-001
│
└── templates/                     # Standardized reusable markdown templates
    ├── execution-record.md        # Standard execution record template
    └── cleanup-checklist.md       # Standard cleanup checklist template
```

---

## 3. Curated Atomic Red Team Catalog Summary

| Test ID | MITRE Technique | Tactic | Objective | Status | Telemetry Result |
|---|---|---|---|---|---|
| **RT-AT-001** | `T1059.001` / `T1564.004` | Execution / Defense Evasion | NTFS Alternate Data Stream PowerShell execution | **PASS** (Executed) | Targeted query: NOT OBSERVED; Defender quarantined adjacent repo files |
| **RT-AT-002** | `T1082` | Discovery | System Information Discovery (`systeminfo`) | **APPROVED CANDIDATE** | Telemetry model ready; pending execution |
| **RT-AT-003** | `T1033` | Discovery | System Owner/User Discovery (`whoami /all`) | **APPROVED CANDIDATE** | Telemetry model ready; pending execution |
| **RT-AT-004** | `T1057` | Discovery | Process Discovery (`tasklist /v`) | **APPROVED CANDIDATE** | Telemetry model ready; pending execution |
| **RT-AT-005** | `T1070.004` | Defense Evasion | Indicator Removal: Benign File Deletion | **APPROVED CANDIDATE** | Telemetry model ready; pending execution |
| **RT-AT-006** | `T1112` | Defense Evasion | Modify Registry: Benign HKCU Test Key | **APPROVED CANDIDATE** | Telemetry model ready; pending execution |
| **RT-AT-007** | `T1059.001` | Execution | PowerShell Base64 Encoded Command Execution | **APPROVED CANDIDATE** | Telemetry model ready; pending execution |
| **RT-AT-008** | `T1016` | Discovery | System Network Configuration Discovery (`ipconfig`) | **APPROVED CANDIDATE** | Telemetry model ready; pending execution |

---

## 4. Workstream Status & Operational Gate

- **Completed Live Execution:** `RT-AT-001` executed on 2026-10-09. Standard output observed (`Stream Data Executed`), exit code `0`, temporary test file cleaned up and absence confirmed.
- **Telemetry Observation:** Targeted query of the exported PowerShell Operational log returned zero matches for specific ADS keywords. Telemetry generation is recorded as `NOT OBSERVED` for the queried event slice.
- **Defender Detections:** Microsoft Defender flagged two inactive tools (`Invoke-DownloadCradle.ps1` and `SOAPHound.exe`) in the upstream clone directory `C:\AtomicRedTeam\atomic-red-team\atomics\T1059.001\`. These represent static signature detections on disk, not behavioral detections of RT-AT-001.
- **Operational Gate:** Live execution on the local host is **PAUSED**. Further atomic test runs will proceed once the team lead reviews the Defender findings and authorizes an isolated lab/sandbox environment.

---

## 5. Git Contribution & Pull Request Standards

1. Work only on branch `feature/redteam-atomic`.
2. Do not commit credentials, tokens, customer data, or raw log files into Git.
3. Validate all Markdown formatting and link references before submitting.
4. Open a Pull Request targeting branch `main` with a comprehensive description covering scope, changes, verification, evidence hashes, and operational status.
