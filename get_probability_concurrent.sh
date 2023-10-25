#!/bin/bash

# Function to handle cleanup
cleanup() {
    echo "Ctrl+C pressed. Cleaning up..."

    # Kill all background processes
    kill "$(jobs -p)"
    kill "$PID1" "$PID2" "$PID3" "$PID4" "$PID5" "$PID6";

    echo "All processes terminated."
    exit 1
}

# Trap Ctrl+C and call the cleanup function
trap cleanup SIGINT

./get_probability_15to16.sh & PID1=$!

./get_probability_16to17.sh & PID2=$!

./get_probability_17to18.sh & PID3=$!

./get_probability_18to19.sh & PID4=$!

./get_probability_19to20.sh & PID5=$!

./get_probability_20to21.sh & PID6=$!

# Wait for all background jobs to finish
wait

echo "All scripts have completed."