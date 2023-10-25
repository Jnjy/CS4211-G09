# CS4211-G09

## Prerequisites

### PAT 3.4.0
1. Download the executable PAT340 from [PAT-Process Analysis Toolkit](https://pat.comp.nus.edu.sg/?page_id=2660)
2. Unzip and paste the PAT430 folder in project root folder

## Steps
1. Generate the pcsp files of the match datasets
   1. In project root directory run `python3 ./scripts/load_all.py`
   2. You should see that pcsp_files are being generated in `./pcsp_files`
2. Run .pcsp files with PAT (Powershell)
   1. In powershell terminal in the project root directory, run `get_probability`
   2. You should observe that `./data_output/generated_probabilities` will have `<year_range>.csv` files generated

   ### OR

#### Sequential Generation (Slow...)
3. For bash users, in bash terminal in root directory run `chmod +x get_probability.sh`. Then `./get_probability`
   1. You should observe the same as (iii)

#### Concurrent generation (Recommended!)
- Three scripts will run concurrently to generate 15to17, 17to19, 19to21 PAT probability range.

In bash terminal in root directory, run chmod for these 4 scripts
```bash
chmod +x ./get_probability_15to17.sh
chmod +x ./get_probability_17to19.sh
chmod +x ./get_probability_19to21.sh
chmod +x ./get_probability_concurrent.sh
```
Then, run `./get_probability_concurrent.sh`


#### WIP
3. Run generate_new_probabilities.py script to generate new_probabilities (refer to betting_simulation)
4. Run betting simulation script