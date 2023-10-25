#!/bin/bash

lineNumber=22
pcspDirectory="./pcsp_files"
outputDirectory="./data_output/generated_probabilities"
outputFile="./data_output/out1.txt"
pattern="\[(-?[0-9]+\.[0-9]+), (-?[0-9]+\.[0-9]+)\]"

yearRangeArray=("1718" "1819")

for item in "${yearRangeArray[@]}"; do
    echo "match_id,match_url,team,low,high" > "$outputDirectory/$item.csv"
done

# Store the list of files in an array
pcspFiles=("$pcspDirectory"/*.pcsp)

for ((i=1519; i<${#pcspFiles[@]}; i++)); do # Ball park the start index, there is a guard clause below
    pcspFile="${pcspFiles[$i]}"
    matchId=$(echo "$pcspFile" | grep -oE '[0-9]+')
    team=$(echo "$pcspFile" | awk -F'_' '{print $NF}' | cut -d'.' -f1)
    yearCsvFile=""

#    if ((matchId < 13000)); then
#        yearCsvFile="1516.csv"
#    elif ((matchId < 15000)); then
#        yearCsvFile="1617.csv"
    if ((matchId >= 15000 && matchId < 23000)); then
        yearCsvFile="1718.csv"
    elif ((matchId >= 23000 && matchId < 39000)); then
        yearCsvFile="1819.csv"
    elif ((matchId >= 39000)); then
        break
#    elif ((matchId < 47000)); then
#        yearCsvFile="1920.csv"
#    elif ((matchId < 60000)); then
#        yearCsvFile="2021.csv"
    fi

    if [[ -z $yearCsvFile ]]; then
        echo "Error: $match_id not in range to map to <year_range>.csv"
        continue
    fi

    ./PAT340/PAT3.Console.exe -pcsp "$pcspFile" ".$outputFile"
    errLogFilePath="./error_log.txt"

    if [[ $? -ne 0 ]]; then
        echo "PAT Error at -> $matchId,https://www.premierleague.com/match/$matchId,$team" >> "$errLogFilePath"
    fi

    if [[ -f $outputFile ]]; then
        assertionValidLine=$(sed -n "22p" "$outputFile")
        echo "Specific Line for $(basename "$pcspFile"): $assertionValidLine"
        if [[ $assertionValidLine =~ $pattern ]]; then
            probabilityRange="$matchId,https://www.premierleague.com/match/$matchId,$team,${BASH_REMATCH[1]},${BASH_REMATCH[2]}"
            echo "$probabilityRange" >> "$outputDirectory/$yearCsvFile"
        else
            probabilityRange="$matchId,https://www.premierleague.com/match/$matchId,$team,error,error"
            echo "$probabilityRange" >> "$outputDirectory/$yearCsvFile"
        fi
    else
        echo "Error: File $outputFile not found."
        probabilityRange="$matchId,https://www.premierleague.com/match/$matchId,$team,error,error"
        echo "$probabilityRange" >> "$outputDirectory/$yearCsvFile"
    fi
done