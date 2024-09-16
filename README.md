CREATE TABLE request_tracking (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,  -- Assuming each user has an ID
    month VARCHAR(7) NOT NULL,  -- Format: YYYY-MM (e.g., 2024-09)
    requests_made INT DEFAULT 0,
    max_requests INT DEFAULT 50,
    last_request TIMESTAMP DEFAULT NOW()
);