import sqlite3


def init_db():
    # Connect to the database file
    conn = sqlite3.connect('traffic_violations.db')
    cursor = conn.cursor()

    # Drop the table if it exists to ensure a fresh start
    cursor.execute('DROP TABLE IF EXISTS violation')

    # Create the table with the 'vehicle' column matching your app.py logic
    # This schema follows your project report requirements [cite: 46, 53]
    cursor.execute('''
        CREATE TABLE violation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle TEXT NOT NULL,
            vtype TEXT NOT NULL,
            location TEXT NOT NULL,
            fine REAL NOT NULL,
            status TEXT NOT NULL,
            issued_on TEXT NOT NULL,
            paid_on TEXT
        )
    ''')

    # Optional: Add some initial sample data for testing
    sample_data = [
        ('TN-45-AT-1234', 'No Helmet', 'Namakkal', 500.0, 'Unpaid', '2026-04-22'),
        ('AP-39-HY-5585', 'No Helmet', 'Nellore', 1000.0, 'Unpaid', '2026-04-27')
    ]

    cursor.executemany('''
        INSERT INTO violation (vehicle, vtype, location, fine, status, issued_on) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_data)

    conn.commit()
    conn.close()
    print("Database initialized successfully with 'vehicle' column.")


if __name__ == '__main__':
    init_db()