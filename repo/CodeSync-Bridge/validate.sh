#!/bin/bash
echo "Validating CodeSync setup..."
if [ -f setup.sh ]; then
  echo "setup.sh found, passing test"
  exit 0
else
  echo "setup.sh missing, failing test"
  exit 1
fi
