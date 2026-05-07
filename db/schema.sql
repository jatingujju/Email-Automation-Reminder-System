PRAGMA foreign_keys = ON;

CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(255) UNIQUE NOT NULL,

    department VARCHAR(100),

    timezone VARCHAR(50) DEFAULT 'Asia/Kolkata',

    is_active BOOLEAN DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);