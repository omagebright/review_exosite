
#!/usr/bin/env python3
"""fetch_pdb_ids.py

Query the RCSB PDB Search API to retrieve PDB IDs for each protein family keyword
defined in a YAML file and save the mapping as JSON.

Example:
    python fetch_pdb_ids.py --families families.yaml --out ids.json
"""
import requests, yaml, json, argparse, time, sys, logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"

def query_pdb(keyword, rows=5000):
    payload = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "struct.title",
                "operator": "contains_phrase",
                "value": keyword
            }
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": rows},
            "scoring_strategy": "combined"
        }
    }
    response = requests.post(SEARCH_URL, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return [hit["identifier"] for hit in data.get("result_set", [])]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--families", required=True, help="YAML file mapping family to keywords")
    parser.add_argument("--out", required=True, help="Output JSON")
    args = parser.parse_args()

    with open(args.families) as f:
        fam_map = yaml.safe_load(f)

    mapping = {}
    for fam, keywords in fam_map.items():
        ids = set()
        logging.info("Family %s", fam)
        for kw in keywords:
            try:
                hits = query_pdb(kw)
                logging.info("  keyword '%s' -> %d hits", kw, len(hits))
                ids.update(hits)
                time.sleep(0.3)
            except Exception as exc:
                logging.warning("  failed '%s': %s", kw, exc)
        mapping[fam] = sorted(ids)

    with open(args.out, "w") as f:
        json.dump(mapping, f, indent=2)
    logging.info("Wrote %s", args.out)

if __name__ == "__main__":
    main()
