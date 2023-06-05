from datetime import datetime, date
from visitor import Visitor
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

try:
    c.execute("""CREATE TABLE visitors (
        id integer,
        name text,
        surname text,
        age integer,
        email text,
        times text,
        presense integer
        )""")   
except:
    print("Table already exists.")


def insert_visitor(visitor: Visitor) -> None:
    """
    Inserts visitor to the database.
    """

    with conn:
        c.execute("INSERT INTO visitors VALUES (:id, :name, :surname, :age, :email, :times, :presense)", 
                {'id': visitor.id, 'name': visitor.name, 'surname': visitor.surname,
                    'age': visitor.age, 'email': visitor.email, 'times': '', 'presense': 0})
        
        conn.commit()
        print("Visitor added successfully.")


def change_user_data_in_db(id: str, name: str, surname: str, age: str, email: str) -> None:
    """
    Change user data in database.
    """

    with conn:
        c.execute("UPDATE visitors SET name = ?, surname = ?, age = ?, email = ? WHERE id = ?", (name, surname, age, email, id))
        conn.commit()

    print("User data changed successfully.")


def get_number_of_user() -> int:
    """
    Get number of users that is registered to database.
    """

    with conn:
        c.execute("SELECT COUNT(*) FROM visitors")
        result = c.fetchone()[0]
        return result


def update(connection, id: int) -> None: # target syntax: ;[14:53:03&2023/05/11 , 14:53:04&2023/05/11];[14:53:06&2023/05/11 , 20:59:39&2023/05/11]
    """
    Updates the database with the current time and date for the specified visitor ID.
    :param connection: The connection object to the database.
    :param id: The ID of the visitor to update.
    """
    
    cursor = connection.cursor()

    now = datetime.now()
    today = date.today()

    current_time = now.strftime("%H:%M:%S")
    today_date = today.strftime("%Y/%m/%d")

    init = current_time + '&' + today_date

    with connection:
        # Retrieve the current value of the column for the specified row
        cursor.execute("SELECT times FROM visitors WHERE id = ?", (id,))
        time = cursor.fetchone()[0]

        cursor.execute("SELECT presense FROM visitors WHERE id = ?", (id,))
        presense = cursor.fetchone()[0]

        #------------------------------------------------------------------#

        new_value = 0 if presense == 1 else 1
        cursor.execute("UPDATE visitors SET presense = ? WHERE id = ?", (new_value, id))

        # Concatenate the current value with the new value, separated by a semicolon and a space
        if presense:
            last_time = time.split(';')[-1].lstrip()
            reversed_time = time[::-1]
            
            i = reversed_time.index(';')
            index = len(time) - (i + 1)

            old = time[:index]
            
            new_combined_value_2 = f'{old};[{last_time} , {init}]'
            cursor.execute("UPDATE visitors SET times = ? WHERE id = ?", (new_combined_value_2, id))

        else:
            new_combined_value = f'{time}; {init}'
            cursor.execute("UPDATE visitors SET times = ? WHERE id = ?", (new_combined_value, id))

        connection.commit()


def reset_times(): # not used as of now
    """
    Reset the times in database.
    """
    
    with conn:
        c.execute("UPDATE visitors SET times = ''")
        c.execute("UPDATE visitors SET presense = 0")

    conn.commit()


    

