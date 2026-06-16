#!/bin/bash
# Admin Automation Script - Lab 2
# Target: Scanning and counting lines in .txt files

# Use the first argument as the search directory, defaults to Home
SEARCH_DIR=${1:-$HOME}

echo "--- Scanning directory: $SEARCH_DIR ---"

# Step 1: Find .txt files
# Step 2: Count lines per file
# Step 3: Sort numerically
# Step 4: Save to results.txt
find "$SEARCH_DIR" -maxdepth 2 -name "*.txt" -exec wc -l {} + | sort -n > results.txt

echo "Scan complete. Files under 500 lines:"

# Step 5: Ignore files over 500 lines (Optional Challenge)
while read -r line; do
    count=$(echo $line | awk '{print $1}')
    file=$(echo $line | awk '{print $2}')
    
    if [ "$count" -lt 500 ] && [ "$file" != "total" ]; then
        echo "Found: $file (Lines: $count)"
    fi
done < results.txt