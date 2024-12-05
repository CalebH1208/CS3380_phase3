import sqlite3
from datetime import datetime, timedelta
import random

# Connect to the SQLite database
conn = sqlite3.connect('project_database.db')
cursor = conn.cursor()

# Helper function to generate random dates
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Populate the tables with synthetic data
try:
    # Fill TEAM_MEMBER
    team_members = [
        (1, "john.doe@example.com", 1234567890, "John Doe"),
        (2, "jane.smith@example.com", 9876543210, "Jane Smith"),
        (3, "bob.brown@example.com", 4567891230, "Bob Brown"),
        (4, "alice.white@example.com", 3216549870, "Alice White")
    ]
    cursor.executemany("INSERT INTO TEAM_MEMBER (Member_ID, Email, Phone, Name) VALUES (?, ?, ?, ?)", team_members)

    # Fill SUB_TEAM
    sub_teams = [
        (1, "Backend Team", "Handle server-side logic", 1),
        (2, "Frontend Team", "Handle UI/UX design", 2)
    ]
    cursor.executemany("INSERT INTO SUB_TEAM (Team_ID, Description, Responsibilities, Team_Lead) VALUES (?, ?, ?, ?)", sub_teams)

    # Fill PROJECT
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)
    projects = [
        (1, random_date(start_date, end_date), random_date(start_date, end_date), random.choice([True, False]), 1),
        (2, random_date(start_date, end_date), random_date(start_date, end_date), random.choice([True, False]), 2)
    ]
    cursor.executemany("INSERT INTO PROJECT (Project_ID, Start_date, End_date, In_use, Owner) VALUES (?, ?, ?, ?, ?)", projects)

    # Fill MATERIALS
    materials = [
        (1, 1, "Material1", "http://example.com/material1", "Type A", "A description of material 1"),
        (1, 2, "Material2", "http://example.com/material2", "Type B", "A description of material 2")
    ]
    cursor.executemany("INSERT INTO MATERIALS (Uses, Needs, Name, Link, Material_type, Description) VALUES (?, ?, ?, ?, ?, ?)", materials)

    # Fill MAINTENANCE_PROCEDURE
    maintenance_procedures = [
        (1, "Procedure for material maintenance", random_date(start_date, end_date), 1),
        (2, "Another procedure", random_date(start_date, end_date), 2)
    ]
    cursor.executemany("INSERT INTO MAINTENANCE_PROCEDURE (Procedure_ID, Description, Last_edited, Maintainer) VALUES (?, ?, ?, ?)", maintenance_procedures)

    # Fill DIMENSIONS
    dimensions = [
        (1, "10x20x30 cm"),
        (2, "50x60x70 cm")
    ]
    cursor.executemany("INSERT INTO DIMENSIONS (Material, Dimensions) VALUES (?, ?)", dimensions)

    # Fill OUTSIDE_RESEARCH
    outside_research = [
        (1, "Research1", "Research about project 1", "http://example.com/research1", 1),
        (2, "Research2", "Research about project 2", "http://example.com/research2", 2)
    ]
    cursor.executemany("INSERT INTO OUTSIDE_RESEARCH (Research, Name, Description, Link, Reference_ID) VALUES (?, ?, ?, ?, ?)", outside_research)

    # Fill PROJECT_MEMBERS
    project_members = [
        (1, 1),
        (1, 2),
        (2, 3),
        (2, 4)
    ]
    cursor.executemany("INSERT INTO PROJECT_MEMBERS (Project, Member) VALUES (?, ?)", project_members)

    # Fill PROCEDURE_CONTRIBUTERS
    procedure_contributors = [
        (1, 1),
        (1, 2),
        (2, 3),
        (2, 4)
    ]
    cursor.executemany("INSERT INTO PROCEDURE_CONTRIBUTERS (Procedure, Member) VALUES (?, ?)", procedure_contributors)

    # Commit the changes
    conn.commit()
    print("Database filled with synthetic data successfully.")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")


finally:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:", tables)

    # Close the database connection
    conn.close()
