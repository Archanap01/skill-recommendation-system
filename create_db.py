import sqlite3
import os

if not os.path.exists("database"):
    os.makedirs("database")

conn = sqlite3.connect("database/skill_data.db")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS user_skills;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS accounts;
""")

cursor.execute("""
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
""")

cursor.execute("""
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    skill_id INTEGER,
    platform TEXT NOT NULL,
    url TEXT NOT NULL,
    timeline TEXT,
    cost TEXT,
    level TEXT,
    instructor TEXT,
    FOREIGN KEY(skill_id) REFERENCES skills(id)
);
""")

cursor.execute("""
CREATE TABLE user_skills (
    user_id INTEGER,
    skill_id INTEGER,
    PRIMARY KEY (user_id, skill_id),
    FOREIGN KEY(user_id) REFERENCES accounts(id),
    FOREIGN KEY(skill_id) REFERENCES skills(id)
);
""")

# Insert skills with IDs starting from 1
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
print("Database schema created and skills inserted.")
