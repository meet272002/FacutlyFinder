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
            print(rows)
            for row in rows:
                print(row)
                (
                    faculty_id,name, phone, email, website, bio, education,
                    edu_inst, edu_city, edu_country, teaching_inst,
                    block, room_no, specialization, research, teaching
                ) = row

                if faculty_id not in data:
                    data[faculty_id] = {
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