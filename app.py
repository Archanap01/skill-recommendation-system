from flask import Flask, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, SkillSelectionForm
import sqlite3
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with env var or config in production

DB = 'database/skill_data.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    skills = conn.execute("SELECT id, name FROM skills").fetchall()
    conn.close()
    form = SkillSelectionForm()
    # Populate choices dynamically:
    form.interests.choices = [(skill['id'], skill['name']) for skill in skills]
    return render_template('index.html', form=form)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = get_db()
    c = conn.cursor()

    # --- Start of Debugging ---
    print("\n--- NEW RECOMMENDATION REQUEST ---")

    if request.method == 'POST':
        # Get data from the form
        selected_skills = request.form.getlist('interests')
        cost = request.form.get('cost', 'any')
        level = request.form.get('level', 'any')

        print(f"Step 1: Form data received: Skills={selected_skills}, Cost={cost}, Level={level}")

        # Check if any skills were selected
        if not selected_skills:
            print("WARNING: No skills were selected in the form.")
            flash("You must select at least one skill.", "warning")
            return redirect(url_for('index'))

        # Store the user's selected skills in the database
        c.execute("DELETE FROM user_skills WHERE user_id=?", (user_id,))
        for skill_id in selected_skills:
            c.execute("INSERT INTO user_skills (user_id, skill_id) VALUES (?, ?)", (user_id, int(skill_id)))
        conn.commit()
        print(f"Step 2: Database - Stored skill IDs {selected_skills} for user_id {user_id}")
    
    # Fetch the user's skills from the database to build the query
    c.execute("SELECT skill_id FROM user_skills WHERE user_id=?", (user_id,))
    skill_ids_from_db = [row['skill_id'] for row in c.fetchall()]
    
    print(f"Step 3: Database - Fetched skill IDs {skill_ids_from_db} for this user.")

    if not skill_ids_from_db:
        conn.close()
        print("ERROR: No skills found in DB for this user. Cannot recommend courses.")
        flash("No skills saved for your profile. Please select your skills.", "warning")
        return redirect(url_for('index'))

    # Build the main part of the query
    placeholders = ','.join('?' for _ in skill_ids_from_db)
    query = f"SELECT * FROM courses WHERE skill_id IN ({placeholders})"
    params = skill_ids_from_db

    # Add filters to the query if they were submitted
    # Note: We only get cost/level from the POST request in this logic
    if request.method == 'POST':
        if cost != 'any':
            # This logic handles 'Free', 'Free (audit)', and 'Paid' (like '₹499')
            if cost == 'Free':
                 query += " AND cost LIKE ?"
                 params.append('%Free%')
            else: # For 'Paid' filter, find courses that are not free
                 query += " AND cost NOT LIKE ?"
                 params.append('%Free%')

        if level != 'any':
            query += " AND level = ?"
            params.append(level)
    
    print(f"Step 4: Executing SQL Query: {query}")
    print(f"Step 5: With Parameters: {params}")

    c.execute(query, params)
    courses = c.fetchall()
    conn.close()

    print(f"Step 6: Query Result - Found {len(courses)} courses.")
    print("--- END OF REQUEST ---\n")

    return render_template("recommendations.html", courses=courses)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    username = session.get('username')

    conn = get_db()
    c = conn.cursor()

    c.execute("""
        SELECT s.name FROM user_skills us
        JOIN skills s ON us.skill_id = s.id
        WHERE us.user_id=?
    """, (user_id,))
    skills = [row['name'] for row in c.fetchall()]

    if skills:
        c.execute("SELECT skill_id FROM user_skills WHERE user_id=?", (user_id,))
        skill_ids = [row['skill_id'] for row in c.fetchall()]
        placeholders = ','.join('?' for _ in skill_ids)
        c.execute(f"SELECT * FROM courses WHERE skill_id IN ({placeholders})", skill_ids)
        recommended_courses = c.fetchall()
    else:
        recommended_courses = []

    conn.close()
    return render_template("dashboard.html", username=username, skills=skills, recommended_courses=recommended_courses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()
        password = form.password.data

        conn = get_db()
        cur = conn.cursor()

        # Check if username or email already exists
        cur.execute("SELECT id FROM accounts WHERE username=?", (username,))
        if cur.fetchone():
            flash("Username already taken.", "danger")
            conn.close()
            return render_template('register.html', form=form)

        cur.execute("SELECT id FROM accounts WHERE email=?", (email,))
        if cur.fetchone():
            flash("Email already registered.", "danger")
            conn.close()
            return render_template('register.html', form=form)

        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO accounts(username, email, password) VALUES (?, ?, ?)",
                    (username, email, hashed_password))
        conn.commit()
        conn.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM accounts WHERE username=?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
