CREATE DATABASE ecocleanup;


-- =========
-- ENUM types (role / status / attendance)
-- =========
CREATE TYPE user_role AS ENUM ('volunteer', 'event_leader', 'admin');
CREATE TYPE user_status AS ENUM ('active', 'inactive');
CREATE TYPE attendance_status AS ENUM ('registered', 'attended', 'absent', 'cancelled');

-- =========
-- users
-- =========
CREATE TABLE users (
  user_id               SERIAL PRIMARY KEY,
  username              VARCHAR(50)  NOT NULL UNIQUE,
  password_hash         TEXT         NOT NULL,          -- bcrypt hash 
  full_name             VARCHAR(100) NOT NULL,
  email                 VARCHAR(100) NOT NULL,
  contact_number        VARCHAR(20),
  home_address          VARCHAR(255),
  profile_image         VARCHAR(255),
  environmental_interests VARCHAR(255),
  role                  user_role    NOT NULL,
  status                user_status  NOT NULL DEFAULT 'active',
  created_at            TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- =========
-- events
-- =========
CREATE TABLE events (
  event_id          SERIAL PRIMARY KEY,
  event_name        VARCHAR(100) NOT NULL,
  event_leader_id   INTEGER NOT NULL REFERENCES users(user_id),
  location          VARCHAR(255) NOT NULL,
  event_type        VARCHAR(50),
  event_date        DATE NOT NULL,
  start_time        TIME NOT NULL,
  end_time          TIME NOT NULL,
  duration          INTEGER NOT NULL CHECK (duration > 0),
  description       TEXT,
  supplies          TEXT,
  safety_instructions TEXT,
  created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
  -- optional sanity check: end_time after start_time (works for same-day events)
  CONSTRAINT chk_time_order CHECK (end_time > start_time)
);

-- =========
-- eventregistrations
-- =========
CREATE TABLE eventregistrations (
  registration_id  SERIAL PRIMARY KEY,
  event_id         INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
  volunteer_id     INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  attendance       attendance_status NOT NULL DEFAULT 'registered',
  registered_at    TIMESTAMP NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_event_volunteer UNIQUE (event_id, volunteer_id)
);

-- =========
-- eventoutcomes
-- =========
CREATE TABLE eventoutcomes (
  outcome_id        SERIAL PRIMARY KEY,
  event_id          INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
  num_attendees     INTEGER NOT NULL CHECK (num_attendees >= 0),
  bags_collected    INTEGER NOT NULL CHECK (bags_collected >= 0),
  recyclables_sorted INTEGER NOT NULL CHECK (recyclables_sorted >= 0),
  other_achievements TEXT,
  recorded_by       INTEGER NOT NULL REFERENCES users(user_id),
  recorded_at       TIMESTAMP NOT NULL DEFAULT NOW(),
  -- Typically one outcome record per event (recommended)
  CONSTRAINT uq_outcome_event UNIQUE (event_id)
);

-- =========
-- feedback
-- =========
CREATE TABLE feedback (
  feedback_id    SERIAL PRIMARY KEY,
  event_id       INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
  volunteer_id   INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  rating         INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
  comments       TEXT,
  submitted_at   TIMESTAMP NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_feedback UNIQUE (event_id, volunteer_id)
);

-- Helpful indexes (optional but good)
CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_regs_volunteer ON eventregistrations(volunteer_id);
CREATE INDEX idx_feedback_event ON feedback(event_id);
