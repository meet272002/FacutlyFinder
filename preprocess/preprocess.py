import pandas as pd
from pathlib import Path
import ast

class PreProcess:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent
        self.DATA_DIR = self.BASE_DIR.parent / "data"
        self.df = pd.read_csv(self.DATA_DIR/"dau-faculty.csv")

    def insertRules(self):
        return {
            "Gandhinagar": 3,
            "M.Phil": 0,
            "(1989)": 0,
            "Canada": 3,
            "New York": 2,
            "Denmark": 3,
            "Australia": 3,
            "Jaipur": 2,
            "Ahmedabad": 2,
            "Kolkata": 2,
            "Ireland": 3,
            "Hyderabad": 2,
            "UK": 3,
            "Calcutta": 2,
            "USA": 3,
            "Udaipur": 2,
            "New Delhi": 2,
            "Durgapur": 2,
            "Mumbai": 2,
            "Delhi": 2,
            "Los Angeles": 2,
            "Jabalpur": 2,
            "Pilani": 2,
            "Shantiniketan": 2,
            "Pittsburgh": 2,
            "PhD (International Economics)": 0,
            "Finland": 3,
            "France": 3,
            "University of London": 1,
            "University of Southern California (USC)": 1,
            "Bangalore": 2,
            "Italy": 3,
            "Germany": 3,
            "Pune (GIPE)": 1,
            "West Bengal": 2,
            "Pennsylvania": 2,
            "MA psychology in Psychotherapy and Counselling": 0
        }

    def upsertAtIndex(self, arr, value, idx):
        if value not in arr:
            return arr  # do nothing if value is not present in this row

        arr = [x for x in arr if x != value]  # remove it from current position

        if len(arr) > idx:
            arr.insert(idx, value)
        else:
            while len(arr) < idx:
                arr.append("")
            arr.append(value)

        return arr

    def applyRules(self, arr):
        insert_rules = self.insertRules()
        for val, idx in insert_rules.items():
            arr = self.upsertAtIndex(arr, val, idx)
        return arr

    def parseList(self, val):
        if pd.isna(val):
            return []

        if val.startswith('[') and val.endswith(']'):
            return [v.strip() for v in ast.literal_eval(val)]

        return [v.strip() for v in val.split(',') if v.strip()]

    def cleanTeach(self,val):
        junk_set = {'facebook', 'x', 'instagram', 'youtube', 'linkedin', 'blogicon'}

        if isinstance(val, list):
            norm = [x.lower().strip() for x in val]
            if set(norm) == junk_set:
                return None
            cleaned = [x for x in val if x.lower().strip() not in junk_set]
            return cleaned if cleaned else None

    def faculty(self):
        df_faculty = self.df[["Name","Phone","Email","FacultyWebsite","Bio","Education","Address","Teaching","specialization","Research"]]
        df_faculty = df_faculty.copy()
        df_faculty.loc['Name'] = df_faculty['Name'].str.strip().str.title()

        df_faculty['edu_list'] = df_faculty['Education'].str.split(',').apply(
            lambda x: [i.strip() for i in x] if isinstance(x, list) else [])
        df_faculty['edu_list'] = df_faculty['edu_list'].apply(self.applyRules)

        df_faculty["Education"] = df_faculty["edu_list"].str[0]
        df_faculty["Education_Institute"] = df_faculty["edu_list"].str[1]
        df_faculty["Education_City"] = df_faculty["edu_list"].str[2]
        df_faculty["Education_country"] = df_faculty["edu_list"].str[3]
        df_faculty.drop(columns=['edu_list'],inplace=True)

        df_faculty['Phone'] = df_faculty['Phone'].str.split(r'[;,/|]').str[0].str.strip()

        df_faculty['Address'] = df_faculty['Address'].str.extract(r'(#.*)', expand=False).str.replace('#', '', regex=False).str.replace(r'\s+', ' ', regex=True).str.strip()
        df_faculty["Room_No"] = df_faculty['Address'].str.split(',').str[0]
        df_faculty["Teaching_Institute"] = df_faculty['Address'].str.split(',').str[2]
        df_faculty["Faculty_Block"] = df_faculty['Address'].str.split(',').str[1]
        df_faculty.drop(columns=['Address'], inplace=True)

        df_faculty['Teaching'] = df_faculty['Teaching'].apply(self.parseList)
        df_faculty['Teaching'] = df_faculty['Teaching'].apply(self.cleanTeach)

        df_faculty['specialization'] = df_faculty['specialization'].apply(self.parseList)
        df_faculty['Research'] = df_faculty['Research'].apply(self.parseList)
        df_faculty.to_csv(self.DATA_DIR/"faculty.csv",index=False)

pp = PreProcess()
pp.faculty()
