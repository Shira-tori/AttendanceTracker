import mysql.connector

mydb = mysql.connector.connect(
        user='sql6523636',
        passwd='YQIBTXeknU',
        host='sql6.freemysqlhosting.net',
        database='sql6523636',
        port=3306
    )

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE students (name VARCHAR(50) NOT NULL, section VARCHAR(50) NOT NULL, grade SMALLINT NOT NULL, lrn BIGINT NOT NULL, password VARCHAR(50) NOT NULL, studentID int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
#mycursor.execute("DESCRIBE students")
#mycursor.execute("INSERT INTO students (name, section, grade, lrn, password) VALUES (%s, %s, %s, %s, %s)", ("SEAN DOMINIC FERNANDEZ", "ICT", "12", "136886100309", "hatdog"))
#mydb.commit()
mycursor.execute("SELECT * FROM students")
print(mycursor.fetchone())
