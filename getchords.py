import mysql.connector as mysql

def fetch_chords():
    # Connect to the database
    connection = mysql.connect(host='localhost', user='root', password='1234')
    cursor = connection.cursor()

    CHORDS = {
        "C": ["C", "E", "G"],
        "Cm": ["C", "D#", "G"],
        "D": ["D", "F#", "A"],
        "Dm": ["D", "F", "A"],
        "E": ["E", "G#", "B"],
        "Em": ["E", "G", "B"],
        "F": ["F", "A", "C"],
        "Fm": ["F", "G#", "C"],
        "G": ["G", "B", "D"],
        "Gm": ["G", "A#", "D"],
        "A": ["A", "C#", "E"],
        "Am": ["A", "C", "E"],
        "B": ["B", "D#", "F#"],
        "Bm": ["B", "D", "F#"]
    }

    cursor.execute('CREATE DATABASE IF NOT EXISTS concorde')
    cursor.execute('USE concorde')
    cursor.execute('CREATE TABLE IF NOT EXISTS chords (chord_name VARCHAR(10) PRIMARY KEY, note1 VARCHAR(2), note2 VARCHAR(2), note3 VARCHAR(2))')
    connection.commit()
    cursor.execute("SELECT COUNT(*) FROM chords")
    if cursor.fetchone()[0] == 0:  # If no data exists in the table
        for chord, notes in CHORDS.items():
            cursor.execute("INSERT INTO chords (chord_name, note1, note2, note3) VALUES ('{}', '{}', '{}', '{}')".format(chord, notes[0], notes[1], notes[2]))
        connection.commit()


    cursor.execute("SELECT * FROM chords")
    
    # Fetch all results
    results = cursor.fetchall()
    chords_dict = {}
    for chord_name, note1, note2, note3 in results:
        chords_dict[chord_name] = [note1, note2, note3]

    # Close the cursor and connection
    cursor.close()
    connection.close()
    
    return chords_dict
