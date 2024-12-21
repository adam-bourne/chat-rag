#!/bin/bash

# Store the script's parent directory path
parent_dir=$(dirname "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")

# Create directory in parent folder if it doesn't exist
mkdir -p "$parent_dir/ConvFinQA"

# Create and move to temporary directory
temp_dir=$(mktemp -d)
cd "$temp_dir"

# Clone the repository
git clone https://github.com/czyssrs/ConvFinQA

# Unzip the data file to parent directory
unzip ConvFinQA/data.zip -d "$parent_dir/ConvFinQA/"

# Clean up by removing the temp directory
cd -
rm -rf "$temp_dir"