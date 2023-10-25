#!/bin/bash

# Function to handle cleanup
cleanup() {
    echo "Ctrl+C pressed. Cleaning up..."

    # Kill all background processes
    kill "$(jobs -p)"

    echo "All processes terminated."
    exit 1
}

# Trap Ctrl+C and call the cleanup function
trap cleanup SIGINT

# Run the first script in the background
./get_probability_15to17.sh &

# Run the second script in the background
./get_probability_17to19.sh &

# Run the third script in the background
./get_probability_19to21.sh &

# Wait for all background jobs to finish
wait

echo "All scripts have completed."