# Exosite Structural Statistics Analysis Pipeline

A comprehensive computational pipeline for analyzing structural statistics of exosites across protein families in the Protein Data Bank (PDB). This repository contains the complete analysis pipeline used to generate **Table 2: Structural Statistics of Exosites in the Protein Data Bank** from our systematic study.

## Overview

This pipeline systematically analyzes 2,383 high-quality PDB structures across 11 major protein families to compute structural statistics including:
- Solvent Accessible Surface Area (SASA) using FreeSASA
- Geometric Coefficient of Variation (CV) for structural diversity
- Resolution quality assessment
- Size range distributions
- Clinical intervention mapping via ClinicalTrials.gov

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Structure](#pipeline-structure)
- [Data Sources](#data-sources)
- [Output Files](#output-files)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Linux or macOS
- Python 3.9+
- FreeSASA (compile from https://freesasa.github.io)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/omagebright/review_exosite.git
cd review_exosite
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install FreeSASA:
```bash
# Download and compile FreeSASA from https://freesasa.github.io
# Follow the installation instructions for your system
```

## Usage

### Quick Start

Run the complete pipeline:
```bash
chmod +x run.sh
./run.sh
```

### Step-by-Step Execution

1. **Fetch PDB IDs**:
```bash
python fetch_pdb_ids.py --families families.yaml --out ids.json
```

2. **Download Structures**:
```bash
python download_structures.py ids.json --dst pdb/ --threads 8
```

3. **Compute Metrics**:
```bash
python compute_metrics.py pdb/ results_raw.csv --ids_json ids.json
```

4. **Summarize Statistics**:
```bash
python summarize_metrics.py results_raw.csv table2_recalc.csv
```

5. **Map Clinical Data**:
```bash
python map_clinical.py interventions.tsv clin_trials.csv
python calc_success.py clin_trials.csv success_rates.csv
```

6. **Generate Final Table**:
```bash
python merge_tables.py table2_recalc.csv success_rates.csv final_table.csv
```

## Pipeline Structure

### Core Scripts

- **`fetch_pdb_ids.py`**: Queries RCSB PDB Search API to retrieve PDB IDs for each protein family
- **`download_structures.py`**: Downloads PDB files for identified structures in parallel
- **`compute_metrics.py`**: Computes SASA and resolution metrics using FreeSASA
- **`summarize_metrics.py`**: Aggregates per-structure metrics into family-level statistics
- **`map_clinical.py`**: Maps clinical interventions to ClinicalTrials.gov data
- **`calc_success.py`**: Calculates clinical success rates (Phase ≥II)
- **`merge_tables.py`**: Merges structural and clinical data into final table

### Configuration Files

- **`families.yaml`**: Protein family definitions and search keywords
- **`interventions.tsv`**: Clinical intervention to family mappings
- **`requirements.txt`**: Python dependencies

### Execution

- **`run.sh`**: Master script for complete pipeline execution

## Data Sources

### Primary Data
- **Protein Data Bank (PDB)**: Structural data via RCSB PDB Search API v2
- **ClinicalTrials.gov**: Clinical trial data via API v2
- **FreeSASA**: Solvent accessible surface area calculations

### Protein Families Analyzed
- Serine Proteases (447 structures)
- Metalloproteases (91 structures)
- Cysteine Proteases (227 structures)
- Aspartic Proteases (89 structures)
- Ser/Thr Kinases (18 structures)
- Tyr Kinases (208 structures)
- Lipid Kinases (6 structures)
- Phosphatases (912 structures)
- Glycosyltransferases (148 structures)
- Ion Channels (202 structures)
- GPCRs (35 structures)

## Output Files

### Intermediate Files
- **`ids.json`**: PDB IDs organized by protein family
- **`results_raw.csv`**: Per-structure metrics (PDB ID, family, SASA, resolution)
- **`table2_recalc.csv`**: Family-level structural statistics
- **`clin_trials.csv`**: Clinical intervention phase data
- **`success_rates.csv`**: Clinical success rates by family

### Final Outputs
- **`final_table.csv`**: Complete structural statistics table
- **`Table2_Structural_Statistics.md`**: Formatted results with analysis

## Results

### Key Findings

**Structural Diversity**: Ion Channels (84,694 Å²) and Lipid Kinases (86,546 Å²) exhibit the largest exosite surfaces, while Serine Proteases (16,177 Å²) have the most compact exosites.

**Resolution Quality**: Metalloproteases achieve the highest resolution (2.01 Å average), while Ion Channels present crystallographic challenges (3.22 Å average).

**Dataset Coverage**: 2,383 high-quality structures across 11 protein families, with Phosphatases contributing the most structures (912).

### Statistical Summary

| Metric | Value |
|--------|-------|
| Total Structures | 2,383 |
| Protein Families | 11 |
| Mean SASA | 31,521 ± 2,291 Å² |
| Size Range | 260-435,359 Å² |
| Mean Resolution | 2.29 ± 0.84 Å |
| Geometric CV | 0.081 |

## Performance Notes

- **Runtime**: Complete pipeline takes ~2-4 hours depending on network speed
- **Memory**: Peak usage ~2GB for SASA calculations
- **Storage**: ~500MB for downloaded PDB files
- **Rate Limiting**: Built-in delays for API calls (0.25-0.3s between requests)

## Troubleshooting

### Common Issues

1. **FreeSASA Installation**: Ensure FreeSASA is properly compiled and accessible
2. **API Rate Limits**: Pipeline includes rate limiting; increase delays if needed
3. **Missing Structures**: Some PDB IDs may return 404 errors (outdated entries)
4. **Memory Issues**: Reduce batch sizes for large protein families

### Error Handling

The pipeline includes comprehensive error handling:
- Failed downloads are logged and skipped
- Invalid structures are excluded from analysis
- API failures are retried with exponential backoff

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit your changes (`git commit -am 'Add enhancement'`)
4. Push to the branch (`git push origin feature/enhancement`)
5. Create a Pull Request

## Citation

If you use this pipeline in your research, please cite:

```bibtex
@article{exosite_analysis_2024,
  title={Structural Statistics of Exosites in the Protein Data Bank},
  author={[Author Names]},
  journal={[Journal Name]},
  year={2024},
  doi={[DOI]}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **RCSB PDB**: For providing structural data and API access
- **ClinicalTrials.gov**: For clinical trial data
- **FreeSASA**: For solvent accessible surface area calculations
- **Python Community**: For the excellent scientific computing ecosystem

## Contact

For questions or support, please open an issue on GitHub or contact [your-email@domain.com].

---

**Last Updated**: 2024-07-08  
**Version**: 1.0.0  
**Status**: Production Ready