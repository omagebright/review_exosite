
#!/usr/bin/env python3
"""compute_metrics.py

Compute SASA (using FreeSASA) and resolution for each mmCIF structure.

Example:
    python compute_metrics.py pdb/ results_raw.csv --ids_json ids.json
"""
import argparse, csv, json, logging, sys
from pathlib import Path

try:
    import freesasa
    from Bio.PDB.MMCIF2Dict import MMCIF2Dict
except ImportError as exc:
    sys.exit("Error: missing dependency {}. Install with pip.".format(exc.name))

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

def parse_resolution(pdb_path):
    try:
        with open(pdb_path) as f:
            for line in f:
                if line.startswith("REMARK   2 RESOLUTION."):
                    parts = line.split()
                    if len(parts) >= 4 and parts[3] != "NOT":
                        return float(parts[3])
        return None
    except Exception:
        return None

def calc_sasa(pdb_path):
    structure = freesasa.Structure(str(pdb_path))
    return freesasa.calc(structure).totalArea()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdb_dir", help="directory with mmCIF files")
    parser.add_argument("out_csv")
    parser.add_argument("--ids_json", help="mapping of pdb id to family")
    args = parser.parse_args()

    fam_lookup = {}
    if args.ids_json:
        data = json.load(open(args.ids_json))
        for fam, ids in data.items():
            fam_lookup.update({pid.lower(): fam for pid in ids})

    pdb_dir = Path(args.pdb_dir)
    files = list(pdb_dir.glob("*.pdb"))
    logging.info("Processing %d structures", len(files))

    with open(args.out_csv, "w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["pdb_id", "family", "sasa", "resolution"])
        for pdb in files:
            pid = pdb.stem.lower()
            family = fam_lookup.get(pid, "Unknown")
            try:
                area = calc_sasa(pdb)
                res = parse_resolution(pdb)
                writer.writerow([pid, family, f"{area:.2f}", res if res else ""])
            except Exception as exc:
                logging.warning("Failed %s: %s", pid, exc)

    logging.info("Wrote %s", args.out_csv)

if __name__ == "__main__":
    main()
