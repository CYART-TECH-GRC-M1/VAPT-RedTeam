# Atomic Red Team Cleanup & System Restoration Checklist

**Project:** CyGRC Module 2 — VAPT & Red Team  
**Workstream:** Atomic Red Team & Technique Execution  
**Document:** Master Operational Cleanup Protocol  
**Branch:** `feature/redteam-atomic`  
**Status:** Approved Operational Protocol  

---

## 1. Safety Principles & Cleanup Mandate

A hallmark of professional Red Team and security unit testing is **operational safety and environmental integrity**. Every Atomic Red Team test executed must leave the host in an identical or cleanly restored state.

### Core Mandates:
1. **Zero Unintended Persistence:** No test-created files, registry values, user accounts, scheduled tasks, or services may remain after testing concludes.
2. **Blast-Radius Containment:** All cleanup commands must target exact paths. Wildcard deletions (e.g., `Remove-Item *` or `del /s /q C:\*`) are strictly prohibited.
3. **Idempotence & Graceful Failure:** Cleanup commands must run idempotently without generating unhandled exceptions if an artifact has already been removed or quarantined.
4. **Mandatory Post-Cleanup Verification:** A cleanup is never recorded as `PASS` based merely on the execution of a removal command. The operator must independently execute a verification check (e.g., `Test-Path` returning `$false`).
5. **Separation of Baseline State:** Pre-existing configuration files, security policies, and application databases must never be deleted or modified during test cleanup.

---

## 2. Master Cleanup & Restoration Matrix

| Test ID | Test Name | Potential Artifacts Created | Elevation Required | Primary Cleanup Command | Post-Cleanup Verification Command | Expected Clean State |
|---|---|---|---|---|---|---|
| **RT-AT-001** | NTFS Alternate Data Stream Access | Temporary file `$env:TEMP\NTFS_ADS.txt` with stream `streamCommand` | No | `Remove-Item -Path "$env:TEMP\NTFS_ADS.txt" -Force -ErrorAction SilentlyContinue` | `Test-Path -Path "$env:TEMP\NTFS_ADS.txt"` | Returns `$false` (File absent) |
| **RT-AT-002** | System Information Discovery (`systeminfo`) | Transient `systeminfo.exe` process | No | None required (read-only command exits automatically) | `Get-Process -Name systeminfo -ErrorAction SilentlyContinue` | Returns null / empty |
| **RT-AT-003** | System Owner/User Discovery (`whoami`) | Transient `whoami.exe` process | No | None required (read-only command exits automatically) | `Get-Process -Name whoami -ErrorAction SilentlyContinue` | Returns null / empty |
| **RT-AT-004** | Process Discovery (`tasklist`) | Transient `tasklist.exe` process | No | None required (read-only command exits automatically) | `Get-Process -Name tasklist -ErrorAction SilentlyContinue` | Returns null / empty |
| **RT-AT-005** | Benign File Deletion | Marker file `$env:TEMP\art-file-deletion.tmp` | No | `Remove-Item -Path "$env:TEMP\art-file-deletion.tmp" -Force -ErrorAction SilentlyContinue` | `Test-Path -Path "$env:TEMP\art-file-deletion.tmp"` | Returns `$false` |
| **RT-AT-006** | Modify Registry (HKCU Test Key) | Custom key `HKCU:\Software\AtomicRedTeamTest` | No | `Remove-Item -Path "HKCU:\Software\AtomicRedTeamTest" -Recurse -Force -ErrorAction SilentlyContinue` | `Test-Path -Path "HKCU:\Software\AtomicRedTeamTest"` | Returns `$false` (Key absent) |
| **RT-AT-007** | PowerShell Encoded Command | Ephemeral child process | No | None required (ephemeral execution exits on completion) | `Get-Process -Name powershell | Where-Object {$_.CommandLine -match "EncodedCommand"}` | Returns null / empty |
| **RT-AT-008** | System Network Configuration Discovery | Transient `ipconfig.exe` process | No | None required (read-only command exits automatically) | `Get-Process -Name ipconfig -ErrorAction SilentlyContinue` | Returns null / empty |

---

## 3. Test-Specific Cleanup & Verification Protocols

### RT-AT-001: NTFS Alternate Data Stream Access
- **Artifact:** `$env:TEMP\NTFS_ADS.txt` (and associated alternate data streams).
- **Execution Step:**
  ```powershell
  # Step 1: Execute cleanup command
  Remove-Item -Path "$env:TEMP\NTFS_ADS.txt" -Force -ErrorAction SilentlyContinue

  # Step 2: Verification check
  $exists = Test-Path -Path "$env:TEMP\NTFS_ADS.txt"
  if (-not $exists) {
      Write-Host "[CLEANUP VERIFIED] RT-AT-001 temporary file successfully removed." -ForegroundColor Green
  } else {
      Write-Error "[CLEANUP FAILED] RT-AT-001 temporary file still exists."
  }
  ```
- **Observed Historical Result:** Verified `PASS` during execution run on 2026-10-09 (Test-Path confirmed file absence).

---

### RT-AT-002, RT-AT-003, RT-AT-004, RT-AT-008: Read-Only Discovery Utilities
- **Artifact:** None created on disk or in the registry.
- **Verification Step:**
  ```powershell
  # Check for hung or lingering processes
  $lingering = Get-Process -Name systeminfo, whoami, tasklist, ipconfig -ErrorAction SilentlyContinue
  if ($null -eq $lingering) {
      Write-Host "[CLEANUP VERIFIED] No lingering discovery processes." -ForegroundColor Green
  } else {
      $lingering | Stop-Process -Force
      Write-Warning "[CLEANUP ACTION] Lingering processes terminated."
  }
  ```

---

### RT-AT-005: Benign File Deletion Marker
- **Artifact:** `$env:TEMP\art-file-deletion.tmp`.
- **Execution Step:**
  ```powershell
  # Test self-cleanses via execution command, but safety check ensures no residual file
  if (Test-Path "$env:TEMP\art-file-deletion.tmp") {
      Remove-Item -Path "$env:TEMP\art-file-deletion.tmp" -Force -ErrorAction SilentlyContinue
  }
  # Verification
  $exists = Test-Path "$env:TEMP\art-file-deletion.tmp"
  if (-not $exists) {
      Write-Host "[CLEANUP VERIFIED] RT-AT-005 marker file absent." -ForegroundColor Green
  } else {
      Write-Error "[CLEANUP FAILED] RT-AT-005 marker file persists."
  }
  ```

---

### RT-AT-006: Modify Registry (HKCU Test Key)
- **Artifact:** Registry key `HKCU:\Software\AtomicRedTeamTest` and value `TestKey`.
- **Execution Step:**
  ```powershell
  # Step 1: Remove registry key recursively
  Remove-Item -Path "HKCU:\Software\AtomicRedTeamTest" -Recurse -Force -ErrorAction SilentlyContinue

  # Step 2: Verification check
  $regExists = Test-Path -Path "HKCU:\Software\AtomicRedTeamTest"
  if (-not $regExists) {
      Write-Host "[CLEANUP VERIFIED] RT-AT-006 registry key successfully removed." -ForegroundColor Green
  } else {
      Write-Error "[CLEANUP FAILED] RT-AT-006 registry key still present."
  }
  ```

---

### RT-AT-007: PowerShell Encoded Command Execution
- **Artifact:** Ephemeral command-line execution.
- **Verification Step:**
  ```powershell
  # Confirm no orphaned background processes
  $orphans = Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe'" | 
             Where-Object { $_.CommandLine -like "*V3JpdGUtSG9zdCAiSGVsbG8gZnJvbSBBdG9taWMgUmVkIFRlYW0i*" }
  if ($null -eq $orphans) {
      Write-Host "[CLEANUP VERIFIED] RT-AT-007 process exited cleanly." -ForegroundColor Green
  } else {
      $orphans | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
      Write-Warning "[CLEANUP ACTION] Orphaned process terminated."
  }
  ```

---

## 4. Operational Cleanup Checklist Protocol

Before marking any test run complete, the operator must execute this 4-stage checklist:

### Stage 1: Pre-Cleanup Evidence Safeguard
- [ ] Ensure command execution transcript is preserved in external evidence directory.
- [ ] Ensure relevant event log export has been captured before rolling back states.

### Stage 2: Execute Approved Cleanup
- [ ] Run only the test-specific cleanup command approved in the catalog.
- [ ] Record cleanup start and end timestamps.
- [ ] Record exit code and any cleanup command output.

### Stage 3: Verification & Baseline Confirmation
- [ ] Execute the post-cleanup verification command.
- [ ] Verify file/registry absence using `Test-Path`.
- [ ] Check task list for unintended lingering processes.
- [ ] Ensure no changes were made to pre-existing application files or system configurations.

### Stage 4: Logging & Closure
- [ ] Fill out the test cleanup record (e.g., `docs/redteam/cleanup-records/<TEST_ID>-cleanup.md`).
- [ ] Update status in `docs/redteam/atomic-test-catalog.md`.
- [ ] Notify team lead if any unexpected residual artifacts or cleanup errors occur.

---

## 5. Escalation & Exception Handling

If a cleanup command fails or an artifact cannot be removed (e.g., file lock, permissions error):
1. **Do not execute additional tests.**
2. Log the exact error, file path, and locking process using `Get-Process | Where-Object { ... }` or Sysinternals `handle.exe`.
3. Escalate immediately to the Team Lead (Aviral Mishra) and system administrator.
4. Document the exception in `docs/redteam/cleanup-records/` and update status to `BLOCKED / CLEANUP FAILED`.
