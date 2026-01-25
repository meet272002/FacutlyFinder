import pandas as pd
from pathlib import Path
import ast


class InsertValues:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.BASE_DIR = Path(__file__).resolve().parent
        self.DATA_DIR = self.BASE_DIR.parent / "data"
        self.df = pd.read_csv(self.DATA_DIR / "faculty.csv")
        self.delete()

    def delete(self):
        try:
            tables = [
                "Faculty_Specialization",
                "Faculty_Teaching",
                "Faculty_Research",
                "Specialization",
                "Teaching",
                "Research",
                "Faculty"
            ]

            for table in tables:
                self.cursor.execute(f"DELETE FROM {table}")
        except Exception as e:
            print("Error in Deleting Existing Records:", e)

    def get_or_create(self, table, column, value):
        try:
            self.cursor.execute(
                f"SELECT {table}_id FROM {table} WHERE {column} = ?",
                (value.strip(),)
            )
            row = self.cursor.fetchone()

            if row:
                return row[0]
            self.cursor.execute(
                f"INSERT INTO {table} ({column}) VALUES (?)",
                (value.strip(),)
            )
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error in get_or_create for {table}:", e)
            return None
        
    def insert_faculty(self, faculty_data: tuple):
        try:
            self.cursor.execute("""
                INSERT INTO Faculty (
                    Name, Phone, Email, FacultyWebsite, Bio,
                    Education, Education_Institute, Education_City,
                    Education_country, Teaching_Institute,
                    Faculty_Block, Room_No
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, faculty_data)
            self.conn.commit()
        except Exception as e:
            print("Error in Inserting Faculty:", e)
        return self.cursor.lastrowid

    def insert_specialization(self, faculty_id, specialization_str):
        try:
            for spec in specialization_str:
                spec_id = self.get_or_create(
                    "Specialization","Specialization", spec
                )
                self.cursor.execute("""
                    INSERT INTO Faculty_Specialization (Faculty_id, Specialization_id)
                    VALUES (?, ?)
                """, (faculty_id, spec_id))
                self.conn.commit()
        except Exception as e:
            print("Error in Inserting Specialization:", e)

    def insert_teaching(self, faculty_id, teaching_str):
        try:
            for topic in teaching_str:
                teaching_id = self.get_or_create("Teaching", "Teaching", topic)
                self.cursor.execute("""
                    INSERT INTO Faculty_Teaching (Faculty_id, Teaching_id)
                    VALUES (?, ?)
                """, (faculty_id, teaching_id))
                self.conn.commit()
        except Exception as e:
            print("Error in Inserting Teaching:", e)    

    def insert_research(self, faculty_id, research_str):
        try:
            for area in research_str:
                research_id = self.get_or_create("Research", "Research", area)
                self.cursor.execute("""
                    INSERT INTO Faculty_Research (Faculty_id, Research_id)
                    VALUES (?, ?)
                """, (faculty_id, research_id))
                self.conn.commit()
        except Exception as e:
            print("Error in Inserting Research:", e)


    def insert_values(self):
        try:
            for _, row in self.df.iterrows():
                faculty_id = self.insert_faculty((
                    row["Name"],
                    row["Phone"],
                    row["Email"],
                    row["FacultyWebsite"],
                    row["Bio"],
                    row["Education"],
                    row["Education_Institute"],
                    row["Education_City"],
                    row["Education_country"],
                    row["Room_No"],
                    row["Teaching_Institute"],
                    row["Faculty_Block"]
                ))

                if isinstance(row["specialization"], str):
                    self.insert_specialization(int(faculty_id), ast.literal_eval(row["specialization"]))
                if isinstance(row["Research"], str):
                    self.insert_research(int(faculty_id), ast.literal_eval(row["Research"]))
                if isinstance(row["Teaching"], str):
                    self.insert_teaching(int(faculty_id), ast.literal_eval(row["Teaching"]))
        except Exception as e:
            print("Error in Inserting Values:", e)
