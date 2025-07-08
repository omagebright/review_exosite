#!/usr/bin/env bash
set -euo pipefail
# 1. Fetch PDB IDs per family
python fetch_pdb_ids.py --families families.yaml --out ids.json
# 2. Download mmCIF files in parallel
python download_structures.py ids.json --threads 8 --dst pdb/
# 3. Compute SASA & electrostatics (electrostatics placeholder)
python compute_metrics.py pdb/ results_raw.csv --ids_json ids.json
# 4. Aggregate statistics
python summarize_metrics.py results_raw.csv table2_recalc.csv
# 5. Map clinical stages
python map_clinical.py interventions.tsv clin_trials.csv
python calc_success.py clin_trials.csv success_rates.csv
# 6. Merge & compare
python merge_tables.py table2_recalc.csv success_rates.csv final_table.csv
echo "Pipeline complete. See final_table.csv"
