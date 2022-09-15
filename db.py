import psycopg2

from settings import host, dbname, user, password



def insert_data_into_database(clear_data_list: list):
    """Inserts data from list to database"""
    try:
        # connect to the PostgreSQL server
        conn_string = f"host={host} dbname={dbname}\
        user={user} password={password}"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        # looping through list items and add them to db
        for item in clear_data_list:
            query = "INSERT INTO rent_appartments (title, location, beds, currency, price, date, description, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            vars = item['title'], item['location'], item['beds'], item['currency'], item['price'], item['date'], item['description'], item['href']
            cursor.execute(query, vars)
        # commit all changes in db
        conn.commit()
        # close connection
        cursor.close()
        print('All data saved to db')
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # close connection to db
        if conn is not None:
            conn.close()




def check_whether_table_exists():
    """Check whether table exists"""
    conn_string = f"host={host} dbname={dbname}\
        user={user} password={password}"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(f"SELECT EXISTS ( SELECT FROM pg_tables WHERE schemaname='public' AND tablename='rent_appartments');")    
    if cursor.fetchone()[0]:
        # if table exists
        return True
    else:
        return False
    

def check_whether_postgres_exists():
    """Check whether database connected to the app"""
    try:
        conn_string = f"host={host} dbname={dbname}\
        user={user} password={password}"
        conn = psycopg2.connect(conn_string)
        conn.close()
        return True
    except:
        return False


def create_table():
    conn_string = f"host={host} dbname={dbname}\
        user={user} password={password}"
    # connect to the PostgreSQL server
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    try:
        # create table "rent_appartments"
        table = """
        CREATE TABLE rent_appartments (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            beds VARCHAR(255) NOT NULL,
            currency VARCHAR(255) NOT NULL,
            price VARCHAR(255) NOT NULL,
            date VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            image_url VARCHAR(255) NOT NULL)
        """
        cursor.execute(table)
        # close communication with the PostgreSQL database server
        cursor.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # close connection to db
        if conn is not None:
            conn.close()