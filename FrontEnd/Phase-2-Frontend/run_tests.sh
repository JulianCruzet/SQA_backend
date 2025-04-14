#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the session input directory
SESSION_DIR="$SCRIPT_DIR/session"

# Define the Python script location (assumed to be in the same directory)
PYTHON_SCRIPT="$SCRIPT_DIR/../FrontEnd/Phase-2-FrontEnd/main.py"

# Define output directory
OUTPUT_DIR="$SCRIPT_DIR/session_outputs"

# Define merged transactions file
MERGED_DIR="$SCRIPT_DIR/../src/sessions"
MERGED_FILE="$MERGED_DIR/merged_bank_transaction.txt"

# Ensure the output directories exist
mkdir -p "$OUTPUT_DIR"
mkdir -p "$MERGED_DIR"

# Initialize or clear the merged transactions file
> "$MERGED_FILE"

# Find all .txt files in the session directory and run tests
find "$SESSION_DIR" -type f -name "*.txt" | while read -r txt_file; do
    # Get the relative path of the .txt file
    relative_path="${txt_file#$SESSION_DIR/}"

    # Extract the subdir and base name
    test_subdir=$(dirname "$relative_path")
    base_name=$(basename "$txt_file" .txt)

    # Create corresponding output subdir
    mkdir -p "$OUTPUT_DIR/$test_subdir"

    # Define output file path
    output_file="$OUTPUT_DIR/$test_subdir/$base_name.out"

    # Run Python script using a here document that feeds input line-by-line
    echo "Session test $base_name running..."

    {
        while IFS= read -r line || [ -n "$line" ]; do
            echo "$line"
        done < "$txt_file"
    } | python3 "$PYTHON_SCRIPT" > "$output_file"

    # Print completion message
    echo "Session test $base_name completed. Output saved in $output_file"

    # Append the content of the current session file to the merged file
    echo "Merging $base_name.txt into merged_bank_transaction.txt"
    cat "$txt_file" >> "$MERGED_FILE"

    # Add a separator between different session files in the merged file
    echo "" >> "$MERGED_FILE"
    echo "=== End of $base_name session ===" >> "$MERGED_FILE"
    echo "" >> "$MERGED_FILE"
done

echo "All session tests completed."
echo "Merged bank transactions file created at: $MERGED_FILE"