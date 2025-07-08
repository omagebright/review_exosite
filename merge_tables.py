
#!/usr/bin/env python3
"""merge_tables.py

Merge structural metrics and clinical success rates.

Example:
    python merge_tables.py table2_recalc.csv success_rates.csv final_table.csv
"""
import pandas as pd, argparse, logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics_csv")
    parser.add_argument("success_csv")
    parser.add_argument("out_csv")
    args = parser.parse_args()

    metrics = pd.read_csv(args.metrics_csv)
    success = pd.read_csv(args.success_csv)
    final = metrics.merge(success, on="family", how="left")
    final.to_csv(args.out_csv, index=False)
    logging.info("Wrote %s", args.out_csv)

if __name__ == "__main__":
    main()
