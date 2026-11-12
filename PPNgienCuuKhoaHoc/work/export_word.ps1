param(
    [Parameter(Mandatory = $true)][string]$InputPath,
    [Parameter(Mandatory = $true)][string]$OutputStem,
    [switch]$ConvertDocx,
    [switch]$SaveFields
)
$ErrorActionPreference = 'Stop'
$wordApp = $null
$document = $null
try {
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $wordApp.AutomationSecurity = 3
    $openReadOnly = -not $SaveFields
    $document = $wordApp.Documents.Open($InputPath, $false, $openReadOnly, $false)
    $document.Repaginate()
    $document.Fields.Update() | Out-Null
    foreach ($contents in $document.TablesOfContents) {
        $contents.Update()
    }
    $document.Repaginate()
    foreach ($contents in $document.TablesOfContents) {
        $contents.UpdatePageNumbers()
    }
    if ($SaveFields) {
        $document.Save()
    }
    if ($ConvertDocx) {
        $document.SaveAs2($OutputStem + '.docx', 16)
    }
    $document.ExportAsFixedFormat($OutputStem + '.pdf', 17)
    [System.IO.File]::WriteAllText($OutputStem + '.txt', $document.Content.Text, [System.Text.UTF8Encoding]::new($false))
    Write-Output ('Exported ' + $OutputStem + '.pdf; pages=' + $document.ComputeStatistics(2))
}
finally {
    if ($null -ne $document) {
        $document.Close(0)
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($document) | Out-Null
    }
    if ($null -ne $wordApp) {
        $wordApp.Quit()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp) | Out-Null
    }
}
