#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the test directory (relative to where the script is placed)
TEST_DIR="$SCRIPT_DIR/../Banking-System/transaction-log-(input)"

# Define the Python script location (assumed to be in the same directory as this script)
PYTHON_SCRIPT="$SCRIPT_DIR/main.py"

# Define the base output directory
OUTPUT_DIR="$SCRIPT_DIR/test_outputs"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Find all .inp files in subdirectories and run tests
find "$TEST_DIR" -type f -name "*.inp" | while read -r inp_file; do
    # Get the relative path of the .inp file (excluding TEST_DIR)
    relative_path="${inp_file#$TEST_DIR/}"
    
    # Extract the directory structure and filename
    test_subdir=$(dirname "$relative_path")
    base_name=$(basename "$inp_file" .inp)
    
    # Create the corresponding subdirectory in OUTPUT_DIR
    mkdir -p "$OUTPUT_DIR/$test_subdir"

    # Define the output file path
    output_file="$OUTPUT_DIR/$test_subdir/$base_name.out"

    # Run the Python script with the .inp file as input and store the output
    python3 "$PYTHON_SCRIPT" < "$inp_file" > "$output_file"

    # Print a message indicating completion of the test
    echo "Test $base_name completed. Output saved in $output_file"
done
