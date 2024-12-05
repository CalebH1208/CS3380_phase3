import sqlite3

connection = sqlite3.connect("project_database.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS TEAM_MEMBER (
    Member_ID INTEGER PRIMARY KEY,
    Email TEXT NOT NULL UNIQUE,
    Phone INTEGER,
    Name TEXT NOT NULL
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS SUB_TEAM (
    Team_ID INTEGER PRIMARY KEY,
    Description TEXT NOT NULL,
    Responsibilities TEXT,
    Team_Lead INTEGER NOT NULL,
    FOREIGN KEY (Team_Lead) REFERENCES TEAM_MEMBER(Member_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PROJECT (
    Project_ID INTEGER PRIMARY KEY,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    In_Use BOOLEAN NOT NULL,
    Owner INTEGER NOT NULL,
    FOREIGN KEY (Owner) REFERENCES TEAM_MEMBER(Member_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS MATERIALS (
    Name TEXT PRIMARY KEY NOT NULL,
    Uses INTEGER,
    Needs INTEGER,
    Link TEXT,
    Material_Type TEXT,
    Description TEXT,
    FOREIGN KEY (Uses) REFERENCES PROJECT(Project_ID),
    FOREIGN KEY (Needs) REFERENCES MAINTENANCE_PROCEDURE(Procedure_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS MAINTENANCE_PROCEDURE (
    Procedure_ID INTEGER PRIMARY KEY,
    Description TEXT NOT NULL,
    Last_Edited DATE NOT NULL,
    Maintainer INTEGER NOT NULL,
    FOREIGN KEY (Maintainer) REFERENCES TEAM_MEMBER(Member_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS DIMENSIONS (
    Material TEXT NOT NULL,
    Dimensions TEXT NOT NULL,
    FOREIGN KEY (Material) REFERENCES MATERIALS(Name)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS OUTSIDE_RESEARCH (
    Research INTEGER,
    Name TEXT PRIMARY KEY,
    Description TEXT,
    Link TEXT,
    Reference_ID INTEGER,
    FOREIGN KEY (Research) REFERENCES PROJECT(Project_ID),
    FOREIGN KEY (Reference_ID) REFERENCES MAINTENANCE_PROCEDURE(Procedure_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PROJECT_MEMBERS (
    Project INTEGER NOT NULL,
    Member INTEGER NOT NULL,
    FOREIGN KEY (Project) REFERENCES PROJECT(Project_ID),
    FOREIGN KEY (Member) REFERENCES TEAM_MEMBER(Member_ID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PROCEDURE_CONTRIBUTERS (
    Procedure INTEGER NOT NULL,
    Member INTEGER NOT NULL,
    FOREIGN KEY (Procedure) REFERENCES MAINTENANCE_PROCEDURE(Procedure_ID),
    FOREIGN KEY (Member) REFERENCES TEAM_MEMBER(Member_ID)
);
""")

connection.commit()
connection.close()

print("Database schema created successfully.")
