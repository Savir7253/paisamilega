import sqlite3

conn = sqlite3.connect("database/scrapsetu.db")
cursor = conn.cursor()

tables = cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
""").fetchall()

print("Tables:")
for table in tables:
    print("-", table[0])

print("\nUsers:")
for row in cursor.execute("SELECT * FROM users"):
    print(row)

print("\nPickups:")
for row in cursor.execute("SELECT * FROM pickups"):
    print(row)

print("\nContacts:")
for row in cursor.execute("SELECT * FROM contacts"):
    print(row)

conn.close()