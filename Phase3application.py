import sqlite3

# Connect to SQLite database
def connect_to_database():
    try:
        conn = sqlite3.connect('project_database.db')
        print("Connected to the database successfully.")
        return conn
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None

# Placeholder function definitions
def create_project_and_assign_team_members(conn):
    """
    Creates a new project and assigns team members to it.
    """
    cursor = conn.cursor()

    # Step 1: Input and create a new project
    print("\n--- Create New Project ---")
    project_name = input("Enter the project name: ").strip()
    start_date = input("Enter the project start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter the project end date (YYYY-MM-DD): ").strip()
    in_use = input("Is the project currently in use? (yes/no): ").strip().lower() == "yes"
    owner_id = input("Enter the owner ID (team member responsible): ").strip()

    # Verify the owner exists
    cursor.execute("SELECT * FROM TEAM_MEMBER WHERE Member_ID = ?", (owner_id,))
    owner = cursor.fetchone()
    if not owner:
        print(f"No team member found with ID {owner_id}. Project creation aborted.")
        return

    # Insert the new project
    cursor.execute("""
        INSERT INTO PROJECT (Start_Date, End_Date, In_Use, Owner)
        VALUES (?, ?, ?, ?)
    """, (start_date, end_date, in_use, owner_id))
    project_id = cursor.lastrowid
    print(f"Project '{project_name}' created with ID {project_id}.")

    # Step 2: Assign team members to the project
    print("\n--- Assign Team Members ---")
    team_member_ids = input("Enter a comma-separated list of team member IDs to assign to this project: ").split(",")
    team_member_ids = [member_id.strip() for member_id in team_member_ids]

    for member_id in team_member_ids:
        # Verify the team member exists
        cursor.execute("SELECT * FROM TEAM_MEMBER WHERE Member_ID = ?", (member_id,))
        team_member = cursor.fetchone()
        if not team_member:
            print(f"No team member found with ID {member_id}. Skipping assignment.")
            continue

        # Add team member to project_members table
        cursor.execute("""
            INSERT INTO PROJECT_MEMBERS (Project, Member)
            VALUES (?, ?)
        """, (project_id, member_id))
        print(f"Team member ID {member_id} assigned to project ID {project_id}.")

    # Step 3: Display confirmation and project details
    print("\n--- Project Details ---")
    print(f"Project ID: {project_id}")
    print(f"Start Date: {start_date}")


def track_materials_for_project(conn):
    """
    Tracks materials for a specified project, adding new materials if necessary.
    """
    cursor = conn.cursor()

    # Step 1: Retrieve and display available projects
    cursor.execute("SELECT Project_ID, Start_Date, End_Date, In_Use, Owner FROM PROJECT")
    projects = cursor.fetchall()
    if not projects:
        print("No projects available in the database.")
        return

    print("\nAvailable Projects:")
    for project in projects:
        print(f"ID: {project[0]}, Start Date: {project[1]}, End Date: {project[2]}, In Use: {bool(project[3])}, Owner ID: {project[4]}")

    project_id = input("\nEnter the Project ID to track materials for: ")

    # Verify the project exists
    cursor.execute("SELECT * FROM PROJECT WHERE Project_ID = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        print(f"No project found with ID {project_id}.")
        return

    print(f"\nTracking materials for Project ID {project_id}.")

    # Step 2: Handle materials
    materials_input = input("Enter a comma-separated list of materials (format: name|material_type|description|link): ").split(",")
    materials = [material.strip().split("|") for material in materials_input]

    for material in materials:
        if len(material) != 4:
            print(f"Skipping invalid material input: {'|'.join(material)}")
            continue

        name, material_type, description, link = map(str.strip, material)

        # Check if the material exists
        cursor.execute("SELECT Name FROM MATERIALS WHERE Name = ?", (name,))
        if not cursor.fetchone():
            # Insert the material into the database
            cursor.execute("""
                INSERT INTO MATERIALS (Name, Material_Type, Description, Link, Uses)
                VALUES (?, ?, ?, ?, ?)
            """, (name, material_type, description, link, project_id))
            print(f"Material '{name}' added to MATERIALS table.")

        # Link the material to the project
        cursor.execute("""
            UPDATE MATERIALS SET Uses = ? WHERE Name = ?
        """, (project_id, name))
        print(f"Material '{name}' linked to Project ID {project_id}.")

    # Step 3: Display the list of materials associated with the project
    print("\nMaterials associated with the project:")
    cursor.execute("""
        SELECT Name, Material_Type, Description, Link FROM MATERIALS WHERE Uses = ?
    """, (project_id,))
    materials = cursor.fetchall()

    for material in materials:
        print(f"Name: {material[0]}, Type: {material[1]}, Description: {material[2]}, Link: {material[3]}")

    conn.commit()
    cursor.close()


def track_outside_resources_for_project(conn):
    """
    Tracks outside resources for a specified project, adding new resources if necessary.
    """
    cursor = conn.cursor()

    # Step 1: Retrieve the project
    cursor.execute("SELECT Project_ID, Start_Date, End_Date, In_Use, Owner FROM PROJECT")
    projects = cursor.fetchall()
    if not projects:
        print("No projects available in the database.")
        return

    print("\nAvailable Projects:")
    for project in projects:
        print(f"ID: {project[0]}, Start Date: {project[1]}, End Date: {project[2]}, In Use: {bool(project[3])}, Owner ID: {project[4]}")

    project_id = input("\nEnter the Project ID to track resources for: ")

    # Verify the project exists
    cursor.execute("SELECT * FROM PROJECT WHERE Project_ID = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        print(f"No project found with ID {project_id}.")
        return

    print(f"\nTracking resources for Project ID {project_id}.")

    # Step 2: Handle outside resources
    resources_input = input("Enter a comma-separated list of resources (format: name|description|link): ").split(",")
    resources = [resource.strip().split("|") for resource in resources_input]

    for resource in resources:
        if len(resource) != 3:
            print(f"Skipping invalid resource input: {'|'.join(resource)}")
            continue

        name, description, link = map(str.strip, resource)

        # Check if the resource exists
        cursor.execute("SELECT Name FROM OUTSIDE_RESEARCH WHERE Name = ?", (name,))
        if not cursor.fetchone():
            # Insert the resource into the database
            cursor.execute("""
                INSERT INTO OUTSIDE_RESEARCH (Name, Description, Link, Research)
                VALUES (?, ?, ?, ?)
            """, (name, description, link, project_id))
            print(f"Resource '{name}' added to OUTSIDE_RESEARCH table.")

        # Link the resource to the project
        cursor.execute("""
            UPDATE OUTSIDE_RESEARCH SET Research = ? WHERE Name = ?
        """, (project_id, name))
        print(f"Resource '{name}' linked to Project ID {project_id}.")

    # Step 3: Display the list of resources associated with the project
    print("\nResources associated with the project:")
    cursor.execute("""
        SELECT Name, Description, Link FROM OUTSIDE_RESEARCH WHERE Research = ?
    """, (project_id,))
    resources = cursor.fetchall()

    for resource in resources:
        print(f"Name: {resource[0]}, Description: {resource[1]}, Link: {resource[2]}")

    conn.commit()
    cursor.close()


def create_maintenance_procedure_with_resources_and_materials(conn):
    """
    Creates a new maintenance procedure, associates materials and resources, and displays details.
    """
    cursor = conn.cursor()

    # Step 1: Gather input for the new maintenance procedure
    procedure_name = input("Enter the name of the maintenance procedure: ")
    maintainer_id = input("Enter the Maintainer ID: ")
    last_edited_date = input("Enter the last edited date (YYYY-MM-DD): ")

    # Insert the new maintenance procedure into the database
    cursor.execute("""
        INSERT INTO MAINTENANCE_PROCEDURE (Description, Last_Edited, Maintainer)
        VALUES (?, ?, ?)
    """, (procedure_name, last_edited_date, maintainer_id))
    procedure_id = cursor.lastrowid  # Retrieve the auto-generated Procedure_ID

    print(f"\nMaintenance Procedure '{procedure_name}' created with ID {procedure_id}.\n")

    # Step 2: Handle materials association
    materials_list = input("Enter a comma-separated list of materials (e.g., material1, material2): ").split(",")
    for material in map(str.strip, materials_list):
        # Check if material exists
        cursor.execute("SELECT Name FROM MATERIALS WHERE Name = ?", (material,))
        if not cursor.fetchone():
            # Insert new material if not exists
            cursor.execute("""
                INSERT INTO MATERIALS (Name, Uses, Needs)
                VALUES (?, NULL, ?)
            """, (material, procedure_id))  # `Uses` is set to NULL since it's unrelated to projects.
            print(f"Material '{material}' added to MATERIALS table.")

        # Link material to the maintenance procedure
        cursor.execute("""
            UPDATE MATERIALS SET Needs = ? WHERE Name = ?
        """, (procedure_id, material))
        print(f"Material '{material}' linked to Maintenance Procedure ID {procedure_id}.")

    # Step 3: Handle outside resources association
    resources_list = input("Enter a comma-separated list of resources (e.g., resource1, resource2): ").split(",")
    for resource in map(str.strip, resources_list):
        # Check if resource exists
        cursor.execute("SELECT Name FROM OUTSIDE_RESEARCH WHERE Name = ?", (resource,))
        if not cursor.fetchone():
            # Insert new resource if not exists
            cursor.execute("""
                INSERT INTO OUTSIDE_RESEARCH (Name, Reference_ID)
                VALUES (?, ?)
            """, (resource, procedure_id))
            print(f"Resource '{resource}' added to OUTSIDE_RESEARCH table.")

        # Link resource to the maintenance procedure
        cursor.execute("""
            UPDATE OUTSIDE_RESEARCH SET Reference_ID = ? WHERE Name = ?
        """, (procedure_id, resource))
        print(f"Resource '{resource}' linked to Maintenance Procedure ID {procedure_id}.")

    # Step 4: Display confirmation
    print("\nMaintenance Procedure Details:")
    print(f"ID: {procedure_id}")
    print(f"Name: {procedure_name}")
    print("Materials:", ", ".join(materials_list))
    print("Resources:", ", ".join(resources_list))

    conn.commit()
    cursor.close()


def search_responsibilities_by_sub_team(conn):
    """
    Searches and displays the responsibilities of a selected sub-team.

    Steps:
    1. Display all sub-teams.
    2. Prompt the user to select a sub-team by its ID.
    3. Retrieve and display the responsibilities for the selected sub-team.
    """
    cursor = conn.cursor()

    # Step 1: Display all available sub-teams
    print("\nAvailable Sub-Teams:")
    cursor.execute("SELECT Team_ID, Description FROM SUB_TEAM")
    sub_teams = cursor.fetchall()
    if not sub_teams:
        print("No sub-teams found.")
        return

    for team in sub_teams:
        print(f"Team ID: {team[0]}, Description: {team[1]}")

    # Step 2: Prompt the user for Sub-Team ID
    sub_team_id = input("\nEnter Sub-Team ID to view responsibilities: ")

    # Step 3: Verify the Sub-Team exists and retrieve its responsibilities
    cursor.execute("SELECT Responsibilities FROM SUB_TEAM WHERE Team_ID = ?", (sub_team_id,))
    result = cursor.fetchone()
    if result:
        responsibilities = result[0]
        print(f"\nResponsibilities for Sub-Team ID {sub_team_id}:")
        print(responsibilities if responsibilities else "No responsibilities assigned.")
    else:
        print("Invalid Sub-Team ID. Please try again.")

    cursor.close()


def retrieve_contact_info_for_project_or_maintenance_procedure(conn):
    """
    Retrieves and displays contact information for team members assigned to a project or maintenance procedure.

    Input:
        - Entity ID (project ID or maintenance procedure ID)
        - Entity type ("project" or "maintenance procedure")

    Features:
        - Lists all available projects and maintenance procedures for user reference.
    """
    print("\n=== Retrieve Contact Info for Project or Maintenance Procedure ===")

    try:
        cursor = conn.cursor()

        # Display all projects
        print("\nAvailable Projects:")
        cursor.execute("SELECT * FROM project;")
        projects = cursor.fetchall()
        if projects:
            for project in projects:
                print(f"ID: {project[0]}, Name: {project[1]}, Start: {project[2]}, End: {project[3]}")
        else:
            print("No projects available.")

        # Display all maintenance procedures
        print("\nAvailable Maintenance Procedures:")
        cursor.execute("SELECT * FROM maintenance_procedure;")
        procedures = cursor.fetchall()
        if procedures:
            for procedure in procedures:
                print(f"ID: {procedure[0]}, Name: {procedure[1]}, Start: {procedure[2]}, End: {procedure[3]}")
        else:
            print("No maintenance procedures available.")

        # Prompt user for inputs
        print("\nExample: Enter Entity ID as 101 and Entity type as 'project' or 'maintenance procedure'")
        entity_id = input("Enter the Entity ID: ").strip()
        entity_type = input("Enter the Entity Type (project or maintenance procedure): ").strip().lower()

        if entity_type == "project":
            # Retrieve project information
            cursor.execute("SELECT * FROM project WHERE Project_ID = ?;", (entity_id,))
            project = cursor.fetchone()
            if not project:
                print(f"No project found with ID {entity_id}.")
                return

            print(f"\nProject Details: {project}")

            # Retrieve team members assigned to the project
            cursor.execute("SELECT Member FROM project_members WHERE Project = ?;", (entity_id,))
            team_members = cursor.fetchall()
            if not team_members:
                print(f"No team members found for project ID {entity_id}.")
                return

            print("\nTeam Member Contact Information:")
            for member in team_members:
                cursor.execute("SELECT * FROM team_member WHERE Member_ID = ?;", (member[0],))
                contact_info = cursor.fetchone()
                if contact_info:
                    print(contact_info)
                else:
                    print(f"No contact information found for team member ID {member[0]}.")

        elif entity_type == "maintenance procedure":
            # Retrieve maintenance procedure information
            cursor.execute("SELECT * FROM maintenance_procedure WHERE Procedure_ID = ?;", (entity_id,))
            procedure = cursor.fetchone()
            if not procedure:
                print(f"No maintenance procedure found with ID {entity_id}.")
                return

            print(f"\nMaintenance Procedure Details: {procedure}")

            # Retrieve team members assigned to the maintenance procedure
            cursor.execute("SELECT Member FROM PROCEDURE_CONTRIBUTERS WHERE Procedure = ?;", (entity_id,))
            team_members = cursor.fetchall()
            if not team_members:
                print(f"No team members found for maintenance procedure ID {entity_id}.")
                return

            print("\nTeam Member Contact Information:")
            for member in team_members:
                cursor.execute("SELECT * FROM team_member WHERE Member_ID = ?;", (member[0],))
                contact_info = cursor.fetchone()
                if contact_info:
                    print(contact_info)
                else:
                    print(f"No contact information found for team member ID {member[0]}.")

        else:
            print("Invalid entity type. Please enter 'project' or 'maintenance procedure'.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def add_item(conn):
    """
    Adds an item to a specified table in the database.
    Prompts the user for column values to insert into the table.
    """
    print("\n=== Add Item to Table ===")
    print("Available tables: SUB_TEAM, TEAM_MEMBER, PROJECT, MATERIALS, MAINTENANCE_PROCEDURE, DIMENSIONS, OUTSIDE_RESEARCH, PROJECT_MEMBERS, PROCEDURE_CONTRIBUTORS")
    print("Example: To add a new team member, specify: TEAM_MEMBER and provide values for Member_ID, Email, Phone_#, Name")

    # Prompt user for table name
    table = input("Enter the table name: ").strip()

    try:
        cursor = conn.cursor()
        # Retrieve column names for the specified table
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()

        if not columns:
            print(f"Table '{table}' does not exist.")
            return

        column_names = [col[1] for col in columns]
        print(f"\nColumns in table '{table}': {', '.join(column_names)}")

        # Prompt user for values for each column
        values = []
        for column in column_names:
            value = input(f"Enter value for '{column}' (leave blank for NULL): ").strip()
            values.append(value if value else None)

        # Construct the INSERT statement
        placeholders = ', '.join(['?'] * len(column_names))
        query = f"INSERT INTO {table} ({', '.join(column_names)}) VALUES ({placeholders});"
        print(f"Executing query: {query} with values {values}")  # Debugging info
        cursor.execute(query, values)
        conn.commit()

        print(f"Successfully added a new item to table '{table}'.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def remove_item(conn):
    """
    Removes an item from a specified table in the database.
    Displays the contents of the table for reference before and after removal.
    """
    print("\n=== Remove Item from Table ===")
    print("Available tables: SUB_TEAM, TEAM_MEMBER, PROJECT, MATERIALS, MAINTENANCE_PROCEDURE, DIMENSIONS, OUTSIDE_RESEARCH, PROJECT_MEMBERS, PROCEDURE_CONTRIBUTORS")
    print("Example: To remove a team member with ID 5, specify: TEAM_MEMBER and 'Member_ID = 5'")

    # Prompt user for table name
    table = input("Enter the table name: ").strip()

    try:
        # Display the contents of the table
        cursor = conn.cursor()
        print(f"\nContents of table '{table}':")
        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]  # Get column headers

        if rows:
            # Print the table contents
            print(f"{' | '.join(column_names)}")
            print("-" * (len(column_names) * 15))
            for row in rows:
                print(" | ".join(map(str, row)))
        else:
            print(f"Table '{table}' is empty.")
        
        # Prompt user for condition
        condition = input(f"\nEnter the condition for deletion (e.g., 'Column_Name = Value'): ").strip()
        
        # Execute the DELETE statement
        query = f"DELETE FROM {table} WHERE {condition};"
        print(f"Executing query: {query}")  # Debugging info
        cursor.execute(query)
        conn.commit()

        # Feedback to user
        if cursor.rowcount > 0:
            print(f"Successfully removed {cursor.rowcount} item(s) from table '{table}'.")
        else:
            print(f"No items matched the condition in table '{table}'.")

        # Display the updated contents of the table
        print(f"\nUpdated contents of table '{table}':")
        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()

        if rows:
            print(f"{' | '.join(column_names)}")
            print("-" * (len(column_names) * 15))
            for row in rows:
                print(" | ".join(map(str, row)))
        else:
            print(f"Table '{table}' is now empty.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def exit_program(conn):
    """
    Exits the program and closes the database connection.
    """
    print("\nExiting program... Goodbye!")
    if conn:
        conn.close()
    exit()

# Main menu
def main():
    conn = connect_to_database()
    if not conn:
        return  # Exit if the database connection fails

    while True:
        print("\n=== Project Management Application ===")
        print("1. Create Project and Assign Team Members")
        print("2. Track Materials for Project")
        print("3. Track Outside Resources for Project")
        print("4. Create Maintenance Procedure with Resources and Materials")
        print("5. Search Responsibilities by Sub-Team")
        print("6. Retrieve Contact Info for Project or Maintenance Procedure")
        print("7. Add Item to Table")
        print("8. Remove Item from Table")
        print("9. Exit Program")

        choice = input("Enter your choice (1-9): ")
        if choice == '1':
            create_project_and_assign_team_members(conn)
        elif choice == '2':
            track_materials_for_project(conn)
        elif choice == '3':
            track_outside_resources_for_project(conn)
        elif choice == '4':
            create_maintenance_procedure_with_resources_and_materials(conn)
        elif choice == '5':
            search_responsibilities_by_sub_team(conn)
        elif choice == '6':
            retrieve_contact_info_for_project_or_maintenance_procedure(conn)
        elif choice == '7':
            add_item(conn)
        elif choice == '8':
            remove_item(conn)
        elif choice == '9':
            exit_program(conn)
            break
        else:
            print("Invalid choice. Please try again.")

    # Close the database connection before exiting
    conn.close()

if __name__ == "__main__":
    main()
