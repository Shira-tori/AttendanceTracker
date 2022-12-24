import mysql.connector

mydb = mysql.connector.connect(
        user='root',
        host='localhost',
        database='pr2',
        port=3306
    )

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE students (name VARCHAR(50) NOT NULL, section VARCHAR(50) NOT NULL, grade SMALLINT NOT NULL, lrn BIGINT NOT NULL, password VARCHAR(50) NOT NULL, studentID int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
#mycursor.execute("DESCRIBE students")
#mycursor.execute("INSERT INTO students (name, section, grade, lrn, password) VALUES (%s, %s, %s, %s, %s)", ("SEAN DOMINIC FERNANDEZ", "ICT", "12", "136886100309", "hatdog"))
#mydb.commit()
mycursor.execute("SELECT * FROM students_tbl")
result = mycursor.fetchall()

for x in range(37):
    mycursor.execute(f"UPDATE students_tbl SET student_id = {x+1} WHERE student_id = {result[x][2]}")
    mydb.commit()
    