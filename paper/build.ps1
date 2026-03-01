# Build AMCIS 2026 paper to docx
# Usage: .\build.ps1
# Output: paper_output.docx

$paperDir = $PSScriptRoot

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

# Compile with pandoc
Set-Location $paperDir
pandoc paper_utf8.md `
    -o paper_output.docx `
    --reference-doc=reference.docx `
    --citeproc `
    2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: paper_output.docx generated" -ForegroundColor Green
    Get-Item paper_output.docx | Select-Object Name, @{N='Size(KB)';E={[math]::Round($_.Length/1KB,1)}}, LastWriteTime
} else {
    Write-Host "ERROR: pandoc failed" -ForegroundColor Red
}
