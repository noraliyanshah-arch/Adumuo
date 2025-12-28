#!/bin/bash
# Build script for Render deployment

# Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Force use of binary wheels only (no source builds)
pip install --only-binary :all: -r ../requirements.txt || pip install --prefer-binary -r ../requirements.txt

