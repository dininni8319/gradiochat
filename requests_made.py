from db import get_connection
from psycopg2 import sql
from decouple import config
from datetime import datetime, timedelta
from helper_functions import read_data_from_file

MAX_REQUESTS = 50  # Set max requests to 50

def get_tracking_period(start_date):
    """Calculate the tracking period based on the start date."""
    period_start_date = start_date
    period_end_date = period_start_date + timedelta(days=30)
    return period_start_date, period_end_date

def create_or_update_tracking(user_id):
    """Create or update tracking entry for the user."""
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now().date()
    period_start, period_end = get_tracking_period(now)

    # Insert or update the tracking entry
    cursor.execute(sql.SQL("""
        INSERT INTO chatbot_requesttracking (user_id, period_start_date, period_end_date, requests_made, max_requests)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE
        SET period_start_date = EXCLUDED.period_start_date,
            period_end_date = EXCLUDED.period_end_date,
            requests_made = CASE
                WHEN chatbot_requesttracking.period_end_date < %s THEN 0
                ELSE chatbot_requesttracking.requests_made
            END,
            max_requests = %s
        WHERE chatbot_requesttracking.user_id = %s;
    """), (user_id, period_start, period_end, 0, MAX_REQUESTS, now, MAX_REQUESTS, user_id))

    conn.commit()
    cursor.close()
    conn.close()

def check_and_update_requests(user_id):
    """Check and update the number of requests made."""
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().date()

    cursor.execute(sql.SQL("""
        SELECT requests_made, max_requests, period_end_date
        FROM chatbot_requesttracking
        WHERE user_id = %s;
    """), (user_id,))
    result = cursor.fetchone()

    if result is None:
        # If user doesn't exist, insert a new row with requests_made = 0
        cursor.execute(sql.SQL("""
            INSERT INTO chatbot_requesttracking (user_id, requests_made, max_requests, period_start_date, period_end_date)
            VALUES (%s, %s, %s, %s, %s);
        """), (user_id, 0, MAX_REQUESTS, now, now + timedelta(days=30)))
        conn.commit()

    else:
        requests_made, max_requests, period_end_date = result
        if now > period_end_date:
            # Reset period
            period_start, period_end = get_tracking_period(now)
            cursor.execute(sql.SQL("""
                UPDATE chatbot_requesttracking
                SET period_start_date = %s,
                    period_end_date = %s,
                    requests_made = 0
                WHERE user_id = %s;
            """), (period_start, period_end, user_id))
            conn.commit()
            requests_made = 0  # Reset requests made for new period
        
        if requests_made >= max_requests:
            print(f"User {user_id} has reached the limit of {max_requests} requests.")
            return False

        # Update request count
        cursor.execute(sql.SQL("""
            UPDATE chatbot_requesttracking
            SET requests_made = requests_made + 1
            WHERE user_id = %s;
        """), (user_id,))
        conn.commit()
        print(f"Request recorded for user {user_id}. Total requests this period: {requests_made + 1}")

    cursor.close()
    conn.close()
    return True

if __name__ == "__main__":
    # Get data from data.txt:
    data = read_data_from_file("data.txt")  # Make sure to pass the filename to the function
    print("user_id:", data['user_id'])
    create_or_update_tracking(data['user_id'])
    check_and_update_requests(data['user_id'])
