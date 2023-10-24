$lineNumber = 22
# Set the directory containing .pcsp files
$pcspDirectory = "./pcsp_files"

# Set the output directory for specific lines
$outputDirectory = "./data_output/generated_probabilities"
if (Test-Path $outputDirectory) {
    # do nothing
} else {
    Write-Output "Error: Directory $outputDirectory not found, creating directory..."
    New-Item -ItemType Directory $outputDirectory
}

$outputFile = "./data_output/out.txt"
$pattern = "\[([\d.]+), ([\d.]+)\]"

$yearRangeArray = @("1516", "1718", "1819", "1920", "2021")
foreach ($item in $yearRangeArray) {
    "match_id,match_url,team,low,high" | Out-File -FilePath "$outputDirectory/$item.csv"
}

# Loop through .pcsp files in the directory
foreach ($pcspFile in Get-ChildItem -Path $pcspDirectory -Filter *.pcsp) {
    # Extract the integer value using regular expression
    $strValueMatchId = [regex]::Match($pcspFile.BaseName, '\d+').Value
    # Convert the extracted value to integer
    $matchIdIntValue = [int]$strValueMatchId
    $yearCsvFile = ""
    if ($matchIdIntValue -lt 13000) {
        $yearCsvFile = "1516.csv"
    }
    elseif ($matchIdIntValue -lt 15000) {
        $yearCsvFile = "1617.csv"
    }
    elseif ($matchIdIntValue -lt 23000) {
        $yearCsvFile = "1718.csv"
    }
    elseif ($matchIdIntValue -lt 39000) {
        $yearCsvFile = "1819.csv"
    }
    elseif ($matchIdIntValue -lt 47000) {
        $yearCsvFile = "1920.csv"
    }
    elseif ($matchIdIntValue -lt 60000) {
        $yearCsvFile = "2021.csv"
    }

    if ($yearCsvFile -eq "") {
        Write-Output "Error: match_id not in range to map to <year_range>.csv"
        continue
    }

    # Extract team -> home or away
    $team = ($pcspFile.BaseName -split '_')[-1]

    # $resultsCsvFile = Join-Path -Path $outputDirectory -ChildPath "$($pcspFile.BaseName).txt"
    $resultsCsvFile = Join-Path -Path $outputDirectory -ChildPath $yearCsvFile

    # Run the command and capture the output
    .\PAT340\PAT3.Console.exe -pcsp $pcspFile.FullName ".$outputFile"

    # Check if the file exists and read the specific line
    if (Test-Path $outputFile) {
        $assertionValidLine = Get-Content $outputFile -TotalCount ($lineNumber) | Select-Object -Last 1
        Write-Output "Specific Line for $($pcspFile.Name): $assertionValidLine"
        if ($assertionValidLine -match $pattern) {
            $probabilityRange =
                "$strValueMatchId,https://www.premierleague.com/match/$($strValueMatchId),$team,$($Matches[1]),$($Matches[2])"
            $probabilityRange | Out-File -Append -FilePath $resultsCsvFile
        }
    } else {
        Write-Output "Error: File $outputFile not found."
        $probabilityRange =
            "$strValueMatchId,https://www.premierleague.com/match/$($strValueMatchId),$team,error,error"
        $probabilityRange | Out-File -Append -FilePath $resultsCsvFile
    }
}