from db import get_connection
from psycopg2 import sql
from decouple import config
from datetime import datetime, timedelta


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

    cursor.execute(sql.SQL("""
        INSERT INTO request_tracking (user_id, period_start_date, period_end_date)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE
        SET period_start_date = EXCLUDED.period_start_date,
            period_end_date = EXCLUDED.period_end_date,
            requests_made = CASE
                WHEN request_tracking.period_end_date < %s THEN 0
                ELSE request_tracking.requests_made
            END
        WHERE request_tracking.user_id = %s;
    """), (user_id, period_start, period_end, now, user_id))

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
        FROM request_tracking
        WHERE user_id = %s;
    """), (user_id,))
    result = cursor.fetchone()

    if result:
        requests_made, max_requests, period_end_date = result
        if now > period_end_date:
            # Reset period
            period_start, period_end = get_tracking_period(now)
            cursor.execute(sql.SQL("""
                UPDATE request_tracking
                SET period_start_date = %s,
                    period_end_date = %s,
                    requests_made = 0
                WHERE user_id = %s;
            """), (period_start, period_end, user_id))
            conn.commit()
        
        if requests_made >= max_requests:
            print(f"User {user_id} has reached the limit of {max_requests} requests.")
            return False

        # Update request count
        cursor.execute(sql.SQL("""
            UPDATE request_tracking
            SET requests_made = requests_made + 1
            WHERE user_id = %s;
        """), (user_id,))
        conn.commit()
        print(f"Request recorded for user {user_id}. Total requests this period: {requests_made + 1}")

    else:
        print(f"No tracking record found for user {user_id}.")
    
    cursor.close()
    conn.close()
    return True

if __name__ == "__main__":
    # Example usage:
    user_id = 1  # Replace with actual user ID
    create_or_update_tracking(user_id)
    check_and_update_requests(user_id)
