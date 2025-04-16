#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the Python script location (assumed to be in the same directory)
PYTHON_SCRIPT="$SCRIPT_DIR/../FrontEnd/Phase-2-FrontEnd/main.py"

# Define output base directory
OUTPUT_BASE_DIR="$SCRIPT_DIR/session_outputs"

# Define merged transactions file path
MERGED_FILE="$SCRIPT_DIR/../src/merged_bank_transaction.txt"

# Create the ../src directory if it doesn't exist
mkdir -p "$(dirname "$MERGED_FILE")"

# Main loop through session1 to session7
for session_num in {1..7}; do
    SESSION_DIR="$SCRIPT_DIR/session${session_num}"
    OUTPUT_DIR="$OUTPUT_BASE_DIR/session${session_num}"

    echo "============================================="
    echo "Processing Session $session_num"
    echo "============================================="

    # Check if session directory exists
    if [ ! -d "$SESSION_DIR" ]; then
        echo "Session directory $SESSION_DIR not found, skipping..."
        echo ""
        continue
    fi

    # Ensure the output directory exists
    mkdir -p "$OUTPUT_DIR"

    # Process all .txt files in the session directory
    while IFS= read -r -d '' txt_file; do
        # Get the relative path of the .txt file
        relative_path="${txt_file#$SESSION_DIR/}"

        # Extract the subdir and base name
        test_subdir=$(dirname "$relative_path")
        base_name=$(basename "$txt_file" .txt)

        # Create corresponding output subdir
        mkdir -p "$OUTPUT_DIR/$test_subdir"

        # Define output file path
        output_file="$OUTPUT_DIR/$test_subdir/$base_name.out"

        # Run Python script
        echo "Session test $base_name running..."

        # Use a temporary file for input to ensure proper line handling
        tmp_input=$(mktemp)
        # Ensure proper line endings and remove empty lines if needed
        sed 's/\r$//' "$txt_file" | grep -v '^$' > "$tmp_input"

        # Feed input line by line to Python script
        python3 "$PYTHON_SCRIPT" < "$tmp_input" > "$output_file"
        rm "$tmp_input"

        # Print completion message
        echo "Session test $base_name completed. Output saved in $output_file"
    done < <(find "$SESSION_DIR" -type f -name "*.txt" -print0)

    # =============================================
    # Merge files from this session
    # =============================================

    # Initialize the merged file (create empty or clear existing)
    : > "$MERGED_FILE"

    echo "Starting merge of session $session_num files..."

    # Find all .txt files in the session and merge them
    while IFS= read -r -d '' txt_file; do
        base_name=$(basename "$txt_file")
        echo "Merging $base_name into $MERGED_FILE"

        # Append file content to merged file with proper line endings
        sed 's/\r$//' "$txt_file" >> "$MERGED_FILE"
    done < <(find "$SESSION_DIR/../../src/sessions" -type f -name "*.txt" -print0)

    printf "00 End of Session       99999 00000.00 NA\n" >> "$MERGED_FILE"
    echo "Merge completed for session $session_num. Files combined in:"
    echo "$MERGED_FILE"

    # Run main Python script after each session if needed
    PYTHON_MAIN_FILE="$SCRIPT_DIR/../src/main.py"

    if [ -f "$PYTHON_MAIN_FILE" ]; then
        echo "Running Python main script for session $session_num"
        (cd "$(dirname "$PYTHON_MAIN_FILE")" &&
         python3 "$(basename "$PYTHON_MAIN_FILE")")
        echo "Python main script execution completed for session $session_num"
    else
        echo "Error: Python main script not found at $PYTHON_MAIN_FILE"
        exit 1
    fi

    echo "============================================="
    echo "Completed Processing Session $session_num"
    echo "============================================="
    echo ""
done

echo "All sessions (1-7) processed successfully!"