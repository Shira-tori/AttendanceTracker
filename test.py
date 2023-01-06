import mysql.connector

mydb = mysql.connector.connect(
    user='root',
    host='localhost',
    database='pr2',
    port=3306
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE TABLE students (name VARCHAR(50) NOT NULL, section VARCHAR(50) NOT NULL, grade SMALLINT NOT NULL, lrn BIGINT NOT NULL, password VARCHAR(50) NOT NULL, studentID int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
# mycursor.execute("DESCRIBE students")
# mycursor.execute("INSERT INTO students (name, section, grade, lrn, password) VALUES (%s, %s, %s, %s, %s)", ("SEAN DOMINIC FERNANDEZ", "ICT", "12", "136886100309", "hatdog"))
# mydb.commit()
mycursor.execute("SELECT * FROM students_tbl")
result = mycursor.fetchall()

with open("ICT STUDENTS.txt") as f:

    i = 1
    for x in f:
        surname = x.strip().split(", ")
        if len(surname) == 3:
            fullname = surname[0] + ", " + surname[1] + " " + surname[2]
            password = surname[1] + " " + surname[2]
            print(i)
            mycursor.execute(
                f"UPDATE students_tbl SET NAME = '{fullname}' WHERE student_id = {i}")
        else:
            fullname = surname[0] + ", " + surname[1]
            print(i)
            mycursor.execute(
                f"UPDATE students_tbl SET NAME = '{fullname}' WHERE student_id = {i}")
        i += 1
        mydb.commit()
        # mycursor.execute(f"UPDATE students_tbl SET fullname = {x} WHERE username = {x}")
        # mydb.commit()
