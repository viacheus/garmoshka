import os
import sqlite3
import sys


def get_database_path():
    # Determine the base path (folder of the executable or script)
    if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller executable
        base_path = sys._MEIPASS  # Folder where the executable is unpacked
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Script directory

    # Build the full path to the database
    return os.path.join(base_path, "cards.db")


def exec_select_query(query, parameters=()):
    con = sqlite3.connect(get_database_path())
    cur = con.cursor()
    result = cur.execute(query, parameters).fetchall()
    con.close()
    return result


def exec_mod_query(query, parameters):
    con = sqlite3.connect(get_database_path())
    cur = con.cursor()
    result = cur.execute(query, parameters)
    con.commit()
    con.close()
    return result


def get_libraries():
    return exec_select_query("SELECT * FROM libraries ORDER BY id")


def add_library(id, card_list=None):
    exec_mod_query(
        "INSERT INTO libraries(id) VALUES(?)",
        (id,),
    )
    if card_list:
        for card in card_list:
            add_card(id, card[0], card[1])


def update_library(id, new_id, card_list=None):
    exec_mod_query(
        "UPDATE cards SET library=? WHERE library=?",
        (new_id, id),
    )
    if card_list:
        for card in card_list:
            add_card(new_id, card[0], card[1])
    return exec_mod_query(
        "UPDATE libraries SET id=? WHERE id=?",
        (new_id, id),
    )


def delete_library(id):
    exec_mod_query(
        "DELETE FROM cards WHERE library=?",
        (id,),
    )
    return exec_mod_query(
        "DELETE FROM libraries WHERE id=?",
        (id,),
    )


def get_cards(library_id):
    return exec_select_query("SELECT * FROM cards WHERE library = ? ORDER BY id", (library_id,))


def add_card(library, question, answer):
    return exec_mod_query(
        "INSERT INTO cards(question, answer, library) VALUES(?, ?, ?)",
        (question, answer, library),
    )


def update_card(id, question, answer):
    return exec_mod_query(
        "UPDATE cards SET question=?, answer=? WHERE id = ?",
        (question, answer, id),
    )


def delete_card(id):
    return exec_mod_query(
        "DELETE FROM cards WHERE id = ?",
        (id,),
    )


def update_card_stat(id, vote):
    return exec_mod_query(
        "UPDATE cards set view_count = view_count + 1, vote_sum = vote_sum + ? WHERE id = ?",
        (vote, id),
    )


def get_card(id):
    con = sqlite3.connect(get_database_path())
    cur = con.cursor()
    result = cur.execute("SELECT * FROM cards WHERE id = ?", (id,)).fetchone()
    con.close()
    return result


def clear_card_stat(library_id):
    return exec_mod_query(
        "UPDATE cards set view_count = 0, vote_sum = 0 WHERE library = ?",
        (library_id,),
    )
