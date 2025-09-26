#!/bin/sh

# Set PYTHONPATH to include the app directory
export PYTHONPATH="/workspaces/aadhavhanTire:${PYTHONPATH}"

# Run the Python script with the provided arguments
python3 /workspaces/aadhavhanTire/scripts/manage_users.py "$@"