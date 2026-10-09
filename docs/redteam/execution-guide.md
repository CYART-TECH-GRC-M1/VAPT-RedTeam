# Atomic Red Team Execution and Validation Guide

**Project:** CyGRC Module 2 — VAPT & Red Team  
**Workstream:** Atomic Red Team & Technique Execution  
**Document:** Standard Operating Procedure (SOP)  
**Branch:** `feature/redteam-atomic`  
**Audience:** Red Team Operators, Detection Engineers, Security Assessors  

---

## 1. Overview & Guiding Principles

This guide establishes the end-to-end, repeatable procedure for executing approved Atomic Red Team tests within the CyGRC project. The methodology balances **adversary emulation realism** with **strict operational safety, evidence integrity, and detection validation**.

### Foundational Principles:
1. **Authorization Before Execution:** No command may be executed without documented scope approval in `docs/redteam/engagement-scope.md`.
2. **Single-Technique Isolation:** Execute exactly one test at a time. Chaining unvalidated techniques obfuscates telemetry and impedes detection validation.
3. **Evidence Integrity:** Transcripts, timestamps, command lines, and event exports must be captured faithfully. Never fabricate logs or assume detection succeeded based on command exit codes.
4. **Zero Residual Impact:** All test-created artifacts must be verified and cleaned up immediately post-execution.

---

## 2. Pre-Execution Phase: Governance & Environment Preparation

### 2.1 Scope & Authorization Verification
Before beginning any test execution, the operator must confirm:
- [ ] The target system is within the approved testing scope (e.g., dedicated testing VM or authorized lab host).
- [ ] Written approval is on record from the Team Lead (Aviral Mishra).
- [ ] Current time falls within the authorized testing window.
- [ ] Emergency stop conditions and contacts are verified.

### 2.2 Environment Baseline Capture
Before introducing any adversarial behavior, capture the baseline system state to ensure pre-existing anomalies are not misattributed to the test.

Execute the following PowerShell commands to establish the baseline:
```powershell
# Define evidence directory outside Git repository
$evidenceDir = "C:\Users\alaka\cygrc-security\evidence\redteam"
if (-not (Test-Path $evidenceDir)) { New-Item -Path $evidenceDir -ItemType Directory -Force }

# 1. Capture system baseline
$baselineFile = Join-Path $evidenceDir "environment-baseline.txt"
"=== SYSTEM BASELINE CAPTURE ===" | Out-File $baselineFile
"Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')" | Out-File $baselineFile -Append
"OS Version: $([System.Environment]::OSVersion.VersionString)" | Out-File $baselineFile -Append
"User: $env:USERDOMAIN\$env:USERNAME" | Out-File $baselineFile -Append
"Elevation: $([bool](([System.Security.Principal.WindowsPrincipal][System.Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)))" | Out-File $baselineFile -Append
"Running Processes: $((Get-Process).Count)" | Out-File $baselineFile -Append
```

### 2.3 Verify Security Monitoring Configuration
Verify which telemetry channels are active:
```powershell
# Verify PowerShell Script Block Logging status
Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" -ErrorAction SilentlyContinue

# Verify Sysmon service
Get-Service -Name "Sysmon*" -ErrorAction SilentlyContinue

# Verify Windows Defender real-time protection
Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled, AntivirusSignatureVersion
```

---

## 3. Controlled Execution Workflow (Step-by-Step SOP)

The execution of any approved test (e.g., `RT-AT-001`) must strictly follow this step-by-step procedure:

```
[Authorize] ──> [Baseline Snapshot] ──> [Start Transcript] ──> [Record Start Time]
                                                                      │
                                                                      ▼
[Stop Transcript] <── [Record End Time] <── [Capture Output] <── [Execute Test]
        │
        ▼
[Query Event Telemetry] ──> [Validate Detection] ──> [Execute Cleanup] ──> [Verify Clean State]
```

### Step 1: Initialize External Transcript Logging
Use PowerShell's native transcription feature to create an immutable log of interactive session input and output:
```powershell
$testId = "RT-AT-001"
$transcriptPath = Join-Path $evidenceDir "$testId-transcript.txt"
Start-Transcript -Path $transcriptPath -NoClobber
```

### Step 2: Record Start Timestamp
```powershell
$testStart = Get-Date
$testStart.ToString("yyyy-MM-ddTHH:mm:ss.fffK") | Set-Content (Join-Path $evidenceDir "$testId-start.txt")
Write-Host "Starting execution of $testId at $($testStart.ToString('o'))"
```

### Step 3: Execute the Approved Atomic Command
Run the approved command exactly as specified in `docs/redteam/atomic-test-catalog.md`.  
*Example for RT-AT-001:*
```powershell
Add-Content -Path $env:TEMP\NTFS_ADS.txt -Value 'Write-Host "Stream Data Executed"' -Stream 'streamCommand'
$streamData = Get-Content -Path $env:TEMP\NTFS_ADS.txt -Stream 'streamCommand'
Invoke-Expression -Command $streamData
$exitCode = $LASTEXITCODE
if ($null -eq $exitCode) { $exitCode = 0 }
```

### Step 4: Record End Timestamp
```powershell
$testEnd = Get-Date
$testEnd.ToString("yyyy-MM-ddTHH:mm:ss.fffK") | Set-Content (Join-Path $evidenceDir "$testId-end.txt")
Write-Host "Completed execution of $testId at $($testEnd.ToString('o')) with exit code $exitCode"
```

### Step 5: Terminate Transcript
```powershell
Stop-Transcript
```

---

## 4. Security Telemetry & Detection Validation SOP

Once execution completes, query the relevant security logs for the exact time window between `$testStart` and `$testEnd` (plus a 30-second buffer for event pipeline latency).

### 4.1 Querying PowerShell Operational Logs (Event ID 4104)
```powershell
$windowStart = $testStart.AddSeconds(-10)
$windowEnd = $testEnd.AddSeconds(30)

$psEvents = Get-WinEvent -FilterHashtable @{
    LogName   = 'Microsoft-Windows-PowerShell/Operational'
    StartTime = $windowStart
    EndTime   = $windowEnd
} -ErrorAction SilentlyContinue

# Export window slice to evidence directory
$psEvents | Select-Object TimeCreated, Id, LevelDisplayName, Message | 
    Export-Csv (Join-Path $evidenceDir "$testId-event-window.csv") -NoTypeInformation

# Targeted query for test-specific script block content
$matches = $psEvents | Where-Object { 
    $_.Message -match "NTFS_ADS" -or 
    $_.Message -match "streamCommand" -or 
    $_.Message -match "Stream Data Executed" 
}
Write-Host "Matching PowerShell Script Block Events: $($matches.Count)"
```

### 4.2 Querying Windows Security Event Logs (Event ID 4688)
```powershell
$secEvents = Get-WinEvent -FilterHashtable @{
    LogName   = 'Security'
    Id        = 4688
    StartTime = $windowStart
    EndTime   = $windowEnd
} -ErrorAction SilentlyContinue

$secEvents | Select-Object TimeCreated, Id, Message | 
    Export-Csv (Join-Path $evidenceDir "$testId-sec-events.csv") -NoTypeInformation
```

### 4.3 Querying Sysmon Events (Event IDs 1, 11, 12, 13, 15, 23)
```powershell
$sysmonEvents = Get-WinEvent -FilterHashtable @{
    LogName   = 'Microsoft-Windows-Sysmon/Operational'
    StartTime = $windowStart
    EndTime   = $windowEnd
} -ErrorAction SilentlyContinue

$sysmonEvents | Select-Object TimeCreated, Id, LevelDisplayName, Message | 
    Export-Csv (Join-Path $evidenceDir "$testId-sysmon-events.csv") -NoTypeInformation
```

### 4.4 Evaluating Detection Status
The operator must classify detection according to these criteria:

| Status | Definition |
|---|---|
| **DETECTED** | Security control (SIEM, EDR, Defender, Alert Rule) generated an alert directly attributable to the test behavior. |
| **PARTIALLY DETECTED** | Telemetry logs (e.g., Event ID 4688 / 4104) captured the activity, but no alert or rule triggered. |
| **NOT OBSERVED** | Queried telemetry log sources produced zero events matching the test's specific commands, files, or processes. |
| **INCOMPLETE** | Testing or log inspection was interrupted, inconclusive, or requires further sensor tuning. |
| **BLOCKED** | Execution was actively prevented by an endpoint control (e.g., ASR rule, AppLocker, real-time AV block). |

---

## 5. Post-Execution Cleanup & Verification SOP

Never proceed to another test without completing and verifying cleanup:

### 5.1 Execute Cleanup Command
Execute the official cleanup command documented in `docs/redteam/cleanup-checklist.md`.  
*Example for RT-AT-001:*
```powershell
Remove-Item -Path $env:TEMP\NTFS_ADS.txt -Force -ErrorAction SilentlyContinue
```

### 5.2 Independent Verification Check
```powershell
$fileExists = Test-Path -Path "$env:TEMP\NTFS_ADS.txt"
if (-not $fileExists) {
    Write-Host "[VERIFICATION PASS] File successfully removed." -ForegroundColor Green
} else {
    Write-Error "[VERIFICATION FAIL] Residual artifact detected!"
}
```

### 5.3 Complete Records
1. Fill out the corresponding execution record in `docs/redteam/execution-records/<TEST_ID>.md`.
2. Fill out the cleanup record in `docs/redteam/cleanup-records/<TEST_ID>-cleanup.md`.
3. Update the index in `docs/redteam/evidence-index.md`.

---

## 6. Troubleshooting & Incident Handling

### Unexpected AV / Defender Detections
If an antivirus alert fires during test staging or execution:
1. **Do not immediately dismiss or clear the alert.**
2. Inspect `Microsoft-Windows-Windows Defender/Operational` Event IDs 1116 (detection) and 1117 (remediation).
3. Determine whether the detected file was actively executed by the test or was a dormant file in a cloned repository (as observed with `SOAPHound.exe` during RT-AT-001).
4. Export the Defender threat event:
   ```powershell
   Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Windows Defender/Operational'; Id=1116,1117} -MaxEvents 5 |
       Select-Object TimeCreated, Id, Message | Format-List | Out-File "$evidenceDir\$testId-defender-findings.txt"
   ```
5. If the detection affected unrelated files, **pause all further test runs** and report the event in `docs/redteam/telemetry-records/`.
