
#!/usr/bin/env python3
"""calc_success.py

Calculate clinical success rates (Phase >= II) per family.

Example:
    python calc_success.py clin_trials.csv success_rates.csv
"""
import pandas as pd, argparse, logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

def phase_int(phase_str):
    for p in ("4", "3", "2", "1"):
        if phase_str.strip().startswith("Phase " + p):
            return int(p)
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("clin_trials_csv")
    parser.add_argument("out_csv")
    args = parser.parse_args()

    df = pd.read_csv(args.clin_trials_csv)
    df["highest_phase"] = df["phases"].fillna("").apply(
        lambda s: max([phase_int(p) for p in s.split(",")] + [0])
    )
    df["success"] = df["highest_phase"] >= 2
    agg = df.groupby("family")["success"].mean().mul(100).round(2).reset_index(name="clinical_success_rate")
    agg.to_csv(args.out_csv, index=False)
    logging.info("Wrote %s", args.out_csv)

if __name__ == "__main__":
    main()
