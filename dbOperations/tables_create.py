class CreateTable():
    def __init__(self,conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.drop_table()

    def drop_table(self):
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
                self.cursor.execute(f"DROP TABLE IF EXISTS {table}")

            self.conn.commit()
        except Exception as e:
            print("Error in Dropping Tables:", e)
            
    def create_tables(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Faculty("
                                "Faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "Name TEXT, "
                                "Phone TEXT, "
                                "Email TEXT, "
                                "FacultyWebsite TEXT, "
                                "Bio TEXT, "
                                "Education TEXT, "
                                "Education_Institute TEXT, "
                                "Education_City TEXT, "
                                "Education_country TEXT, "
                                "Teaching_Institute TEXT, "
                                "Faculty_Block TEXT, "
                                "Room_No INTEGER)")

            self.cursor.execute("CREATE TABLE IF NOT EXISTS Specialization("
                                "Specialization_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "Specialization TEXT)")

            self.cursor.execute("CREATE TABLE IF NOT EXISTS Faculty_Specialization("
                                "Faculty_id INTEGER, "
                                "Specialization_id INTEGER,"
                                "FOREIGN KEY(Faculty_id) REFERENCES Faculty(Faculty_id), "
                                "FOREIGN KEY(Specialization_id) REFERENCES Specialization(Specialization_id))")

            self.cursor.execute("CREATE TABLE IF NOT EXISTS Research("
                                "Research_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "Research TEXT)")

            self.cursor.execute("CREATE TABLE IF NOT EXISTS Faculty_Research("
                                "Faculty_id INTEGER, "
                                "Research_id INTEGER, "
                                "FOREIGN KEY(Faculty_id) REFERENCES Faculty(Faculty_id),"
                                "FOREIGN KEY(Research_id) REFERENCES Research(Research_id))")

            self.cursor.execute("CREATE TABLE IF NOT EXISTS Teaching("
                                "Teaching_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "Teaching TEXT)")

            self.cursor.execute("CREATE TABLE IF NOT EXISTS Faculty_Teaching("
                                "Faculty_id INTEGER, "
                                "Teaching_id INTEGER, "
                                "FOREIGN KEY(Faculty_id) REFERENCES Faculty(Faculty_id),"
                                "FOREIGN KEY(Teaching_id) REFERENCES Teaching(Teaching_id))")
            self.conn.commit()
        except Exception as e:
            print("Error in Creating Tables:", e)