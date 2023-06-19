import sqlite3
from random import randint

def set_up_connection():
    # connect database
    conn = sqlite3.connect('E:\\db_ass2\\db_ass2.db')
    # create cursor
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS word_table
                                (id INTEGER PRIMARY KEY,
                                word TEXT NOT NULL,
                                score INTEGER NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS account_table
                                (id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL,
                                score INTEGER,
                                admin BOOLEAN NOT NULL)''')
    return cursor, conn

def insert_data_word(word, score):
    # Execute INSERT OR IGNORE query
    cursor, conn = set_up_connection()
    cursor.execute('''INSERT OR IGNORE INTO word_table(word, score)\
                VALUES (?, ?)''', (word, score))
    # Save changes
    conn.commit()
    cursor.close()
    conn.close()

def update_data_word(id, word, score):
    cursor, conn = set_up_connection()
    query = """
        UPDATE word_table
        SET word = ?, score = ?
        WHERE id = ?
        """
    cursor.execute(query, (word, score, id))
    conn.commit()
    conn.close()

def insert_data_account(username, password, admin):
    # Execute INSERT OR IGNORE query
    cursor, conn = set_up_connection()
    cursor.execute('''INSERT OR IGNORE INTO account_table(username, password, score, admin)\
                VALUES (?, ?, ?, ?)''', (username, password, 0, admin))
    # Save changes
    conn.commit()
    cursor.close()
    conn.close()

def update_data_account(id, password, score, admin):
    cursor, conn = set_up_connection()
    query = """
        UPDATE account_table
        SET password = ?, score = ?, admin = ?
        WHERE id = ?
        """
    cursor.execute(query, (password, score, admin, id))
    conn.commit()
    conn.close()

def login_game(username, password):
    cursor, conn = set_up_connection()
    query = """
            SELECT * 
            FROM account_table
            WHERE username = ?
            """
    cursor.execute(query, (username,))
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    if data != [] and password == data[0][2]:
        print("You logged in success")
        return data
    else:
        print("Wrong password or username")
        return None

def get_all_words():
    cursor, conn = set_up_connection()
    query = """
            SELECT * 
            FROM word_table
            """
    cursor.execute(query, ())
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def get_random_word(data):
    random_index = randint(0, len(data) - 1)
    return data[random_index]

def hangman_gameplay(acc_id, username, password, acc_score, admin):
    data = get_all_words()
    while True:
        word_tuple = get_random_word(data)
        word = word_tuple[1]
        print(word)
        score = word_tuple[2]
        is_cont = None
        while True:
            choice = input("Would you like to play hangman (yes, no)?: ")
            if choice not in ["yes", "no"]:
                print("Please enter yes or no.")
                continue
            if choice == "yes":
                is_cont = True
                break
            else:
                is_cont = False
                break
        if not is_cont:
            print("Thanks for playing our game.")
            break
        else:
            incorrect_guess = 0
            puzzle = "_" * len(word)
            guessed = []
            while True:
                print(f"You currently have {incorrect_guess} guesses.")
                print("Here is your puzzle:")
                print(puzzle)
                while True:
                    guess_letter = input("Please enter your guess: ")
                    if guess_letter < "A" and guess_letter > "Z":
                        print("Please enter a uppercase letter.")
                        continue
                    break
                if guess_letter not in word:
                    print("Sorry, that letter is NOT in the puzzle.")
                    incorrect_guess += 1
                    if incorrect_guess == 5:
                        print("Sorry, you have made 5 incorrect guesses, you lose.")
                        print(f"The correct word was {word}")
                        break
                elif guess_letter in guessed:
                    print("Sorry, you have 2 incorrect guess.")
                    print("Now it counts as a miss.")
                    continue
                else:
                    print("Congratulations, you guessed a letter in the puzzle!")
                    guessed.append(guess_letter)
                    list_ind = []
                    for i, v in enumerate(word):
                        if v == guess_letter:
                            list_ind.append(i)
                    for i,v in enumerate(puzzle):
                        if i in list_ind:
                            puzzle = puzzle[: i] + guess_letter + puzzle[i + 1: ]
                    if "_" not in puzzle:
                        print(f"Congratulations! You got the the correct word, {word}")
                        acc_score += score
                        update_data_account(acc_id, password, acc_score, admin)
                        break

if __name__ == "__main__":
    while True:
        exit_flag = False
        print("---------------------------WELCOME TO OUR HANGMAN GAME---------------------------")
        print("Please log in to play the game.")
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if username == "0":
                exit_flag = True
                break
            data_user = login_game(username, password)
            if data_user == None:
                continue
            else:
                break
        if exit_flag:
            print("EXITED")
            break
        while True:
            data_user = login_game(username, password)
            user_id, user_name, user_pass, user_score, user_admin = data_user[0]
            print("1. Play game.")
            print("2. See your score: ")
            print("3. See ranking of all players: ")
            print("4. Log out.")
            while True:
                your_choice = input("Enter your choice: ")
                if your_choice not in ["1", "2", "3", "4"]:
                    print("Please enter an option 1, 2, 3, 4")
                    continue
                else:
                    break
            if your_choice == "1":
                hangman_gameplay(user_id, user_name, user_pass, user_score, user_admin)
            elif your_choice == "2":
                print(f"Your score: {user_score}")
            elif your_choice == "3":
                pass
            elif your_choice == "4":
                print(f"See you later {user_name}")
                break

