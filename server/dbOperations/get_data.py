from typing import List


class GetData:
    def __init__(self,conn):
        self.cursor = conn.cursor()

    def get_data(self):
        result = []
        try:
            self.cursor.execute("SELECT F.Faculty_id,F.Name,F.Phone,F.Email,F.FacultyWebsite,F.Bio,F.Education,"
                                "F.Education_Institute,F.Education_City,F.Education_country,F.Teaching_Institute,"
                                "F.Faculty_Block,F.Room_No,S.Specialization,R.Research,T.Teaching FROM Faculty F "
                                "left join Faculty_Specialization FS on F.Faculty_id = FS.Faculty_id "
                                "left join Faculty_Research FR on F.Faculty_id = FR.Faculty_id "
                                "left join Faculty_Teaching FT on F.Faculty_id = FT.Faculty_id "
                                "left join Specialization S on FS.Specialization_id = S.Specialization_id "
                                "left join Research R on R.Research_id = FR.Research_id "
                                "left join Teaching T on T.Teaching_id = FT.Teaching_id ")
            rows = self.cursor.fetchall()

            data = {}
            for row in rows:
                (
                    faculty_id,name, phone, email, website, bio, education,
                    edu_inst, edu_city, edu_country, teaching_inst,
                    block, room_no, specialization, research, teaching
                ) = row

                if faculty_id not in data:
                    data[faculty_id] = {
                        "Faculty_id": faculty_id,
                        "Name": name,
                        "Phone": phone,
                        "Email": email,
                        "FacultyWebsite": website,
                        "Bio": bio,
                        "Education": education,
                        "Education_Institute": edu_inst,
                        "Education_City": edu_city,
                        "Education_Country": edu_country,
                        "Teaching_Institute": teaching_inst,
                        "Faculty_Block": block,
                        "Room_No": room_no,
                        "Specializations": set(),
                        "Researches": set(),
                        "Teachings": set()
                    }

                if specialization:
                    data[faculty_id]["Specializations"].add(specialization)
                
                if research:
                    data[faculty_id]["Researches"].add(research)
                
                if teaching:
                    data[faculty_id]["Teachings"].add(teaching)

            for faculty in data.values():
                faculty["Specializations"] = list(faculty["Specializations"])
                faculty["Researches"] = list(faculty["Researches"])
                faculty["Teachings"] = list(faculty["Teachings"])
                result.append(faculty)
        except Exception as e:
            return {"Error": str(e)}
        return result
    
    def get_faculty_by_ids(self, faculty_ids: List[int]):
        """
        Fetch faculty details for the given list of faculty IDs.
        
        Args:
            faculty_ids: List of faculty IDs to fetch details for.
        """
        faculties = []
        for fid in faculty_ids:
            self.cursor.execute("""
                SELECT F.Faculty_id,F.Name,F.Phone,F.Email,F.FacultyWebsite,F.Bio,F.Education,
                                F.Education_Institute,F.Education_City,F.Education_country,F.Teaching_Institute,
                                F.Faculty_Block,F.Room_No,S.Specialization,R.Research,T.Teaching FROM Faculty F 
                                left join Faculty_Specialization FS on F.Faculty_id = FS.Faculty_id 
                                left join Faculty_Research FR on F.Faculty_id = FR.Faculty_id 
                                left join Faculty_Teaching FT on F.Faculty_id = FT.Faculty_id 
                                left join Specialization S on FS.Specialization_id = S.Specialization_id 
                                left join Research R on R.Research_id = FR.Research_id 
                                left join Teaching T on T.Teaching_id = FT.Teaching_id  
                WHERE F.Faculty_id = ?
            """, (fid,))
            result = self.cursor.fetchall()
            if result:
                if result:
                    first_row = result[0]
                    specializations = set()
                    research_areas = set()
                    teaching_areas = set()

                    for row in result:
                        if row[13]:  # Specialization
                            specializations.add(row[13])
                        if row[14]:  # Research
                            research_areas.add(row[14])
                        if row[15]:  # Teaching
                            teaching_areas.add(row[15])
                    faculties.append({
                        'id': first_row[0],                    # Faculty_id
                        'name': first_row[1],                  # Name
                        'phone': first_row[2],                 # Phone
                        'email': first_row[3],                 # Email
                        'website': first_row[4],               # FacultyWebsite
                        'bio': first_row[5],                   # Bio
                        'education': first_row[6],             # Education
                        'education_institute': first_row[7],   # Education_Institute
                        'education_city': first_row[8],        # Education_City
                        'education_country': first_row[9],     # Education_country
                        'teaching_institute': first_row[10],   # Teaching_Institute
                        'faculty_block': first_row[11],        # Faculty_Block
                        'room_number': first_row[12],          # Room_No
                        'specialization': list(specializations),       # Specialization ← WAS result[2]
                        'research': list(research_areas),             # Research
                        'teaching': list(teaching_areas)              # Teaching ← WAS result[3]
                    })
        return faculties