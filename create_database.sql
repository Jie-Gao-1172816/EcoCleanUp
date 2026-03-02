
/* =========================================================
   EcoCleanup - Database Schema (PostgreSQL)
 
   ========================================================= */

CREATE DATABASE ecocleanup;

-- =========================================================
-- 1) ENUM types
--    Restrict allowed values for role/status/attendance
-- =========================================================
CREATE TYPE user_role AS ENUM ('volunteer', 'event_leader', 'admin');
CREATE TYPE user_status AS ENUM ('active', 'inactive');
CREATE TYPE attendance_status AS ENUM ('registered', 'attended', 'absent', 'cancelled');

-- =========================================================
-- 2) Table: users
--    Stores all users (volunteers / leaders / admins)
-- =========================================================
CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,                 -- PK: auto-increment user id
  username VARCHAR(50) NOT NULL UNIQUE,        -- login username (unique)
  password_hash TEXT NOT NULL,                 -- store hashed password (e.g., bcrypt)
  full_name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  contact_number VARCHAR(20),
  home_address VARCHAR(255),
  profile_image VARCHAR(255),
  environmental_interests VARCHAR(255),
  role user_role NOT NULL,                     -- volunteer / event_leader / admin
  status user_status NOT NULL DEFAULT 'active',
  created_at TIMESTAMP NOT NULL DEFAULT NOW());

-- =========================================================
-- 3) Table: events
--    Stores cleanup events
--    FK: event_leader_id -> users(user_id)
-- =========================================================

CREATE TABLE events (
  event_id SERIAL PRIMARY KEY,
  event_name VARCHAR(100) NOT NULL,
  event_leader_id INTEGER NOT NULL,
  location VARCHAR(255) NOT NULL,
  event_type VARCHAR(50),
  event_date DATE NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  duration INTEGER NOT NULL CHECK (duration > 0),  -- positive duration
  description TEXT,
  supplies TEXT,
  safety_instructions TEXT,

  -- NEW: event lifecycle status (supports cancel/history/reports)
  status VARCHAR(20) NOT NULL DEFAULT 'upcoming',
  updated_at TIMESTAMP,

  created_at TIMESTAMP NOT NULL DEFAULT NOW(),

  -- time order check (works for same-day events)
  CONSTRAINT chk_time_order CHECK (end_time > start_time),

  -- NEW: restrict allowed status values
  CONSTRAINT chk_events_status CHECK (status IN ('upcoming', 'cancelled', 'completed')),

  -- foreign key: each event must have a leader who exists in users
  CONSTRAINT fk_events_leader
    FOREIGN KEY (event_leader_id) REFERENCES users(user_id)
);

-- =========================================================
-- 4) Table: eventregistrations
--    Many-to-many link between volunteers (users) and events
--    FK: event_id -> events, volunteer_id -> users
--    UNIQUE(event_id, volunteer_id) prevents duplicate registration
-- =========================================================
CREATE TABLE eventregistrations (
  registration_id SERIAL PRIMARY KEY,
  event_id INTEGER NOT NULL,
  volunteer_id INTEGER NOT NULL,
  attendance attendance_status NOT NULL DEFAULT 'registered',
  registered_at TIMESTAMP NOT NULL DEFAULT NOW(),
  reminder_flag BOOLEAN DEFAULT FALSE,  -- flag to indicate if reminder is set
  reminder_message TEXT,

  CONSTRAINT uq_event_volunteer UNIQUE (event_id, volunteer_id),

  CONSTRAINT fk_regs_event
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,

  CONSTRAINT fk_regs_user
    FOREIGN KEY (volunteer_id) REFERENCES users(user_id) ON DELETE CASCADE);
-- =========================================================
-- 5) Table: eventoutcomes
--    Stores event outcome metrics (usually 1 outcome record per event)
--    FK: event_id -> events
--    FK: recorded_by -> users (who recorded the outcome)
--    UNIQUE(event_id) ensures at most one outcome per event
-- =========================================================
CREATE TABLE eventoutcomes (
  outcome_id SERIAL PRIMARY KEY,
  event_id INTEGER NOT NULL,
  num_attendees INTEGER NOT NULL CHECK (num_attendees >= 0),
  bags_collected INTEGER NOT NULL CHECK (bags_collected >= 0),
  recyclables_sorted INTEGER NOT NULL CHECK (recyclables_sorted >= 0),
  other_achievements TEXT,
  recorded_by INTEGER NOT NULL,
  recorded_at TIMESTAMP NOT NULL DEFAULT NOW(),

  CONSTRAINT uq_outcome_event UNIQUE (event_id),

  CONSTRAINT fk_outcomes_event
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,

  CONSTRAINT fk_outcomes_recorder
    FOREIGN KEY (recorded_by) REFERENCES users(user_id));

-- =========================================================
-- 6) Table: feedback
--    Stores volunteer feedback for an event
--    FK: event_id -> events, volunteer_id -> users
--    UNIQUE(event_id, volunteer_id) ensures one feedback per volunteer per event
-- =========================================================
CREATE TABLE feedback (
  feedback_id SERIAL PRIMARY KEY,
  event_id INTEGER NOT NULL,
  volunteer_id INTEGER NOT NULL,
  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
  comments TEXT,
  submitted_at TIMESTAMP NOT NULL DEFAULT NOW(),

  CONSTRAINT uq_feedback UNIQUE (event_id, volunteer_id),

  CONSTRAINT fk_feedback_event
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,

  CONSTRAINT fk_feedback_user
    FOREIGN KEY (volunteer_id) REFERENCES users(user_id) ON DELETE CASCADE);

-- =========================================================
-- 7) reminders
-- =========================================================
CREATE TABLE eventreminders (
  reminder_id SERIAL PRIMARY KEY,
  event_id INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
  sent_by INTEGER NOT NULL REFERENCES users(user_id),
  sent_at TIMESTAMP NOT NULL DEFAULT NOW(),
  message TEXT
);

CREATE TABLE reminderreads (
  reminder_id INTEGER NOT NULL REFERENCES eventreminders(reminder_id) ON DELETE CASCADE,
  volunteer_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  seen_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (reminder_id, volunteer_id)
);


ALTER TABLE eventregistrations
  ADD COLUMN IF NOT EXISTS reminder_flag BOOLEAN NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS reminder_message TEXT;