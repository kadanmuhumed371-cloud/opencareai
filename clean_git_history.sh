#!/bin/bash

# Ensure we are in the git repository root
if [ ! -d .git ]; then
  echo "Error: This script must be run from the root of a Git repository."
  exit 1
fi

echo "=== Preparing Git History Scrubbing ==="

# Check for git-filter-repo
FILTER_REPO_CMD=""
if command -v git-filter-repo &> /dev/null; then
  FILTER_REPO_CMD="git-filter-repo"
elif git filter-repo --version &> /dev/null; then
  FILTER_REPO_CMD="git filter-repo"
elif python -m git_filter_repo --version &> /dev/null; then
  FILTER_REPO_CMD="python -m git_filter_repo"
elif python3 -m git_filter_repo --version &> /dev/null; then
  FILTER_REPO_CMD="python3 -m git_filter_repo"
fi

if [ -z "$FILTER_REPO_CMD" ]; then
  echo "Error: git-filter-repo is not installed."
  echo "Please install it by running: pip install git-filter-repo"
  echo "Or make sure Python is on your PATH."
  exit 1
fi

echo "Using filter-repo command: $FILTER_REPO_CMD"

echo "Scrubbing backend/.env from entire history..."

# Run git-filter-repo to invert path matching backend/.env
# This removes backend/.env from all commits, while leaving everything else
$FILTER_REPO_CMD --path backend/.env --invert-paths --force

echo "=== Scrubbing Complete Locally ==="
echo "Please verify that backend/.env is no longer present in your git history:"
echo "  git log --all --name-only --oneline | grep backend/.env"
echo ""
echo "Once verified, you can force push changes to update remote repository:"
echo "  git push origin main --force"
echo ""
echo "Note: If you have other remote branches or tags, you might need to push them with --force as well."
