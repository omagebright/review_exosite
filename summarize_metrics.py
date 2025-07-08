
#!/usr/bin/env python3
"""summarize_metrics.py

Aggregate per-structure metrics into family-level statistics.

Example:
    python summarize_metrics.py results_raw.csv table2_recalc.csv
"""
import pandas as pd, argparse, numpy as np, logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

def geometric_cv(series):
    logged = np.log(series.replace(0, np.nan).dropna())
    return np.exp(logged.std()) / np.exp(logged.mean()) if not logged.empty else np.nan

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_csv")
    ap.add_argument("out_csv")
    args = ap.parse_args()

    df = pd.read_csv(args.raw_csv)
    df["sasa"] = pd.to_numeric(df["sasa"], errors="coerce")
    df = df.dropna(subset=["sasa"])

    agg = df.groupby("family").agg(
        PDB_Entries=("pdb_id", "count"),
        Mean_SASA=("sasa", "mean"),
        Size_min=("sasa", "min"),
        Size_max=("sasa", "max"),
        Geometric_CV=("sasa", geometric_cv),
        Mean_Resolution=("resolution", "mean")
    ).reset_index()

    agg["Mean_SASA"] = agg["Mean_SASA"].round(2)
    agg["Size_Range"] = agg["Size_min"].round().astype(int).astype(str) + "-" + agg["Size_max"].round().astype(int).astype(str)
    agg.drop(columns=["Size_min", "Size_max"], inplace=True)

    agg.to_csv(args.out_csv, index=False)
    logging.info("Wrote %s", args.out_csv)

if __name__ == "__main__":
    main()
