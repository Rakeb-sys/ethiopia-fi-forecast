import os
import logging
import pandas as pd
import numpy as np

# Setup logging telemetry
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SelamForecastingPipeline")

class UnifiedDataPipeline:
    def __init__(self, raw_data_path: str, reference_path: str):
        self.raw_data_path = raw_data_path
        self.reference_path = reference_path
        self.df_unified = None
        self.df_refs = None
        
        self.expected_columns = [
            'record_id', 'record_type', 'pillar', 'category', 'indicator', 
            'indicator_code', 'value_numeric', 'observation_date', 'source_name', 
            'source_url', 'confidence', 'parent_id', 'related_indicator', 
            'impact_direction', 'impact_magnitude', 'lag_months', 'evidence_basis'
        ]

    def load_datasets(self) -> "UnifiedDataPipeline":
        """Reads raw assets defensively."""
        logger.info("Initializing raw data acquisition...")
        for path in [self.raw_data_path, self.reference_path]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Critical Error: Missing baseline input file at {path}")
        
        self.df_unified = pd.read_csv(self.raw_data_path)
        self.df_refs = pd.read_csv(self.reference_path)
        logger.info(f"Loaded {len(self.df_unified)} raw records.")
        return self

    def enforce_schema_and_types(self) -> "UnifiedDataPipeline":
        """Ensures column alignment and type normalization."""
        if self.df_unified is None:
            raise ValueError("Pipeline state error: Execute load_datasets before normalization.")
        
        for col in self.expected_columns:
            if col not in self.df_unified.columns:
                self.df_unified[col] = np.nan
        
        self.df_unified = self.df_unified[self.expected_columns]
        
        self.df_unified['record_id'] = self.df_unified['record_id'].astype(str)
        self.df_unified['record_type'] = self.df_unified['record_type'].astype(str).str.strip().str.lower()
        self.df_unified['value_numeric'] = pd.to_numeric(self.df_unified['value_numeric'], errors='coerce')
        self.df_unified['observation_date'] = pd.to_datetime(self.df_unified['observation_date'], errors='coerce')
        
        logger.info("Schema structural invariants verified.")
        return self

    def inject_enriched_records(self, enrichment_records: list) -> "UnifiedDataPipeline":
        """Appends verified records into memory."""
        logger.info(f"Injecting {len(enrichment_records)} enriched records...")
        df_new = pd.DataFrame(enrichment_records)
        
        for col in self.expected_columns:
            if col not in df_new.columns:
                df_new[col] = np.nan
        df_new = df_new[self.expected_columns]
        
        self.df_unified = pd.concat([self.df_unified, df_new], ignore_index=True)
        self.enforce_schema_and_types()
        return self

    def save_processed_data(self, output_path: str):
        """Saves output into data/processed directory."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.df_unified.to_csv(output_path, index=False)
        logger.info(f"Processed dataset successfully written to: {output_path}")

if __name__ == "__main__":
    # Explicit directory routing
    RAW_DATA_PATH = "data/raw/ethiopia_fi_unified_data.csv"
    REF_DATA_PATH = "data/raw/reference_codes.csv"
    PROCESSED_DATA_PATH = "data/processed/ethiopia_fi_unified_data_processed.csv"

    pipeline = UnifiedDataPipeline(RAW_DATA_PATH, REF_DATA_PATH).load_datasets().enforce_schema_and_types()

    # Enriched payload tracking Findex gender splits and central bank policy shocks
    enrichment_payload = [
        {
            'record_id': 'ENR_OBS_001', 'record_type': 'observation', 'pillar': 'ACCESS',
            'category': 'demographic_findex', 'indicator': 'Account Ownership Rate, Female',
            'indicator_code': 'ACC_OWNERSHIP_FEMALE', 'value_numeric': 36.0,
            'observation_date': '2021-12-31', 'source_name': 'World Bank Global Findex Database 2021',
            'source_url': 'https://www.worldbank.org/en/publication/globalfindex', 'confidence': 'high'
        },
        {
            'record_id': 'ENR_OBS_002', 'record_type': 'observation', 'pillar': 'ACCESS',
            'category': 'demographic_findex', 'indicator': 'Account Ownership Rate, Male',
            'indicator_code': 'ACC_OWNERSHIP_MALE', 'value_numeric': 56.0,
            'observation_date': '2021-12-31', 'source_name': 'World Bank Global Findex Database 2021',
            'source_url': 'https://www.worldbank.org/en/publication/globalfindex', 'confidence': 'high'
        },
        {
            'record_id': 'ENR_EVT_003', 'record_type': 'event', 'pillar': np.nan,
            'category': 'policy', 'indicator': 'NBE Mobile Money Licensing Directive No. ONPSD/01/2020',
            'indicator_code': 'EVENT_NBE_DIR', 'value_numeric': np.nan,
            'observation_date': '2020-04-01', 'source_name': 'National Bank of Ethiopia Legal Gazette',
            'source_url': 'https://nbe.gov.et', 'confidence': 'high'
        },
        {
            'record_id': 'ENR_LNK_004', 'record_type': 'impact_link', 'pillar': 'USAGE',
            'category': 'causal_link', 'indicator': np.nan, 'indicator_code': np.nan,
            'value_numeric': np.nan, 'observation_date': np.nan,
            'parent_id': 'ENR_EVT_003', 'related_indicator': 'MOBILE_MONEY_ACC',
            'impact_direction': 'positive', 'impact_magnitude': 'high',
            'lag_months': 12, 'evidence_basis': 'Direct catalyst for non-bank payment operator entries (Telebirr, M-Pesa).'
        }
    ]

    pipeline.inject_enriched_records(enrichment_payload)
    pipeline.save_processed_data(PROCESSED_DATA_PATH)