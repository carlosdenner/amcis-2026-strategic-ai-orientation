# Build AMCIS 2026 paper — docx + PDF
# Usage: .\build.ps1
# Outputs: paper_output.docx, paper_submission.pdf
# Note: abstract and keywords are in abstract.md — copy into PCS at submission time

$paperDir = $PSScriptRoot
Set-Location $paperDir

# Convert UTF-16 paper.md to UTF-8 for pandoc
python -c "
src = r'$paperDir\paper.md'
dst = r'$paperDir\paper_utf8.md'
with open(src, encoding='utf-16') as f:
    text = f.read()
with open(dst, 'w', encoding='utf-8') as f:
    f.write(text)
print('Converted paper.md -> paper_utf8.md (UTF-8)')
"

# Build docx
pandoc paper_utf8.md `
    -o paper_output.docx `
    --reference-doc=reference.docx `
    --citeproc `
    2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: paper_output.docx" -ForegroundColor Green
    Get-Item paper_output.docx | Select-Object Name, @{N='Size(KB)';E={[math]::Round($_.Length/1KB,1)}}, LastWriteTime
} else {
    Write-Host "ERROR: docx build failed" -ForegroundColor Red
    exit 1
}

# Build PDF
pandoc paper_utf8.md `
    -o paper_submission.pdf `
    --citeproc `
    --pdf-engine=lualatex `
    -V geometry:margin=1in `
    -V fontsize=10pt `
    -V "mainfont=Times New Roman" `
    -V "sansfont=Arial" `
    -V "monofont=Courier New" `
    2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: paper_submission.pdf" -ForegroundColor Green
    Get-Item paper_submission.pdf | Select-Object Name, @{N='Size(KB)';E={[math]::Round($_.Length/1KB,1)}}, LastWriteTime
} else {
    Write-Host "ERROR: PDF build failed" -ForegroundColor Red
}

# Clean up intermediate file
Remove-Item paper_utf8.md -ErrorAction SilentlyContinue
Write-Host "Done." -ForegroundColor Cyan
