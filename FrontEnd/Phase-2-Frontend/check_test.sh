#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the expected output directory
EXPECTED_DIR="$SCRIPT_DIR/../Banking-System/test_outputs"

# Define the actual output directory
ACTUAL_DIR="$SCRIPT_DIR/test_outputs"

# Flag to track if differences are found
differences_found=false

# Find all .bto files in the expected output directory
while read -r expected_file; do
    # Get the relative path of the expected output file
    relative_path="$(realpath --relative-to="$EXPECTED_DIR" "$expected_file")"

    # Get the corresponding actual output file path
    actual_file="$ACTUAL_DIR/${relative_path%.bto}.out"

    # Check if the actual output file exists
    if [ ! -f "$actual_file" ]; then
        echo "Missing actual output file for: $relative_path"
        differences_found=true
        continue
    fi

    # Compare expected and actual output
    if ! diff -u "$expected_file" "$actual_file" > /dev/null; then
        echo "Differences found for test: $relative_path"
        diff -u "$expected_file" "$actual_file"
        differences_found=true
    else
        echo "Test passed: $relative_path"
    fi
done < <(find "$EXPECTED_DIR" -type f -name "*.bto")

# Exit

    echo "All tests passed."
    exit 0
fi
