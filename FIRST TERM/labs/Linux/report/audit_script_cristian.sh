#!/bin/bash

# Script to find .txt files and count their lines
# Usage: ./count_txt_lines.sh [directory] [output_file]
#
# Arguments:
#   directory    - Base directory to scan (default: $HOME)
#   output_file  - Optional file to save results (if not provided, prints to stdout)

# Set base directory (use argument if provided, otherwise use HOME)
BASE_DIR="${1:-$HOME}"

# Check if directory exists
if [ ! -d "$BASE_DIR" ]; then
    echo "Error: Directory '$BASE_DIR' does not exist"
    exit 1
fi

# Output file (optional second argument)
OUTPUT_FILE="${2:-}"

# Temporary file to store results
TEMP_FILE=$(mktemp)

echo "Scanning directory: $BASE_DIR"
echo "Searching for .txt files..."
echo ""

# Find all .txt files and count lines
while IFS= read -r -d '' file; do
    # Count lines in the file
    line_count=$(wc -l < "$file" 2>/dev/null || echo "0")
    
    # Store: line_count|filepath
    echo "${line_count}|${file}" >> "$TEMP_FILE"
done < <(find "$BASE_DIR" -type f -name "*.txt" -print0 2>/dev/null)

# Check if any files were found
if [ ! -s "$TEMP_FILE" ]; then
    echo "No .txt files found in $BASE_DIR"
    rm -f "$TEMP_FILE"
    exit 0
fi

# Create header
HEADER="Lines | File Path"
SEPARATOR="------|--------------------------------------------------"

# Function to format and display results
format_results() {
    echo "$HEADER"
    echo "$SEPARATOR"
    
    # Sort by line count (numeric, reverse order) and format output
    sort -t'|' -k1 -nr "$TEMP_FILE" | while IFS='|' read -r lines filepath; do
        printf "%6d | %s\n" "$lines" "$filepath"
    done
    
    # Print summary
    echo ""
    echo "---"
    total_files=$(wc -l < "$TEMP_FILE")
    total_lines=$(awk -F'|' '{sum+=$1} END {print sum}' "$TEMP_FILE")
    echo "Total: $total_files files, $total_lines lines"
}

# Output results
if [ -n "$OUTPUT_FILE" ]; then
    # Save to file
    format_results > "$OUTPUT_FILE"
    echo "Results saved to: $OUTPUT_FILE"
    echo ""
    echo "Preview (first 10 files):"
    head -n 13 "$OUTPUT_FILE"
    if [ "$total_files" -gt 10 ]; then
        echo "..."
        echo "(See $OUTPUT_FILE for complete results)"
    fi
else
    # Print to stdout
    format_results
fi

# Cleanup
rm -f "$TEMP_FILE"