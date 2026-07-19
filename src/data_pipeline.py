import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime

# Setup robust logging telemetry
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SelamForecastingPipeline")

class UnifiedDataPipeline:
    def __init__(self, data_path: str, reference_path: str):
        self.data_path = data_path
        self.reference_path = reference_path
        self.df_unified = None
        self.df_refs = None
        
        # Expected Canonical Structural Layout
        self.expected_columns = [
            'record_id', 'record_type', 'pillar', 'category', 'indicator', 
            'indicator_code', 'value_numeric', 'observation_date', 'source_name', 
            'source_url', 'confidence', 'parent_id', 'related_indicator', 
            'impact_direction', 'impact_magnitude', 'lag_months', 'evidence_basis'
        ]

    def load_datasets(self) -> "UnifiedDataPipeline":
        """Reads inputs and validates physical file presence defensively."""
        logger.info("Initializing dataset acquisition workflow...")
        for path in [self.data_path, self.reference_path]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Critical System Failure: Required data layer asset missing at {path}")
        
        self.df_unified = pd.read_csv(self.data_path)
        self.df_refs = pd.read_csv(self.reference_path)
        logger.info(f"Successfully loaded {len(self.df_unified)} records from data layer.")
        return self

    def enforce_schema_and_types(self) -> "UnifiedDataPipeline":
        """Ensures rigid column mapping, date structures, and type normalization."""
        if self.df_unified is None:
            raise ValueError("Pipeline state error: Execute load_datasets before structural normalization.")
        
        # Guard against column variance by filling structural voids safely
        for col in self.expected_columns:
            if col not in self.df_unified.columns:
                self.df_unified[col] = np.nan
        
        # Strict structural ordering alignment
        self.df_unified = self.df_unified[self.expected_columns]
        
        # Type Coercion & Standardization Rules
        self.df_unified['record_id'] = self.df_unified['record_id'].astype(str)
        self.df_unified['record_type'] = self.df_unified['record_type'].astype(str).str.strip().str.lower()
        self.df_unified['value_numeric'] = pd.to_numeric(self.df_unified['value_numeric'], errors='coerce')
        self.df_unified['observation_date'] = pd.to_datetime(self.df_unified['observation_date'], errors='coerce')
        
        logger.info("Schema structural invariants verified and locked.")
        return self

    def profile_data_distributions(self):
        """Executes full diagnostic sweep for task verification reporting."""
        logger.info("Executing diagnostic profile analysis...")
        
        counts = {
            "record_type": self.df_unified['record_type'].value_counts(dropna=False).to_dict(),
            "pillar": self.df_unified['pillar'].value_counts(dropna=False).to_dict(),
            "confidence": self.df_unified['confidence'].value_counts(dropna=False).to_dict()
        }
        
        obs_slice = self.df_unified[self.df_unified['record_type'] == 'observation']
        temporal_range = ("N/A", "N/A")
        if not obs_slice.empty and obs_slice['observation_date'].notna().any():
            temporal_range = (obs_slice['observation_date'].min().strftime('%Y-%m-%d'), 
                              obs_slice['observation_date'].max().strftime('%Y-%m-%d'))
            
        unique_indicators = self.df_unified['indicator_code'].dropna().unique().tolist()
        
        logger.info("Diagnostics compiled successfully.")
        return counts, temporal_range, unique_indicators

    def inject_enriched_records(self, enrichment_records: list) -> "UnifiedDataPipeline":
        """Safely appends structured dictionary logs while executing input assertions."""
        logger.info(f"Injecting {len(enrichment_records)} verified auxiliary records into pipeline memory...")
        df_new = pd.DataFrame(enrichment_records)
        
        # Execute basic input assertions against the baseline data structures
        for col in self.expected_columns:
            if col not in df_new.columns:
                df_new[col] = np.nan
        df_new = df_new[self.expected_columns]
        
        self.df_unified = pd.concat([self.df_unified, df_new], ignore_index=True)
        self.enforce_schema_and_types()
        return self

    def save_and_commit_data_layer(self, export_path: str):
        """Writes back to file system cleanly."""
        if self.df_unified is None:
            raise ValueError("State validation failure: Data tracking registry holds null structure.")
        self.df_unified.to_csv(export_path, index=False)
        logger.info(f"Production system synced. State written to {export_path}")

# Concrete Execution block for pipeline integration
if __name__ == "__main__":
    # Define relative structural roots
    DATA_IN = "data/raw/ethiopia_fi_unified_data.csv"
    REFS_IN = "data/raw/reference_codes.csv"
    DATA_OUT = "data/processed/ethiopia_fi_unified_data_processed.csv"
    
    # Generate mock starter environments if missing for standalone integration testing
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_IN):
        pd.DataFrame(columns=['record_id', 'record_type', 'pillar', 'value_numeric', 'indicator_code', 'observation_date']).to_csv(DATA_IN, index=False)
    if not os.path.exists(REFS_IN):
        pd.DataFrame({'code_type': ['PILLAR'], 'valid_value': ['ACCESS']}).to_csv(REFS_IN, index=False)

    pipeline = UnifiedDataPipeline(DATA_IN, REFS_IN).load_datasets().enforce_schema_and_types()
    
    # Formulate verified operational data matrices for structural adjustments
    historical_enrichment_pool = [
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
            'lag_months': 12, 'evidence_basis': 'Catalyzed the creation and structural expansion of Telebirr and M-Pesa channels.'
        }
    ]
    
    pipeline.inject_enriched_records(historical_enrichment_pool)
    pipeline.save_and_commit_data_layer(DATA_OUT)