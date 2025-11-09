# Drug database - Top 200 prescribed drugs with their mechanisms of action
# Data structure matches the API response format expected by the frontend

DRUGS_DATABASE = [
    # Top 8 drugs from frontend array
    {
        "id": 1,
        "generic_name": "lisinopril",
        "brand_name": "Prinivil, Zestril",
        "moa": [{"moa": "ACE Inhibitor"}]
    },
    {
        "id": 2,
        "generic_name": "atorvastatin calcium",
        "brand_name": "Lipitor",
        "moa": [{"moa": "HMG-CoA Reductase Inhibitor (Statin)"}]
    },
    {
        "id": 3,
        "generic_name": "amlodipine besylate",
        "brand_name": "Norvasc",
        "moa": [{"moa": "Calcium Channel Blocker"}]
    },
    {
        "id": 4,
        "generic_name": "metoprolol tartrate",
        "brand_name": "Lopressor",
        "moa": [{"moa": "Beta-1 Selective Blocker"}]
    },
    {
        "id": 5,
        "generic_name": "simvastatin",
        "brand_name": "Zocor",
        "moa": [{"moa": "HMG-CoA Reductase Inhibitor (Statin)"}]
    },
    {
        "id": 6,
        "generic_name": "losartan potassium",
        "brand_name": "Cozaar",
        "moa": [{"moa": "Angiotensin II Receptor Blocker (ARB)"}]
    },
    {
        "id": 7,
        "generic_name": "albuterol sulfate",
        "brand_name": "Proventil, Ventolin",
        "moa": [{"moa": "Beta-2 Adrenergic Agonist"}]
    },
    {
        "id": 8,
        "generic_name": "sertraline hydrochloride",
        "brand_name": "Zoloft",
        "moa": [{"moa": "Selective Serotonin Reuptake Inhibitor (SSRI)"}]
    },
    # Additional top prescribed drugs
    {
        "id": 9,
        "generic_name": "levothyroxine sodium",
        "brand_name": "Synthroid, Levoxyl",
        "moa": [{"moa": "Thyroid Hormone Replacement"}]
    },
    {
        "id": 10,
        "generic_name": "metformin hydrochloride",
        "brand_name": "Glucophage",
        "moa": [{"moa": "Biguanide (Decreases Hepatic Glucose Production)"}]
    },
    {
        "id": 11,
        "generic_name": "omeprazole",
        "brand_name": "Prilosec",
        "moa": [{"moa": "Proton Pump Inhibitor (PPI)"}]
    },
    {
        "id": 12,
        "generic_name": "azithromycin",
        "brand_name": "Zithromax",
        "moa": [{"moa": "Macrolide Antibiotic (Protein Synthesis Inhibitor)"}]
    },
    {
        "id": 13,
        "generic_name": "amoxicillin",
        "brand_name": "Amoxil",
        "moa": [{"moa": "Beta-Lactam Antibiotic (Cell Wall Synthesis Inhibitor)"}]
    },
    {
        "id": 14,
        "generic_name": "hydrochlorothiazide",
        "brand_name": "Microzide",
        "moa": [{"moa": "Thiazide Diuretic"}]
    },
    {
        "id": 15,
        "generic_name": "gabapentin",
        "brand_name": "Neurontin",
        "moa": [{"moa": "GABA Analogue (Calcium Channel Modulator)"}]
    },
    {
        "id": 16,
        "generic_name": "clopidogrel",
        "brand_name": "Plavix",
        "moa": [{"moa": "Antiplatelet Agent (P2Y12 Inhibitor)"}]
    },
    {
        "id": 17,
        "generic_name": "furosemide",
        "brand_name": "Lasix",
        "moa": [{"moa": "Loop Diuretic"}]
    },
    {
        "id": 18,
        "generic_name": "warfarin sodium",
        "brand_name": "Coumadin",
        "moa": [{"moa": "Vitamin K Antagonist (Anticoagulant)"}]
    },
    {
        "id": 19,
        "generic_name": "atenolol",
        "brand_name": "Tenormin",
        "moa": [{"moa": "Beta-1 Selective Blocker"}]
    },
    {
        "id": 20,
        "generic_name": "prednisone",
        "brand_name": "Deltasone",
        "moa": [{"moa": "Corticosteroid (Anti-inflammatory)"}]
    },
    {
        "id": 21,
        "generic_name": "alprazolam",
        "brand_name": "Xanax",
        "moa": [{"moa": "Benzodiazepine (GABA-A Receptor Agonist)"}]
    },
    {
        "id": 22,
        "generic_name": "fluoxetine",
        "brand_name": "Prozac",
        "moa": [{"moa": "Selective Serotonin Reuptake Inhibitor (SSRI)"}]
    },
    {
        "id": 23,
        "generic_name": "escitalopram",
        "brand_name": "Lexapro",
        "moa": [{"moa": "Selective Serotonin Reuptake Inhibitor (SSRI)"}]
    },
    {
        "id": 24,
        "generic_name": "carvedilol",
        "brand_name": "Coreg",
        "moa": [{"moa": "Non-selective Beta Blocker with Alpha-1 Blocking"}]
    },
    {
        "id": 25,
        "generic_name": "tramadol",
        "brand_name": "Ultram",
        "moa": [{"moa": "Opioid Agonist and SNRI"}]
    },
]

# Extract unique MOAs for the MOA endpoint
def get_all_moas():
    """Extract all unique mechanisms of action from the drug database"""
    moas = set()
    for drug in DRUGS_DATABASE:
        for moa_obj in drug["moa"]:
            moas.add(moa_obj["moa"])

    return [{"id": idx + 1, "moa": moa} for idx, moa in enumerate(sorted(moas))]


def get_drug_by_generic_name(generic_name: str):
    """Find drug by generic name (case-insensitive)"""
    generic_lower = generic_name.lower().strip()
    for drug in DRUGS_DATABASE:
        if drug["generic_name"].lower() == generic_lower:
            return drug
    return None
