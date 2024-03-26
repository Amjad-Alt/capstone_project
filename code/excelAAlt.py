
#%%
import os
import glob
import pandas as pd
import re

#%%
class excelAAlt:
    """
    A class to extract data from Excel files (.xls and .xlsx), focusing on
    structured data extraction and organization into a pandas DataFrame.
    """

    def __init__(self, excel_path=""):
        """
        Constructor initializes the class with lists of cities, months, years,
        and sets up a multi-index DataFrame for storing extracted data.
        """
        self.cities = [
            "MAKKAH", "RIYADH", "TAIF", "JEDDAH", "BURAYDAH", "MEDINA",
            "HOFHUF", "DAMMAM", "TABUK", "ABHA", "JAZAN", "HAIL", "BAHA",
            "NJRAN", "ARAR", "SKAKA"
        ] 
        self.months = [
            "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
            "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"
        ]
        self.years = list(range(2015, 2017))

        # Setup multi-level columns for the DataFrame
        multicolumns = pd.MultiIndex.from_product(
            [self.cities, self.years, self.months],
            names=['City', 'Year', 'Month']
        )

        self.rowIndices = ['General Index',
                           'FOOD AND BEVERAGES',
                           'FOOD',
                           'BEVERAGES',
                           'TOBACCO',
                           'CLOTHING AND FOOTWEAR',
                           'CLOTHING',
                           'FOOTWEAR',
                           'HOUSING, WATER, ELECTRI-CITY ,GAS AND OTHER FUELS',
                           'RENTALS FOR HOUSING',
                           'MAITENANCE OF THE DEWELLING',
                           'WATER SUPPLY & OTHER SERVICES',
                           'ELECTRICITY, GAS AND OTHER FUELS',
                           'FURNISHINGS, HOUSEHOLD EQUIPMENT AND MAINTENANCE',
                           'FURNITURE & CARPETS',
                           'HOUSEHOLD TEXTILES',
                           'HOUSEHOLD APPLIANCES',
                           'HOUSEHOLD UTENSILS',
                           'TOOLS FOR HOUSE & GARDEN',
                           'GOODS FOR HOUSEHOLD MAINTENANCE',
                           'HEALTH',
                           'MEDICAL PRODUCTS & EQUIPMENT',
                           'OUTPATIENT SERVICES',
                           'HOSPITAL SERVICES',
                           'TRANSPORT',
                           'PURCHASE OF VEHICLES',
                           'OPERATION OF TRANSPORT EQUIPMENT',
                           'TRANSPORT SERVICES',
                           'COMMUNICATION',
                           'POSTAL SERVICES',
                           'TELEPHONE AND TELEFAX EQUIPMENT',
                           'TELEPHONE AND TELEFAX SERVICES',
                           'RECREATION AND CULTURE',
                           'AUDIO, PHOTO & INFO. EQUIPMENT',
                           'OTHER RECREATION & CULTURE GOODS',
                           'OTHER RECREATIONAL GOODS',
                           'RECREATIONAL & CULTURAL SERVICES',
                           'NEWSPAPERS, BOOKS & STATIONERY',
                           'PACKAGE HOLIDAYS',
                           'EDUCATION',
                           'PRE-PRIMARY & PRIMARY EDUCATION',
                           'SECONDARY&INTERMEDIATE EDUCATION',
                           'POST-SECONDARY EDUCATION',
                           'TERTIARY EDUCATION',
                           'RESTAURANTS AND HOTELS',
                           'CATERING SERVICE',
                           'ACCOMMODATION SERVICES',
                           'MISCELLANEOUS GOODS AND SERVICES',
                           'PERSONAL CARE',
                           'PERSONAL EFFECTS N.E.C.',
                           'SOCIAL PROTECTION',
                           'INSURANCE',
                           'FINANCIAL SERVICES N.E C.',
                           'OTHER SERVICES N.E.C.'
                           ]

        # Setup DataFrame with multi-level columns and no initial rows
        self.cityIndexDf = pd.DataFrame(columns=multicolumns)
        self.cityIndexDf.index.name = "Category"  # Naming the index for clarity

    def find_year_months_cities(self, df):
        """input: all the data
        loop and find cities, months and year
        output: two list of two index and a number"""
        found_year = None
        found_months = []
        found_cities = []

        combined_text = " ".join(df.iloc[:10].astype(str).values.flatten())
        year_re = re.compile(r'(2015|2016|2017)')
        year_match = year_re.search(combined_text)
        if year_match:
            found_year = int(year_match.group())

        for month in self.months:
            if month.lower() in combined_text.lower():
                found_months.append(month)
                if len(found_months) == 2:
                    break

        for city in self.cities:
            if city.lower() in combined_text.lower():
                found_cities.append(city)
                if len(found_cities) == 2:
                    break

        if found_year and len(found_months) == 2 and len(found_cities) == 2:
            return (found_year, found_months, found_cities)
        else:
            return None
                   
    def extract_values(self, df, rowIndices):
        """ get the values:
        input: rowIndices
        then loop through each one
        then when you find have a list of the values based on position
        output: list of 4 indexs"""
        
        # Iterate through each rowIndex to find its starting position
        for rowIndex in rowIndices:
            for row in range(len(df)):
                if rowIndex in df.iloc[row, :].values:
                    # Found the row where rowIndex is located
                    start_col = df.columns.get_loc(df.iloc[row, :][df.iloc[row, :].str.contains(rowIndex, na=False)].index[0]) - 1
                    values_to_assign = [
                        df.iloc[row, start_col],  # Value for city[1], month[1]
                        df.iloc[row, start_col - 1],  # Value for city[1], month[0]
                        df.iloc[row, start_col - 4],  # Value for city[0], month[1] (skipping two cell)
                        df.iloc[row, start_col - 5],  # Value for city[0], month[0]
                    ]

    
    def extract_info(self, values_to_assign, found_year, found_months, found_cities):
        """ input value list== 4, cities == 2, months ==2, year ==1
        do:
        [found_cities[0], found_year, found_months[0]] = values_to_assign[0],
        [found_cities[0], found_year, found_months[1]] = values_to_assign[1],
        [found_cities[1], found_year, found_months[0]] = values_to_assign[2],
        [found_cities[1], found_year,found_months[1]] = values_to_assign[3]"""
        
        self.cityIndexDf.loc[(found_cities[0], found_year, found_months[0])] = values_to_assign[0]
        self.cityIndexDf.loc[(found_cities[0], found_year, found_months[1])] = values_to_assign[1]
        self.cityIndexDf.loc[(found_cities[1], found_year, found_months[0])] = values_to_assign[2]
        self.cityIndexDf.loc[(found_cities[1], found_year, found_months[1])] = values_to_assign[3]
    
    def processPages(self, directory_path, file_pattern="*.xls*"):
        for file_path in glob.glob(os.path.join(directory_path, file_pattern)):
            sheet_names = pd.ExcelFile(file_path).sheet_names
            for sheet_name in sheet_names:
                if '4' in sheet_name:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    cityYearMonth = self.find_year_months_cities(df)
                    if cityYearMonth:
                        found_year, found_months, found_cities = cityYearMonth
                        for rowIndex in self.rowIndices:
                            values_to_assign = self.extract_values(df, rowIndex)
                            if values_to_assign:
                                self.extract_info(values_to_assign, found_year, found_months, found_cities)



# %%
file_path = '../data/2016'
extractor = excelAAlt()
extractor.processPages(file_path)  # %%

# %%