import dbConnection.db_connection as conn

class CreateTable():
    def __init__(self):
        self.cursor = conn.SQLConnection.getConnection().cursor()

    def create_tables(self):
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

        self.cursor.execute("CREATE TABLE IF NOT EXISTS Faculty_Specialization("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "Faculty_id INTEGER, "
                            "Specialization TEXT, "
                            "FOREIGN KEY(Faculty_id) REFERENCES Faculty(Faculty_id)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS Faculty_Research("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "Faculty_id INTEGER, "
                            "Research TEXT, "
                            "FOREIGN KEY(Faculty_id) REFERENCES Faculty(Faculty_id)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS Faculty_Teaching("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "Faculty_id INTEGER, "
                            "Teaching TEXT, "
                            "FOREIGN KEY(Faculty_id) REFERENCES Faculty(Faculty_id)")