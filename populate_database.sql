-- populate_database.sql (PostgreSQL)
-- EcoCleanup realistic seed data
-- NO plaintext passwords stored in SQL (hashes only)

-- =========================
-- 0) Clear existing data
-- =========================
TRUNCATE feedback, eventoutcomes, eventregistrations, events, users RESTART IDENTITY CASCADE;

-- =========================
-- 1) USERS (2 admins, 5 event leaders, 20 volunteers)
-- =========================
INSERT INTO users
(username, password_hash, full_name, email, contact_number, home_address, environmental_interests, role, status, profile_image)
VALUES
-- Admins (2)
('amelia.admin', '$2b$12$ctI3geegl9BUK3rcNkSxauJEBSvkTw/5PMNmHHPqIGcq1koJdFhgW', 'Amelia Parker', 'amelia.parker@ecocleanup.nz', '021 438 9201', '21 Queen St, Auckland CBD', 'governance, sustainability reporting', 'admin', 'active', 'amelia.png'),
('noah.admin',   '$2b$12$XahoA2qSxytAhdMq3vzuZuXjBuD9gWO2cfwdcTvZw6u/FghcPVMme', 'Noah Thompson', 'noah.thompson@ecocleanup.nz', '022 901 3372', '8 Albert St, Auckland CBD', 'compliance, community engagement', 'admin', 'active', 'noah.png'),

-- Event Leaders (5)
('sophie.king',  '$2b$12$FdOPJzcNxwzX5G91LIGreuFZR4nYDPFAmm335JHC03yIltFmyrzkC', 'Sophie King',  'sophie.king@ecocleanup.nz',  '021 555 1034', '14 Ponsonby Rd, Ponsonby, Auckland', 'beach cleanups, volunteer coordination', 'event_leader', 'active', 'sophie.png'),
('ethan.chen',   '$2b$12$jqQq6mG/gfU4IoJSz6HkKezEckKdxWosxdEqZkY8165r9UvClMH02', 'Ethan Chen',   'ethan.chen@ecocleanup.nz',   '022 614 7721', '33 Great North Rd, Grey Lynn, Auckland', 'waste reduction, recycling education', 'event_leader', 'active', 'ethan.png'),
('ava.patel',    '$2b$12$juEcTLm977Mzv2qIowRehO3eCVEOLGzMHLvcMUWKSaPDU618YHRIq', 'Ava Patel',    'ava.patel@ecocleanup.nz',    '021 771 2049', '5 Dominion Rd, Mt Eden, Auckland', 'river cleanups, safety planning', 'event_leader', 'active', 'ava.png'),
('jack.wilson',  '$2b$12$hTRfTCYsPGbrmwBRwbl56.E4w4CznGaqXdB0p4ZnYajXUL8H/ev0y', 'Jack Wilson',  'jack.wilson@ecocleanup.nz',  '027 108 6620', '19 Lake Rd, Takapuna, Auckland', 'coastal protection, event logistics', 'event_leader', 'active', 'jack.png'),
('mia.ngata',    '$2b$12$L2l23gRFzCrdJDvSwSA66effj4n7rlhRx4Dt9tyStOFg7pWYxaWua', 'Mia Ngata',    'mia.ngata@ecocleanup.nz',    '021 390 4488', '2 Station Rd, Otahuhu, Auckland', 'community partnerships, conservation', 'event_leader', 'active', 'mia.png'),

-- Volunteers (20)
('liam.brown',    '$2b$12$oiTRh3unzW7pQvDZXdXifOO30Pmyacjd2mG2FAo8MTQQdnxsVx5DC', 'Liam Brown',    'liam.brown@example.com',    '021 333 9200', '7 New North Rd, Mt Albert, Auckland', 'beach cleanup, recycling', 'volunteer', 'active', 'liam.png'),
('olivia.wang',   '$2b$12$vgkNnRq9QeUiSuHXJq6NpulTmX3pINcSUNrRE824rxrArI9i6r3IC', 'Olivia Wang',   'olivia.wang@example.com',   '022 110 7865', '18 Sandringham Rd, Sandringham, Auckland', 'tree planting, community events', 'volunteer', 'active', 'olivia.png'),
('lucas.li',      '$2b$12$YNg0uTkXa5tVxVQaGMe76OzJRIqqFpi8VDIKMwR6QC1rbdO0Cc5Ua', 'Lucas Li',      'lucas.li@example.com',      '021 609 2741', '9 Mt Albert Rd, Mt Albert, Auckland', 'river cleanup, wildlife', 'volunteer', 'active', 'lucas.png'),
('isla.taylor',   '$2b$12$z25NPRkHaIuL49MLRBU.5.WHPdbGAGWEBIDf01eWAJa/O/MtE/1yi', 'Isla Taylor',   'isla.taylor@example.com',   '027 401 2230', '25 St Lukes Rd, Mt Albert, Auckland', 'waste reduction, education', 'volunteer', 'active', 'isla.png'),
('henry.zhang',   '$2b$12$Fm2CFoyrrSUDOWU1YDvLE.PH6VwfMb85Gm0fgUuh.K5j3pxJ0UCwi', 'Henry Zhang',   'henry.zhang@example.com',   '021 777 3219', '11 Great South Rd, Epsom, Auckland', 'beach cleanup, recycling', 'volunteer', 'active', 'henry.png'),
('charlotte.lee', '$2b$12$5IglJpIUdyex7jrG2fBx/uoOSCZgq6QlRenntazAJvk5Q4L0tYJ9C', 'Charlotte Lee', 'charlotte.lee@example.com', '022 999 1033', '6 Remuera Rd, Newmarket, Auckland', 'tree planting, community events', 'volunteer', 'active', 'charlotte.png'),
('benjamin.ng',   '$2b$12$XRc.ClqlaBZfEelc8SoQmejJ8xB7221dGugOKfzJO5YMsXM5UkA6q', 'Benjamin Ng',   'ben.ng@example.com',        '021 882 5104', '2 Khyber Pass Rd, Grafton, Auckland', 'river cleanup, wildlife', 'volunteer', 'active', 'benjamin.png'),
('emma.roberts',  '$2b$12$Ks/nOD./WGNFW7Epg89ux.W2U5CnaFUDlvuRhxb0YEAVufiFX7dsu', 'Emma Roberts',  'emma.roberts@example.com',  '027 880 1442', '41 Jervois Rd, Herne Bay, Auckland', 'waste reduction, education', 'volunteer', 'active', 'emma.png'),
('william.singh', '$2b$12$2QsB/f/EfDpm3gXcucXqHOyfSKWI9kDF4rPfToCa/X0/3CSMxMOSS', 'William Singh', 'william.singh@example.com', '021 455 6210', '15 Balmoral Rd, Balmoral, Auckland', 'beach cleanup, recycling', 'volunteer', 'active', 'william.png'),
('mia.harris',    '$2b$12$lkIb7gvPnl1Z8h4vL.f2c.KHYwr0t5SqNQlwflO8kLHN85badq5D6', 'Mia Harris',    'mia.harris@example.com',    '022 706 9090', '3 Carrington Rd, Pt Chevalier, Auckland', 'tree planting, community events', 'volunteer', 'active', 'mia_h.png'),
('james.miller',  '$2b$12$spTHEfFTd7g.CSeN1Utm0.t8FBZMFEHvMd05B06Fpsp7641MQzpuG', 'James Miller',  'james.miller@example.com',  '021 222 7301', '12 Rosebank Rd, Avondale, Auckland', 'river cleanup, wildlife', 'volunteer', 'active', 'james.png'),
('grace.ahmed',   '$2b$12$leZvqkCDxqlWh50r9vHHduv1.eEajSNJJNhZ5HJ19Ej50dLzmHEuW', 'Grace Ahmed',   'grace.ahmed@example.com',   '027 312 8807', '8 Manukau Rd, Epsom, Auckland', 'waste reduction, education', 'volunteer', 'active', 'grace.png'),
('daniel.kim',    '$2b$12$TT4TWkqL3VJLP/eUdU0F9evBCTcxcjiDAa7zNj/H1qf2mx1FM29Ty', 'Daniel Kim',    'daniel.kim@example.com',    '021 590 7314', '22 Queen St, Auckland CBD', 'beach cleanup, recycling', 'volunteer', 'active', 'daniel.png'),
('zoe.martin',    '$2b$12$xKWa.mYuIEExQyG73l9eZ./.IWDZb5GwIBex5EG9LypHUzkYaLaLS', 'Zoe Martin',    'zoe.martin@example.com',    '022 814 0066', '16 Hobson St, Auckland CBD', 'tree planting, community events', 'volunteer', 'active', 'zoe.png'),
('ryan.clark',    '$2b$12$FP7QAyhmSXS0dGGSpM4yqOg.nout8Hd8y6d4TaxELv2AObnmmOwPu', 'Ryan Clark',    'ryan.clark@example.com',    '021 914 3002', '7 Fanshawe St, Auckland CBD', 'river cleanup, wildlife', 'volunteer', 'active', 'ryan.png'),
('ella.johnson',  '$2b$12$XZmpB.Wfn22p/0ZP4kRYBONnrdIS5gWem236tSiNngfnad.locglO', 'Ella Johnson',  'ella.johnson@example.com',  '027 777 1181', '30 Lake Rd, Takapuna, Auckland', 'waste reduction, education', 'volunteer', 'active', 'ella.png'),
('kai.robinson',  '$2b$12$X7k.nF0EZYgeW/ECgN0lO.yUiU6XsoT3r1dq0BpzZ15we8LzuXiQi', 'Kai Robinson',  'kai.robinson@example.com',  '021 678 4433', '5 Anzac Ave, Auckland CBD', 'beach cleanup, recycling', 'volunteer', 'active', 'kai.png'),
('chloe.moore',   '$2b$12$KPaCZU0SC1OoM1d5f0I/9e9oSSYPESt69qBPLKcNajkmRDfyPQTpy', 'Chloe Moore',   'chloe.moore@example.com',   '022 450 6321', '9 Symonds St, Grafton, Auckland', 'tree planting, community events', 'volunteer', 'active', 'chloe.png'),
('leo.anderson',  '$2b$12$jIR7CdWzY3L.SRJMI/e9IObryEnzB5J7rmcT.JyeVfVv1t1zMpxiu', 'Leo Anderson',  'leo.anderson@example.com',  '021 318 4020', '18 Broadway, Newmarket, Auckland', 'river cleanup, wildlife', 'volunteer', 'active', 'leo.png'),
('hana.williams', '$2b$12$7bBlKg3J8Xc7JMWCry1yyuuu5dg3/fCc6oTC/zLFQ3d6AWdSzi0cy', 'Hana Williams', 'hana.williams@example.com', '027 909 7700', '4 Great South Rd, Otahuhu, Auckland', 'waste reduction, education', 'volunteer', 'active', 'hana.png');

-- =========================
-- 2) EVENTS (20) leader_id references users with role 'event_leader'
-- =========================
WITH leader_map AS (
  SELECT username, user_id
  FROM users
  WHERE role = 'event_leader'),
event_seed AS (
  SELECT * FROM (VALUES
    ('Takapuna Beach Morning Cleanup',      'jack.wilson', 'Takapuna Beach, Auckland', 'Beach',     CURRENT_DATE + 2,  TIME '09:00', TIME '11:00', 120,
     'A relaxed beach cleanup focused on plastic and micro-litter along the shoreline.', 'Gloves, bags, grabbers', 'Wear closed shoes; be mindful of tides; stay hydrated.'),
    ('Onehunga Foreshore Waste Sort',       'mia.ngata',   'Onehunga Bay Reserve, Auckland', 'Community', CURRENT_DATE + 3, TIME '10:00', TIME '12:30', 150,
     'Collect and sort waste; learn quick sorting tips and safe handling procedures.', 'Sorting bins, gloves, bags', 'Avoid sharp items; use grabbers; report hazards to leader.'),
    ('Mt Albert Park Litter Patrol',        'ethan.chen',  'Mt Albert, Auckland', 'Park',        CURRENT_DATE + 4,  TIME '08:30', TIME '10:30', 120,
     'Short morning patrol around park tracks and picnic areas to reduce litter hotspots.', 'Gloves, bags', 'Stay on paths; sun protection recommended.'),
    ('Meadowbank Stream Edge Cleanup',      'ava.patel',   'Meadowbank, Auckland', 'River',       CURRENT_DATE + 5,  TIME '09:30', TIME '12:00', 150,
     'Stream-side cleanup with a focus on preventing waste entering waterways.', 'Gloves, bags, grabbers', 'Keep a safe distance from water edge; work in pairs.'),
    ('Auckland CBD Laneway Clean',          'sophie.king', 'High St & Vulcan Ln, Auckland CBD', 'Community', CURRENT_DATE + 6, TIME '18:00', TIME '20:00', 120,
     'Evening laneway clean-up targeting small litter, cigarette butts, and flyers.', 'Gloves, bags, tongs', 'Hi-vis recommended; be aware of traffic and pedestrians.'),

    ('Mangere Mountain Reserve Cleanup',    'mia.ngata',   'Mangere Mountain, Auckland', 'Park',     CURRENT_DATE + 7, TIME '09:00', TIME '11:30', 150,
     'Trail and reserve cleanup with light educational talk about local ecology.', 'Gloves, bags', 'Stay together; watch uneven ground.'),
    ('Newmarket Shopping Strip Sweep',      'sophie.king', 'Broadway, Newmarket, Auckland', 'Community', CURRENT_DATE + 8, TIME '17:30', TIME '19:30', 120,
     'Quick sweep along high-traffic areas to reduce street litter and improve presentation.', 'Gloves, bags', 'Work in pairs; keep clear of shop entrances.'),
    ('Point Chev Coastal Cleanup',          'jack.wilson', 'Point Chevalier Beach, Auckland', 'Beach',  CURRENT_DATE + 9, TIME '09:00', TIME '11:00', 120,
     'Beach cleanup plus a short briefing on common coastal waste sources.', 'Gloves, bags, grabbers', 'Mind the tide; sunscreen recommended.'),
    ('Otahuhu Community Clean Day',         'mia.ngata',   'Otahuhu Town Centre, Auckland', 'Community', CURRENT_DATE + 10, TIME '10:00', TIME '12:00', 120,
     'Community-led clean day near transport hubs and streets with high foot traffic.', 'Gloves, bags', 'Be aware of vehicles; use crossings.'),
    ('Grey Lynn Park Recycling Focus',      'ethan.chen',  'Grey Lynn Park, Auckland', 'Park',      CURRENT_DATE + 11, TIME '09:30', TIME '11:30', 120,
     'Park cleanup with emphasis on separating recyclables to reduce landfill waste.', 'Gloves, bags, sorting bins', 'Avoid sharp items; inform leader if found.'),

    ('Mission Bay Early Bird Cleanup',      'jack.wilson', 'Mission Bay Beach, Auckland', 'Beach',   CURRENT_DATE + 12, TIME '07:30', TIME '09:30', 120,
     'Early morning cleanup to reduce litter before peak visitor time.', 'Gloves, bags, grabbers', 'Hydrate; watch for glass fragments.'),
    ('Western Springs Park Tracks Patrol',  'ethan.chen',  'Western Springs, Auckland', 'Park',     CURRENT_DATE + 13, TIME '09:00', TIME '11:00', 120,
     'Track-side cleanup and bin-area tidy-up around the lake and lawns.', 'Gloves, bags', 'Stay on marked paths; keep distance from wildlife.'),
    ('Kingsland Neighbourhood Sweep',       'sophie.king', 'Kingsland, Auckland', 'Community',  CURRENT_DATE + 14, TIME '16:30', TIME '18:30', 120,
     'Neighbourhood sweep with a focus on bottle tops, wrappers, and street litter.', 'Gloves, bags', 'Hi-vis recommended near intersections.'),
    ('Avondale Market Area Clean',          'mia.ngata',   'Avondale, Auckland', 'Community',   CURRENT_DATE + 15, TIME '14:00', TIME '16:00', 120,
     'Post-market cleanup to keep streets clean and reduce waste in storm drains.', 'Gloves, bags', 'Be cautious of traffic; watch for sharp items.'),
    ('Panmure Basin Edge Cleanup',          'ava.patel',   'Panmure Basin, Auckland', 'River',     CURRENT_DATE + 16, TIME '09:30', TIME '12:00', 150,
     'Cleanup around basin edges to protect water quality and reduce runoff litter.', 'Gloves, bags, grabbers', 'Stay clear of slippery edges; work in pairs.'),

    ('Hobsonville Point Coastal Walk',      'jack.wilson', 'Hobsonville Point, Auckland', 'Beach',   CURRENT_DATE + 17, TIME '09:00', TIME '11:30', 150,
     'Coastal walk cleanup covering common litter spots near paths and lookouts.', 'Gloves, bags', 'Watch footing on rocks; sunscreen recommended.'),
    ('Manukau Harbour Shoreline Cleanup',   'ava.patel',   'Mangere Bridge, Auckland', 'Beach',     CURRENT_DATE + 18, TIME '10:00', TIME '12:30', 150,
     'Shoreline cleanup aimed at preventing plastics entering the harbour ecosystem.', 'Gloves, bags, grabbers', 'Mind tides; avoid unknown containers.'),
    ('Parnell Rose Gardens Quick Clean',    'sophie.king', 'Parnell Rose Gardens, Auckland', 'Park',   CURRENT_DATE + 19, TIME '09:00', TIME '10:30', 90,
     'Short cleanup around garden paths and picnic areas to maintain a welcoming space.', 'Gloves, bags', 'Stay on paths; respect garden areas.'),
    ('Devonport Waterfront Cleanup',        'jack.wilson', 'Devonport Waterfront, Auckland', 'Beach',  CURRENT_DATE + 20, TIME '09:30', TIME '11:30', 120,
     'Waterfront cleanup with a focus on wind-blown plastics and bottle litter.', 'Gloves, bags, grabbers', 'Be mindful of ferry traffic areas.'),
    ('Henderson Park Community Event',      'ethan.chen',  'Henderson Park, Auckland', 'Community', CURRENT_DATE + 21, TIME '10:00', TIME '12:00', 120,
     'Community cleanup plus short recycling talk; ideal for first-time volunteers.', 'Gloves, bags, sorting bins', 'Wear closed shoes; hydrate; follow leader instructions.'))
	AS t(
    event_name, leader_username, location, event_type,
    event_date, start_time, end_time, duration,
    description, supplies, safety_instructions))
INSERT INTO events
(event_name, event_leader_id, location, event_type, event_date, start_time, end_time, duration, description, supplies, safety_instructions)
SELECT
  e.event_name,
  lm.user_id,
  e.location,
  e.event_type,
  e.event_date,
  e.start_time,
  e.end_time,
  e.duration,
  e.description,
  e.supplies,
  e.safety_instructions
FROM event_seed e
JOIN leader_map lm ON lm.username = e.leader_username;

-- =========================
-- 3) REGISTRATIONS (25) volunteer_id references users with role 'volunteer', event_id references events
-- =========================
WITH vmap AS (
  SELECT username, user_id FROM users WHERE role = 'volunteer'
),
emap AS (
  SELECT event_name, event_id FROM events
),
reg_seed AS (
  SELECT * FROM (VALUES
    ('Takapuna Beach Morning Cleanup', 'liam.brown'),
    ('Takapuna Beach Morning Cleanup', 'olivia.wang'),
    ('Onehunga Foreshore Waste Sort', 'lucas.li'),
    ('Mt Albert Park Litter Patrol', 'isla.taylor'),
    ('Meadowbank Stream Edge Cleanup', 'henry.zhang'),
    ('Auckland CBD Laneway Clean', 'charlotte.lee'),
    ('Mangere Mountain Reserve Cleanup', 'benjamin.ng'),
    ('Newmarket Shopping Strip Sweep', 'emma.roberts'),
    ('Point Chev Coastal Cleanup', 'william.singh'),
    ('Otahuhu Community Clean Day', 'mia.harris'),
    ('Grey Lynn Park Recycling Focus', 'james.miller'),
    ('Mission Bay Early Bird Cleanup', 'grace.ahmed'),
    ('Western Springs Park Tracks Patrol', 'daniel.kim'),
    ('Kingsland Neighbourhood Sweep', 'zoe.martin'),
    ('Avondale Market Area Clean', 'ryan.clark'),
    ('Panmure Basin Edge Cleanup', 'ella.johnson'),
    ('Hobsonville Point Coastal Walk', 'kai.robinson'),
    ('Manukau Harbour Shoreline Cleanup', 'chloe.moore'),
    ('Parnell Rose Gardens Quick Clean', 'leo.anderson'),
    ('Devonport Waterfront Cleanup', 'hana.williams'),
    ('Takapuna Beach Morning Cleanup', 'daniel.kim'),
    ('Mission Bay Early Bird Cleanup', 'olivia.wang'),
    ('Henderson Park Community Event', 'liam.brown'),
    ('Henderson Park Community Event', 'emma.roberts'),
    ('Henderson Park Community Event', 'grace.ahmed')) 
	AS t(event_name, volunteer_username))
INSERT INTO eventregistrations (event_id, volunteer_id, attendance)
SELECT
  em.event_id,
  vm.user_id,
  'registered'
FROM reg_seed r
JOIN emap em ON em.event_name = r.event_name
JOIN vmap vm ON vm.username = r.volunteer_username;

-- =========================
-- 4) FEEDBACK (10)
-- =========================
WITH vmap AS (SELECT username, user_id FROM users WHERE role='volunteer'),
     emap AS (SELECT event_name, event_id FROM events),
     fb_seed AS (
       SELECT * FROM (VALUES
         ('Takapuna Beach Morning Cleanup', 'liam.brown', 5, 'Great vibe and clear instructions.'),
         ('Onehunga Foreshore Waste Sort', 'lucas.li', 4, 'Loved the sorting tips, very practical.'),
         ('Mt Albert Park Litter Patrol', 'isla.taylor', 5, 'Short and effective, nice group.'),
         ('Meadowbank Stream Edge Cleanup', 'henry.zhang', 4, 'Good safety focus near the water.'),
         ('Auckland CBD Laneway Clean', 'charlotte.lee', 4, 'Evening time worked well for me.'),
         ('Mission Bay Early Bird Cleanup', 'grace.ahmed', 5, 'Early start but worth it.'),
         ('Western Springs Park Tracks Patrol', 'daniel.kim', 4, 'Well organised, good pace.'),
         ('Avondale Market Area Clean', 'ryan.clark', 4, 'Helpful team, lots collected.'),
         ('Parnell Rose Gardens Quick Clean', 'leo.anderson', 5, 'Beautiful spot, quick tidy up.'),
         ('Henderson Park Community Event', 'emma.roberts', 5, 'Great for first-timers, friendly leader.')
       ) AS t(event_name, volunteer_username, rating, comments)
     )
INSERT INTO feedback (event_id, volunteer_id, rating, comments)
SELECT
  em.event_id,
  vm.user_id,
  f.rating,
  f.comments
FROM fb_seed f
JOIN emap em ON em.event_name = f.event_name
JOIN vmap vm ON vm.username = f.volunteer_username;

-- =========================
-- 5) OUTCOMES (8)
-- =========================
WITH em AS (
  SELECT e.event_id, e.event_name, u.user_id AS leader_id
  FROM events e
  JOIN users u ON u.user_id = e.event_leader_id
),
out_seed AS (
  SELECT * FROM (VALUES
    ('Takapuna Beach Morning Cleanup', 28, 16, 9, 'Removed several bags of micro-litter near the dunes.'),
    ('Onehunga Foreshore Waste Sort',  22, 12, 7, 'Good sorting accuracy; plastics separated cleanly.'),
    ('Mt Albert Park Litter Patrol',   18,  9, 5, 'Focused on picnic areas; noticeable improvement.'),
    ('Meadowbank Stream Edge Cleanup', 20, 11, 6, 'Cleared storm drain inlets and stream edges.'),
    ('Auckland CBD Laneway Clean',     15,  7, 3, 'Collected cigarette butts and flyers in laneways.'),
    ('Mission Bay Early Bird Cleanup', 24, 14, 8, 'High volume of take-away packaging removed.'),
    ('Panmure Basin Edge Cleanup',     19, 10, 6, 'Reduced litter along basin path and edge.'),
    ('Henderson Park Community Event', 26, 13, 9, 'Great turnout; strong recycling participation.')
  ) AS t(event_name, num_attendees, bags_collected, recyclables_sorted, other_achievements)
)
INSERT INTO eventoutcomes (event_id, num_attendees, bags_collected, recyclables_sorted, other_achievements, recorded_by)
SELECT
  em.event_id,
  o.num_attendees,
  o.bags_collected,
  o.recyclables_sorted,
  o.other_achievements,
  em.leader_id
FROM out_seed o
JOIN em ON em.event_name = o.event_name;

-- Optional checks:
-- SELECT role, COUNT(*) FROM users GROUP BY role ORDER BY role;
-- SELECT COUNT(*) FROM events;
-- SELECT COUNT(*) FROM eventregistrations;
-- SELECT COUNT(*) FROM feedback;
-- SELECT COUNT(*) FROM eventoutcomes;
