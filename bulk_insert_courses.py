import sqlite3

conn = sqlite3.connect('database/skill_data.db')
cursor = conn.cursor()

courses = [
    # Programming (skill_id=1)
    ("CS50: Introduction to Computer Science", 1, "HarvardX (edX)", "https://cs50.harvard.edu/x/", "11 weeks", "Free (audit)", "Beginner", "Harvard University"),
    ("Python for Everybody", 1, "Coursera", "https://www.coursera.org/learn/python", "7 weeks", "Free (audit)", "Beginner", "University of Michigan"),
    ("Introduction to Programming with Python", 1, "edX", "https://www.edx.org/professional-certificate/python-basics", "8 weeks", "Free (audit)", "Beginner", "Rice University"),

    # Machine Learning (skill_id=2)
    ("Machine Learning by Andrew Ng", 2, "Coursera", "https://www.coursera.org/learn/machine-learning", "11 weeks", "Free (audit)", "Intermediate", "Stanford University"),
    ("IBM Data Science Professional Certificate", 2, "Coursera", "https://www.coursera.org/professional-certificates/ibm-data-science", "4–6 months", "Free (audit)", "Beginner", "IBM"),

    # Data Science (skill_id=3)
    ("Data Science Specialization", 3, "Coursera", "https://www.coursera.org/specializations/jhu-data-science", "4–6 months", "Free (audit)", "Intermediate", "Johns Hopkins University"),

    # Digital Marketing (skill_id=4)
    ("Digital Marketing Course", 4, "Google Digital Garage", "https://learndigital.withgoogle.com/digitalgarage/course/digital-marketing", "40 hrs", "Free", "Beginner", "Google"),
    ("Social Media Strategy", 4, "HubSpot Academy", "https://academy.hubspot.com/courses/social-media-strategy", "5 hrs", "Free", "Beginner", "HubSpot Academy"),

    # Cloud Computing (AWS, GCP) (skill_id=5)
    ("AWS Cloud Practitioner Essentials", 5, "AWS Training", "https://www.aws.training/Details/Curriculum?id=20685", "6 hrs", "Free", "Beginner", "AWS"),
    ("Google Cloud Fundamentals", 5, "Coursera", "https://www.coursera.org/learn/gcp-fundamentals", "10 hrs", "Free (audit)", "Beginner", "Google Cloud"),

    # UI/UX Design (skill_id=6)
    ("UX Design Fundamentals", 6, "Coursera", "https://www.coursera.org/specializations/ui-ux-design", "4 months", "Free (audit)", "Beginner", "CalArts"),
    ("Intro to UI Design", 6, "Udacity", "https://www.udacity.com/course/intro-to-the-design-of-everyday-things--ud509", "3–4 hrs", "Free", "Beginner", "Udacity"),

    # Cybersecurity (skill_id=7)
    ("Introduction to Cybersecurity", 7, "Cisco Networking Academy", "https://skillsforall.com/course/introduction-to-cybersecurity", "6 hrs", "Free", "Beginner", "Cisco"),
    ("Google Cybersecurity Professional Certificate", 7, "Coursera", "https://www.coursera.org/professional-certificates/google-cybersecurity", "6 months", "Free (audit)", "Beginner", "Google"),

    # SQL & Databases (skill_id=8)
    ("SQL for Data Science", 8, "Coursera", "https://www.coursera.org/learn/sql-for-data-science", "4 weeks", "Free (audit)", "Beginner", "UC Davis"),
    ("Advanced SQL Tutorial", 8, "Mode Analytics", "https://mode.com/sql-tutorial/", "Self-paced", "Free", "Intermediate", "Mode Analytics"),

    # Graphic Design (skill_id=9)
    ("Canva Design School", 9, "Canva", "https://www.canva.com/designschool/courses/", "2 hrs", "Free", "Beginner", "Canva"),
    ("Graphic Design for Beginners", 9, "Udemy", "https://www.udemy.com/course/graphic-design-for-beginners/", "3 hrs", "₹499", "Beginner", "Jeremy Deighan"),

    # Artificial Intelligence (skill_id=10)
    ("AI For Everyone", 10, "Coursera", "https://www.coursera.org/learn/ai-for-everyone", "8 hrs", "Free (audit)", "Beginner", "Andrew Ng"),
    ("Deep Learning Specialization", 10, "Coursera", "https://www.coursera.org/specializations/deep-learning", "5 months", "Free (audit)", "Intermediate", "Andrew Ng")
]

cursor.executemany('''
INSERT INTO courses (course_name, skill_id, platform, url, timeline, cost, level, instructor)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', courses)

conn.commit()
conn.close()
print("Courses inserted successfully!")
