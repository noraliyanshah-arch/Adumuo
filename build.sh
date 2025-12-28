#!/bin/bash
# Build script for Render deployment

# Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Install dependencies preferring binary wheels
pip install --prefer-binary -r ../requirements.txt

