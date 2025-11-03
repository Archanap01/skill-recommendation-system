import sqlite3

conn = sqlite3.connect('database/skill_data.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM skills")

skills = [
    ("Programming",),
    ("Machine Learning",),
    ("Data Science",),
    ("Digital Marketing",),
    ("Cloud Computing (AWS, GCP)",),
    ("UI/UX Design",),
    ("Cybersecurity",),
    ("SQL & Databases",),
    ("Graphic Design",),
    ("Artificial Intelligence",)
]
cursor.executemany("INSERT INTO skills (name) VALUES (?)", skills)

conn.commit()
conn.close()
print("Skills inserted successfully!")
