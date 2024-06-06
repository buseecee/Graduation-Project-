import sqlite3
import random

def create_classlist_table():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS classlist (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        surname TEXT
                    )''')

    conn.commit()
    conn.close()

def insert_data_into_classlist():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()

    names = ["John", "Emma", "Michael", "Sophia", "William", "Olivia", "James", "Ava", "Alexander", "Isabella"]
    surnames = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]

    for i in range(1, 51):  # id 1'den 50'ye kadar
        name = random.choice(names)
        surname = random.choice(surnames)
        cursor.execute('''INSERT INTO classlist (name, surname)
                          VALUES (?, ?)''', (name, surname))

    conn.commit()
    conn.close()

def main():
    create_classlist_table()
    insert_data_into_classlist()
    print("Veriler başarıyla eklendi.")

if __name__ == "__main__":
    main()
