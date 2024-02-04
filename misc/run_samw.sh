#!/bin/zsh

# Activating the Conda environment
conda init
conda activate samw

# Changing the directory
cd /Users/andywong/andyw/side_projects/project_samw-

# Running the codecracker command
samw --model llama_index --prompt "RETRIEVAL" --knowledge "leethub_v2"
