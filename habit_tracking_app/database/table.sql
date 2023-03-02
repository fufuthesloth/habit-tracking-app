CREATE TABLE IF NOT EXISTS habits
('entry_no' INTEGER PRIMARY KEY NOT NULL,
'id' INTEGER NOT NULL,
'title' TEXT NOT NULL,
'period' TEXT NOT NULL,
'created_date' TEXT NOT NULL,
'start_date' TEXT NOT NULL,
'due_date' TEXT NOT NULL,
'completed_timestamp' TEXT DEFAULT NULL,
'streak' INTEGER DEFAULT 0,
'max_streak' INTEGER DEFAULT 0,
'break' INTEGER DEFAULT 0,
'max_break' INTEGER DEFAULT 0)