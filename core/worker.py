import psycopg2
import time


def worker():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="Pythondev12!?",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Bet")
        cursor = connection.cursor()
        print("Connected...")

        postgres_insert_query = """ 
        update  public.core_paymenttransaction
        set date_expired=s.date_modified + g.days*INTERVAL'1 day' 
        from  public.core_paymenttransaction as s
        inner join public.core_group as g on 
        g.id=s.group_id
        """
        query2 = """update  public.core_paymenttransaction
        set is_deleted=true
        where date_expired<now() """
        cursor.execute(postgres_insert_query)
        cursor.execute(query2)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


while True:
    worker()
    time.sleep(20)
    print("Worker running")
