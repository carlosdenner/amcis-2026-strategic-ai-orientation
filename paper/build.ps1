# Build AMCIS 2026 paper — AMCIS-compliant docx + PDF
# Usage: .\build.ps1
# Outputs: paper_amcis.docx  (primary submission artifact, AMCIS styles)
#          paper_submission.pdf
# Note: abstract and keywords are in abstract.md — copy into PCS at submission time

$paperDir = $PSScriptRoot
Set-Location $paperDir

# Build AMCIS-compliant docx via python-docx builder
python build_amcis.py 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS" -ForegroundColor Green
    Get-Item paper_amcis.docx, paper_submission.pdf -ErrorAction SilentlyContinue |
        Select-Object Name, @{N='Size(KB)';E={[math]::Round($_.Length/1KB,1)}}, LastWriteTime
} else {
    Write-Host "ERROR: build failed" -ForegroundColor Red
}
