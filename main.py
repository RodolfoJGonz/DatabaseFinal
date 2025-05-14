# Group:
# Rodolfo Gonzalez
# Hector Moreno

import sqlite3
import csv

##### MAKE SURE YOU HAVE CSV FILES IN A ./Data DIRECTORY #####
conn = sqlite3.connect("robot.db")
cursor = conn.cursor()

# Robots Table
print("Task 2")
exist = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='Robots'"
).fetchone()

if exist is not None:
    print("Robots Table exists")
else:
    print("Creating Robots Table")
    cursor.execute("""CREATE TABLE Robots
    (
        Rid     INTEGER NOT NULL,
        name    CHAR(20),
        PRIMARY KEY (Rid)
    );""")
## Populate Robots table
count = cursor.execute("SELECT COUNT(Rid) FROM Robots").fetchone()
if count[0] == 0:
    with open("./Data/robot.csv") as file:
        reader = csv.DictReader(file, fieldnames=["Rid", "name"])
        for row in reader:
            cursor.execute(
                "INSERT INTO Robots (Rid, name) VALUES (?,?)",
                [int(row["Rid"]), row["name"]],
            )
        print("Populating Robots Table")
        conn.commit()
else:
    print("Robots Table already populated")

# Coordinates Table (weak entity)

exist = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='Coordinates'"
).fetchone()

if exist is not None:
    print("Coordinates Table exists")
else:
    print("Creating Coordinates Table")
    cursor.execute("""CREATE TABLE Coordinates
    (
        timestamp   INTEGER NOT NULL,
        x_axis      FLOAT,
        y_axis      FLOAT,
        Rid         INTEGER NOT NULL,
        PRIMARY KEY (Rid,timestamp),
        FOREIGN KEY (Rid) REFERENCES Robots(Rid)
    );""")

# Populating Coordinates Table

count = cursor.execute("SELECT COUNT(timestamp) FROM Coordinates").fetchone()
if count[0] == 0:
    for i in range(5):
        with open(f"./Data/t{i + 1}.csv") as file:
            row_count = 0
            reader = csv.DictReader(file, fieldnames=["x_axis", "y_axis"])
            for row in reader:
                cursor.execute(
                    "INSERT INTO Coordinates (timestamp,x_axis,y_axis,Rid) VALUES (?,?,?,?)",
                    [row_count, float(row["x_axis"]), float(row["y_axis"]), i + 1],
                )
                row_count += 1
            conn.commit()
    print("Coordinates table populated")

else:
    print("Coordinates Table already populated")


# Interval Table
exist = cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='Intervals'"
).fetchone()

if exist is not None:
    print("Intervals Table exists")
else:
    print("Creating Intervals Table")
    cursor.execute("""CREATE TABLE Intervals
    (
        Iid         INTEGER NOT NULL,
        start       INTEGER,
        end         INTEGER,
        event_type  CHAR(15),
        PRIMARY KEY(Iid AUTOINCREMENT)
    );""")

# Populating Intervals Table
count = cursor.execute("SELECT COUNT(Iid) FROM Intervals").fetchone()
if count[0] == 0:
    with open("./Data/interval.csv") as file:
        reader = csv.DictReader(file, fieldnames=["start", "end", "event_type"])
        for row in reader:
            cursor.execute(
                "INSERT INTO Intervals (start, end, event_type) VALUES (?,?,?)",
                [int(row["start"]), int(row["end"]), row["event_type"]],
            )

        print("Populating Intervals Table")
        conn.commit()
else:
    print("Intervals Table already populated")
# Maybe we make a CoordinateIntervalMapping Table (BIG MAYBE)


### TASK 3 ###
# 1. A table consists of the names of robots and the maximal x-axis, minimum x-axis reached by this robot.
print("\n\nTask 3.1")
statement = """SELECT name, MAX(x_axis), MIN(x_axis)
FROM Robots NATURAL JOIN Coordinates
GROUP BY name;"""

cursor.execute(statement)

res = cursor.execute(statement)

relational_schema = [x[0] for x in res.description]

print(relational_schema)
print("-------------------------------------")
for x in res:
    print(x)

# 2. A table consists of the names of robots and the maximal y-axis, minimum y-axis reached by this robot
print("\n\nTask 3.2")
statement = """SELECT name, MAX(y_axis), MIN(y_axis)
FROM Robots NATURAL JOIN Coordinates
GROUP BY name;"""

cursor.execute(statement)

res = cursor.execute(statement)

relational_schema = [x[0] for x in res.description]

print(relational_schema)
print("-------------------------------------")
for x in res:
    print(x)


### TASK 4 ###

# 1.Regions where Astro and IamHuman are close (within 1 cm)
print("\n\nTask 4.1")
statement = """
SELECT
    MIN(MIN(c1.x_axis),MIN(c2.x_axis)) AS x_min,
    MAX(MAX(c1.x_axis),MAX(c2.x_axis)) AS x_max,
    MIN(MIN(c1.y_axis),MIN(c2.y_axis)) AS y_min,
    MAX(MAX(c1.y_axis),MAX(c2.y_axis)) AS y_max
FROM Coordinates c1
JOIN Coordinates c2 ON c1.timestamp = c2.timestamp
WHERE c1.Rid = (SELECT Rid FROM Robots WHERE name = 'Astro')
  AND c2.Rid = (SELECT Rid FROM Robots WHERE name = 'IamHuman')
  AND ABS(c1.x_axis - c2.x_axis) < 1
  AND ABS(c1.y_axis - c2.y_axis) < 1;
"""
# ABS (absoulte value) The difference between their x positions is less than 1 cm in either direction (positive or negative), and same for y.

cursor.execute(statement)
res = cursor.fetchall()

relational_schema = [description[0] for description in cursor.description]
print(relational_schema)
print("-------------------------------------")
for row in res:
    print(row)


# 2. Total seconds Astro and IamHuman are close (within 1 cm)
print("\n\nTask 4.2")
statement = """
SELECT COUNT(*) AS seconds_close
FROM Coordinates c1
JOIN Coordinates c2 ON c1.timestamp = c2.timestamp
WHERE c1.Rid = (SELECT Rid FROM Robots WHERE name = 'Astro')
  AND c2.Rid = (SELECT Rid FROM Robots WHERE name = 'IamHuman')
  AND ABS(c1.x_axis - c2.x_axis) < 1
  AND ABS(c1.y_axis - c2.y_axis) < 1;
"""
# ABS (absoulte value)

cursor.execute(statement)
res = cursor.fetchall()

relational_schema = [description[0] for description in cursor.description]
print(relational_schema)
print("-------------------------------------")
for row in res:
    print(row)


conn.close()
