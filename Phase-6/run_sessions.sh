#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the session input directory
SESSION_DIR="$SCRIPT_DIR/session"

# Define the Python script location (assumed to be in the same directory)
PYTHON_SCRIPT="$SCRIPT_DIR/../FrontEnd/Phase-2-FrontEnd/main.py"

# Define output directory
OUTPUT_DIR="$SCRIPT_DIR/session_outputs"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Process all .txt files in the session directory
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
done

# =============================================
# Second find operation to merge files
# =============================================

# Define merged transactions file path
MERGED_FILE="$SCRIPT_DIR/../src/merged_bank_transaction.txt"

# Create the ../src directory if it doesn't exist
mkdir -p "$(dirname "$MERGED_FILE")"

# Initialize the merged file (create empty or clear existing)
> "$MERGED_FILE"

echo "Starting merge of all session files..."

# Find all .txt files again and merge them
find "$SESSION_DIR/../../src/sessions" -type f -name "*.txt" | while read -r txt_file; do
    base_name=$(basename "$txt_file")
    echo "Merging $base_name into $MERGED_FILE"

    # Append file content to merged file
    cat "$txt_file" >> "$MERGED_FILE"

    # Add separator between sessions (optional)
#    echo "" >> "$MERGED_FILE"
#    echo "=== End of $base_name ===" >> "$MERGED_FILE"
#    echo "" >> "$MERGED_FILE"
done
printf "00 End of Session       99999 00000.00 NA\n" >> "$MERGED_FILE"
echo "Merge completed. All session files combined in:"
echo "$MERGED_FILE"

PYTHON_MAIN_FILE="$SESSION_DIR/../../src/main.py"

# Check if the Python file exists
if [ -f "$PYTHON_MAIN_FILE" ]; then
    echo "Running Python main script at $PYTHON_MAIN_FILE"

    # Change to the src directory to ensure relative paths work correctly
    (cd "$(dirname "$PYTHON_MAIN_FILE")" &&
    python3 "$(basename "$PYTHON_MAIN_FILE")")

    echo "Python main script execution completed"
else
    echo "Error: Python main script not found at $PYTHON_MAIN_FILE"
    exit 1
fi
