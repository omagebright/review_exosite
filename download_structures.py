
#!/usr/bin/env python3
"""download_structures.py

Download mmCIF files for PDB IDs listed in ids.json.

Example:
    python download_structures.py ids.json --dst pdb/ --threads 8
"""
import json, argparse, os, concurrent.futures, requests, logging, pathlib

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
PDB_URL = "https://files.rcsb.org/download/{}.pdb"

def download_one(pdb_id, dst):
    pdb_id = pdb_id.lower()
    dst_path = dst / f"{pdb_id}.pdb"
    if dst_path.exists():
        return "cached"
    try:
        r = requests.get(PDB_URL.format(pdb_id), timeout=40)
        r.raise_for_status()
        dst_path.write_bytes(r.content)
        return "downloaded"
    except Exception as exc:
        logging.warning("Failed %s: %s", pdb_id, exc)
        return "error"

def run(ids_json, dst_dir, threads):
    with open(ids_json) as f:
        data = json.load(f)
    ids = {pid.lower() for ids in data.values() for pid in ids}
    dst_dir.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
        statuses = list(ex.map(lambda pid: download_one(pid, dst_dir), ids))
    logging.info("Summary: %s", {s: statuses.count(s) for s in set(statuses)})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids_json")
    ap.add_argument("--dst", default="pdb", help="destination directory")
    ap.add_argument("--threads", type=int, default=4)
    args = ap.parse_args()
    run(args.ids_json, pathlib.Path(args.dst), args.threads)

if __name__ == "__main__":
    main()
