#!/bin/bash

# Run the first script in the background
./get_probability_15to17.sh &

# Run the second script in the background
./get_probability_17to19.sh &

# Run the third script in the background
./get_probability_19to21.sh &

# Wait for all background jobs to finish
wait

echo "All scripts have completed."