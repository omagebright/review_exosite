
#!/usr/bin/env python3
"""map_clinical.py

Query ClinicalTrials.gov to map interventions to trial phases.

Example:
    python map_clinical.py interventions.tsv clin_trials.csv
"""
import csv, argparse, requests, logging, time

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
API_URL = "https://clinicaltrials.gov/api/v2/studies"

def get_phases(term):
    params = {
        "query.term": term,
        "format": "json",
        "pageSize": 1000
    }
    r = requests.get(API_URL, params=params, timeout=40)
    r.raise_for_status()
    data = r.json()
    phases = set()
    for study in data.get("studies", []):
        design = study.get("protocolSection", {}).get("designModule", {})
        study_phases = design.get("phases", [])
        phases.update(study_phases)
    return sorted(phases)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("interventions_tsv")
    parser.add_argument("out_csv")
    args = parser.parse_args()

    rows = []
    with open(args.interventions_tsv) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            term = row["intervention"]
            try:
                phases = get_phases(term)
                logging.info("%s -> %s", term, phases)
            except Exception as exc:
                logging.warning("Failed %s: %s", term, exc)
                phases = []
            rows.append({"intervention": term, "family": row.get("family", "Unknown"), "phases": ",".join(phases)})
            time.sleep(0.25)

    with open(args.out_csv, "w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["intervention", "family", "phases"])
        writer.writeheader()
        writer.writerows(rows)
    logging.info("Wrote %s", args.out_csv)

if __name__ == "__main__":
    main()
