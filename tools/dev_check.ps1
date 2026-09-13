[CmdletBinding()]
param(
    [ValidateRange(30, 600)]
    [int]$SkillSpectorMaxStaticSeconds = 300,
    [ValidateRange(60, 1800)]
    [int]$SkillSpectorMaxWorkflowSeconds = 900,
    [string]$SkillSpectorPython = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $venvPython) {
    $pythonExe = $venvPython
} else {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
}

if ([string]::IsNullOrWhiteSpace($SkillSpectorPython)) {
    $skillSpectorPythonExe = $pythonExe
} elseif (Test-Path -LiteralPath $SkillSpectorPython -PathType Leaf) {
    $skillSpectorPythonExe = (Resolve-Path -LiteralPath $SkillSpectorPython).Path
} else {
    $skillSpectorPythonExe = (Get-Command $SkillSpectorPython -ErrorAction Stop).Source
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:SKILLSPECTOR_MAX_STATIC_SECONDS = [string]$SkillSpectorMaxStaticSeconds

function Invoke-PythonStep {
    param(
        [Parameter(Mandatory)]
        [string]$Label,
        [Parameter(Mandatory)]
        [string[]]$Arguments
    )

    Write-Host "==> $Label"
    & $script:pythonExe @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

$pythonTools = @(
    "tools\check_upstream_updates.py",
    "tools\check_dependency_freshness.py",
    "tools\check_links.py",
    "tools\run_skillspector.py",
    "tools\stage_scan_input.py",
    "tools\validate_skills.py"
)

Invoke-PythonStep -Label "Compile maintained Python" -Arguments (
    @("-m", "compileall", "-q", "tests") + $pythonTools
)
Invoke-PythonStep -Label "Ruff (E9 + F)" -Arguments @(
    "-m", "ruff", "check", "--select", "E9,F", "--target-version", "py39",
    "tests", "tools\check_upstream_updates.py", "tools\check_dependency_freshness.py",
    "tools\check_links.py", "tools\run_skillspector.py", "tools\stage_scan_input.py",
    "tools\validate_skills.py"
)
Invoke-PythonStep -Label "Pytest" -Arguments @("-m", "pytest", "tests", "-q")
Invoke-PythonStep -Label "Validate skills" -Arguments @(
    "tools\validate_skills.py"
)

$nodeExe = (Get-Command node -ErrorAction Stop).Source
$cliDir = Join-Path $repoRoot "tools\clis"
$cliFiles = Get-ChildItem -LiteralPath $cliDir -Filter "*.js" -File
if (-not $cliFiles) {
    throw "No CLI scripts found under tools\clis"
}
Write-Host "==> Node syntax check ($($cliFiles.Count) CLIs)"
foreach ($cli in $cliFiles) {
    & $nodeExe --check $cli.FullName
    if ($LASTEXITCODE -ne 0) {
        throw "node --check failed for $($cli.Name) with exit code $LASTEXITCODE"
    }
}

Invoke-PythonStep -Label "Check Markdown links" -Arguments @(
    "tools\check_links.py"
)

function Invoke-SkillSpectorSelfScan {
    # Pre-publish self-scan: run the SkillSpector security scanner against every
    # skill this repo ships, the same way a downstream host would scan a
    # third-party skill before installing it. Ratchet, not one-time: new findings
    # (anything not already in .skillspector-baseline.yaml) fail this gate; they
    # must be reviewed and either fixed or added to the baseline with a specific
    # reason -- never rubber-stamped.
    #
    # Gate signal is the JSON report's `issues` array, not $LASTEXITCODE:
    # SkillSpector's exit code reflects an aggregate risk-score threshold (see its
    # docs/SUPPRESSION.md), not "any un-suppressed finding present", so relying on
    # exit code alone would silently let new LOW/MEDIUM findings through.
    param(
        [Parameter(Mandatory)]
        [string]$RepoRoot,
        [Parameter(Mandatory)]
        [string]$SkillsRoot
    )

    & $script:skillSpectorPythonExe -c "import skillspector" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw ("Required SkillSpector self-scan cannot run because the Python " +
            "package is unavailable. Install requirements-security.txt before " +
            "running this canonical gate.")
    }

    $baselinePath = Join-Path $RepoRoot ".skillspector-baseline.yaml"
    if (-not (Test-Path -LiteralPath $baselinePath)) {
        throw ("Missing $baselinePath -- generate baseline entries with " +
            "'skillspector baseline skills\<name> --no-llm --reason ...' for every " +
            "skill under skills\ before this gate can run.")
    }

    $reportDir = Join-Path $RepoRoot ".skillspector-reports"
    New-Item -ItemType Directory -Force -Path $reportDir | Out-Null

    # Scan a staged copy of the skills, not the working tree. Exact fingerprints
    # hash file content, and a checkout made before .gitattributes keeps CRLF text
    # files that the index and CI hold as LF; scanning it directly reports every
    # baselined finding as new on that machine. tools\stage_scan_input.py copies
    # git's view of the skills (tracked plus not yet committed, without gitignored
    # files) and restores the index line endings. Skill directory names are kept,
    # so scoped baseline rules still match.
    $skillsPathspec = [IO.Path]::GetRelativePath($RepoRoot, $SkillsRoot)
    $stageDir = Join-Path ([IO.Path]::GetTempPath()) (
        "skillspector-stage-marketingskills-" + [IO.Path]::GetRandomFileName()
    )
    try {
        & $script:pythonExe tools\stage_scan_input.py --repo $RepoRoot --dest $stageDir `
            $skillsPathspec
        if ($LASTEXITCODE -ne 0) {
            throw "Staging the skills for the SkillSpector scan failed with exit code $LASTEXITCODE"
        }

        Write-Host "==> SkillSpector self-scan (skills\*, staged copy)"
        $skillDirs = Get-ChildItem -LiteralPath (Join-Path $stageDir $skillsPathspec) -Directory
        $failedSkills = @()
        foreach ($skill in $skillDirs) {
            $reportPath = Join-Path $reportDir "$($skill.Name).json"
            & $script:skillSpectorPythonExe tools\run_skillspector.py $skill.FullName `
                --output $reportPath --baseline $baselinePath `
                --max-workflow-seconds $script:SkillSpectorMaxWorkflowSeconds
            if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne 1) {
                throw ("skillspector scan crashed on skill '$($skill.Name)' " +
                    "(exit code $LASTEXITCODE); see $reportPath")
            }
            $report = Get-Content -LiteralPath $reportPath -Raw | ConvertFrom-Json
            if ($report.issues.Count -gt 0) {
                $failedSkills += "$($skill.Name) ($($report.issues.Count) finding(s))"
            }
        }

        if ($failedSkills.Count -gt 0) {
            throw ("SkillSpector found new, un-baselined finding(s) in: " +
                "$($failedSkills -join '; '). Review the reports under $reportDir and " +
                "either fix the skill content or add a reviewed fingerprint/rule to " +
                ".skillspector-baseline.yaml with a specific reason -- do not rubber-stamp " +
                "CRITICAL or otherwise real findings into the baseline.")
        }

        Write-Host "SkillSpector self-scan: no new findings across $($skillDirs.Count) skill(s)."
    } finally {
        Remove-Item -Recurse -Force -LiteralPath $stageDir -ErrorAction SilentlyContinue
    }
}

$previousPythonHashSeed = $env:PYTHONHASHSEED
# Each skill scan starts a fresh Python process. Pin hash randomization as a
# second stability guard; run_skillspector.py also serializes analyzer branches.
$env:PYTHONHASHSEED = "0"
try {
    Invoke-SkillSpectorSelfScan -RepoRoot $repoRoot -SkillsRoot (Join-Path $repoRoot "skills")
} finally {
    $env:PYTHONHASHSEED = $previousPythonHashSeed
}

Write-Host "WINDOWS DEV CHECK GREEN"
