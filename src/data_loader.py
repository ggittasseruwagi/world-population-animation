
"""
Data loading and cleaning module for world population visualization
"""
import pandas as pd
import requests


class DataLoader:
    """
    Handles fetching and processing world population data from World Bank API.
    """

    def __init__(self):
        """Initialize the DataLoader with World Bank API endpoint"""
        self.base_url = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL"
        self.data = None
        self.cleaned_data = None

    def fetch_population_data(self, start_year=1960, end_year=2023):
        """
        Fetch population data from World Bank API

        Parameters:
        - start_year: Starting year for data (default 1960)
        - end_year: Ending year for data (default 2023)

        Returns:
        - DataFrame with population data
        """
        print(f"📥 Fetching population data from {start_year} to {end_year}...")

        params = {
            'date': f'{start_year}:{end_year}',
            'format': 'json',
            'per_page': 20000
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            json_data = response.json()

            if len(json_data) < 2:
                print("❌ No data returned from API")
                return None

            data_records = json_data[1]
            self.data = pd.DataFrame(data_records)
            print(f"✅ Fetched {len(self.data)} records!")

            return self.data

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching data: {e}")
            return None

    def clean_data(self):
        """Clean and prepare data for visualization"""
        if self.data is None:
            print("❌ No data to clean. Run fetch_population_data() first!")
            return None

        print("🧹 Cleaning data...")

        df = self.data.copy()

        cleaned = pd.DataFrame({
            'country': df['country'].apply(lambda x: x['value'] if isinstance(x, dict) else x),
            'country_code': df['countryiso3code'],
            'year': df['date'].astype(int),
            'population': df['value']
        })

        cleaned = cleaned.dropna(subset=['population'])

        aggregate_codes = ['ARB', 'CSS', 'CEB', 'EAR', 'EAS', 'EAP', 'TEA', 'EMU', 'ECS', 
                          'ECA', 'TEC', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 'IDB',
                          'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC',
                          'LMC', 'MEA', 'MNA', 'TMN', 'MIC', 'NAC', 'OED', 'OSS', 'PSS',
                          'PST', 'PRE', 'SST', 'SAS', 'TSA', 'SSF', 'SSA', 'TSS', 'UMC',
                          'WLD']

        cleaned = cleaned[~cleaned['country_code'].isin(aggregate_codes)]
        cleaned = cleaned[cleaned['country_code'].notna()]
        cleaned = cleaned[cleaned['country_code'].str.len() == 3]

        cleaned['population'] = pd.to_numeric(cleaned['population'], errors='coerce')
        cleaned = cleaned.sort_values(['year', 'country']).reset_index(drop=True)

        self.cleaned_data = cleaned

        print(f"✅ Cleaned data: {len(cleaned)} records")
        print(f"   Countries: {cleaned['country'].nunique()}")
        print(f"   Years: {cleaned['year'].min()} to {cleaned['year'].max()}")

        return self.cleaned_data

    def get_data_summary(self):
        """Get a summary of the loaded data"""
        if self.cleaned_data is None:
            print("❌ No cleaned data available!")
            return None

        summary = {
            'total_records': len(self.cleaned_data),
            'countries': self.cleaned_data['country'].nunique(),
            'year_range': f"{self.cleaned_data['year'].min()} - {self.cleaned_data['year'].max()}",
            'total_population_latest': self.cleaned_data[
                self.cleaned_data['year'] == self.cleaned_data['year'].max()
            ]['population'].sum()
        }

        return summary
