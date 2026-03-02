
BEGIN;

-- =========================================================
-- 1) USERS (27)
-- =========================================================
INSERT INTO users
(username, password_hash, full_name, email, contact_number, home_address, environmental_interests, role, status, profile_image)
VALUES
-- Admins (2)
('amelia.admin', '$2b$12$ctI3geegl9BUK3rcNkSxauJEBSvkTw/5PMNmHHPqIGcq1koJdFhgW', 'Amelia Parker', 'amelia.parker@ecocleanup.nz', '021 438 9201', '21 Queen St, Auckland CBD', 'governance, sustainability reporting', 'admin', 'active', 'amelia.png'),
('noah.admin',   '$2b$12$XahoA2qSxytAhdMq3vzuZuXjBuD9gWO2cfwdcTvZw6u/FghcPVMme', 'Noah Thompson', 'noah.thompson@ecocleanup.nz', '022 901 3372', '8 Albert St, Auckland CBD', 'compliance, community engagement', 'admin', 'active', 'noah.png'),

-- Event Leaders (5)
('sophie.king',  '$2b$12$FdOPJzcNxwzX5G91LIGreuFZR4nYDPFAmm335JHC03yIltFmyrzkC', 'Sophie King',  'sophie.king@ecocleanup.nz',  '021 555 1034', '14 Ponsonby Rd, Ponsonby, Auckland', 'beach cleanups, coordination', 'event_leader', 'active', 'sophie.png'),
('ethan.chen',   '$2b$12$jqQq6mG/gfU4IoJSz6HkKezEckKdxWosxdEqZkY8165r9UvClMH02', 'Ethan Chen',   'ethan.chen@ecocleanup.nz',   '022 614 7721', '33 Great North Rd, Grey Lynn, Auckland', 'recycling education', 'event_leader', 'active', 'ethan.png'),
('ava.patel',    '$2b$12$juEcTLm977Mzv2qIowRehO3eCVEOLGzMHLvcMUWKSaPDU618YHRIq', 'Ava Patel',    'ava.patel@ecocleanup.nz',    '021 771 2049', '5 Dominion Rd, Mt Eden, Auckland', 'river cleanups, safety', 'event_leader', 'active', 'ava.png'),
('jack.wilson',  '$2b$12$hTRfTCYsPGbrmwBRwbl56.E4w4CznGaqXdB0p4ZnYajXUL8H/ev0y', 'Jack Wilson',  'jack.wilson@ecocleanup.nz',  '027 108 6620', '19 Lake Rd, Takapuna, Auckland', 'coastal protection, logistics', 'event_leader', 'active', 'jack.png'),
('mia.ngata',    '$2b$12$L2l23gRFzCrdJDvSwSA66effj4n7rlhRx4Dt9tyStOFg7pWYxaWua', 'Mia Ngata',    'mia.ngata@ecocleanup.nz',    '021 390 4488', '2 Station Rd, Otahuhu, Auckland', 'community partnerships', 'event_leader', 'active', 'mia.png'),

-- Volunteers (20)
('liam.brown',    '$2b$12$oiTRh3unzW7pQvDZXdXifOO30Pmyacjd2mG2FAo8MTQQdnxsVx5DC', 'Liam Brown',    'liam.brown@example.com',    '021 333 9200', '7 New North Rd, Mt Albert, Auckland', 'beach cleanup, recycling', 'volunteer', 'active', 'liam.png'),
('olivia.wang',   '$2b$12$vgkNnRq9QeUiSuHXJq6NpulTmX3pINcSUNrRE824rxrArI9i6r3IC', 'Olivia Wang',   'olivia.wang@example.com',   '022 110 7865', '18 Sandringham Rd, Sandringham, Auckland', 'tree planting, community', 'volunteer', 'active', 'olivia.png'),
('lucas.li',      '$2b$12$YNg0uTkXa5tVxVQaGMe76OzJRIqqFpi8VDIKMwR6QC1rbdO0Cc5Ua', 'Lucas Li',      'lucas.li@example.com',      '021 609 2741', '9 Mt Albert Rd, Mt Albert, Auckland', 'river cleanup, wildlife', 'volunteer', 'active', 'lucas.png'),
('isla.taylor',   '$2b$12$z25NPRkHaIuL49MLRBU.5.WHPdbGAGWEBIDf01eWAJa/O/MtE/1yi', 'Isla Taylor',   'isla.taylor@example.com',   '027 401 2230', '25 St Lukes Rd, Mt Albert, Auckland', 'waste reduction, education', 'volunteer', 'active', 'isla.png'),
('henry.zhang',   '$2b$12$Fm2CFoyrrSUDOWU1YDvLE.PH6VwfMb85Gm0fgUuh.K5j3pxJ0UCwi', 'Henry Zhang',   'henry.zhang@example.com',   '021 777 3219', '11 Great South Rd, Epsom, Auckland', 'beach cleanup, recycling', 'volunteer', 'active', 'henry.png'),
('charlotte.lee', '$2b$12$5IglJpIUdyex7jrG2fBx/uoOSCZgq6QlRenntazAJvk5Q4L0tYJ9C', 'Charlotte Lee', 'charlotte.lee@example.com', '022 999 1033', '6 Remuera Rd, Newmarket, Auckland', 'tree planting, community', 'volunteer', 'active', 'charlotte.png'),
('benjamin.ng',   '$2b$12$XRc.ClqlaBZfEelc8SoQmejJ8xB7221dGugOKfzJO5YMsXM5UkA6q', 'Benjamin Ng',   'ben.ng@example.com',        '021 882 5104', '2 Khyber Pass Rd, Grafton, Auckland', 'river cleanup, wildlife', 'volunteer', 'active', 'benjamin.png'),
('emma.roberts',  '$2b$12$Ks/nOD./WGNFW7Epg89ux.W2U5CnaFUDlvuRhxb0YEAVufiFX7dsu', 'Emma Roberts',  'emma.roberts@example.com',  '027 880 1442', '41 Jervois Rd, Herne Bay, Auckland', 'waste reduction, education', 'volunteer', 'active', 'emma.png'),
('william.singh', '$2b$12$2QsB/f/EfDpm3gXcucXqHOyfSKWI9kDF4rPfToCa/X0/3CSMxMOSS', 'William Singh', 'william.singh@example.com', '021 455 6210', '15 Balmoral Rd, Balmoral, Auckland', 'beach cleanup, recycling', 'volunteer', 'active', 'william.png'),
('mia.harris',    '$2b$12$lkIb7gvPnl1Z8h4vL.f2c.KHYwr0t5SqNQlwflO8kLHN85badq5D6', 'Mia Harris',    'mia.harris@example.com',    '022 706 9090', '3 Carrington Rd, Pt Chevalier, Auckland', 'tree planting, community', 'volunteer', 'active', 'mia_h.png'),
('james.miller',  '$2b$12$spTHEfFTd7g.CSeN1Utm0.t8FBZMFEHvMd05B06Fpsp7641MQzpuG', 'James Miller',  'james.miller@example.com',  '021 222 7301', '12 Rosebank Rd, Avondale, Auckland', 'river cleanup, wildlife', 'volunteer', 'active', 'james.png'),
('grace.ahmed',   '$2b$12$leZvqkCDxqlWh50r9vHHduv1.eEajSNJJNhZ5HJ19Ej50dLzmHEuW', 'Grace Ahmed',   'grace.ahmed@example.com',   '027 312 8807', '8 Manukau Rd, Epsom, Auckland', 'waste reduction, education', 'volunteer', 'active', 'grace.png'),
('daniel.kim',    '$2b$12$TT4TWkqL3VJLP/eUdU0F9evBCTcxcjiDAa7zNj/H1qf2mx1FM29Ty', 'Daniel Kim',    'daniel.kim@example.com',    '021 590 7314', '22 Queen St, Auckland CBD', 'beach cleanup, recycling', 'volunteer', 'active', 'daniel.png'),
('zoe.martin',    '$2b$12$xKWa.mYuIEExQyG73l9eZ./.IWDZb5GwIBex5EG9LypHUzkYaLaLS', 'Zoe Martin',    'zoe.martin@example.com',    '022 814 0066', '16 Hobson St, Auckland CBD', 'tree planting, community', 'volunteer', 'active', 'zoe.png'),
('ryan.clark',    '$2b$12$FP7QAyhmSXS0dGGSpM4yqOg.nout8Hd8y6d4TaxELv2AObnmmOwPu', 'Ryan Clark',    'ryan.clark@example.com',    '021 914 3002', '7 Fanshawe St, Auckland CBD', 'river cleanup, wildlife', 'volunteer', 'active', 'ryan.png'),
('ella.johnson',  '$2b$12$XZmpB.Wfn22p/0ZP4kRYBONnrdIS5gWem236tSiNngfnad.locglO', 'Ella Johnson',  'ella.johnson@example.com',  '027 777 1181', '30 Lake Rd, Takapuna, Auckland', 'waste reduction, education', 'volunteer', 'active', 'ella.png'),
('kai.robinson',  '$2b$12$X7k.nF0EZYgeW/ECgN0lO.yUiU6XsoT3r1dq0BpzZ15we8LzuXiQi', 'Kai Robinson',  'kai.robinson@example.com',  '021 678 4433', '5 Anzac Ave, Auckland CBD', 'beach cleanup, recycling', 'volunteer', 'active', 'kai.png'),
('chloe.moore',   '$2b$12$KPaCZU0SC1OoM1d5f0I/9e9oSSYPESt69qBPLKcNajkmRDfyPQTpy', 'Chloe Moore',   'chloe.moore@example.com',   '022 450 6321', '9 Symonds St, Grafton, Auckland', 'tree planting, community', 'volunteer', 'active', 'chloe.png'),
('leo.anderson',  '$2b$12$jIR7CdWzY3L.SRJMI/e9IObryEnzB5J7rmcT.JyeVfVv1t1zMpxiu', 'Leo Anderson',  'leo.anderson@example.com',  '021 318 4020', '18 Broadway, Newmarket, Auckland', 'river cleanup, wildlife', 'volunteer', 'active', 'leo.png'),
('hana.williams', '$2b$12$7bBlKg3J8Xc7JMWCry1yyuuu5dg3/fCc6oTC/zLFQ3d6AWdSzi0cy', 'Hana Williams', 'hana.williams@example.com', '027 909 7700', '4 Great South Rd, Otahuhu, Auckland', 'waste reduction, education', 'volunteer', 'active', 'hana.png');

-- =========================================================
-- 2) EVENTS (20 total) - mix of past + future
--    Past events: 5 events (for history + outcomes + feedback)
-- =========================================================
INSERT INTO events
(event_name, event_leader_id, location, event_type, event_date, start_time, end_time, duration, description, supplies, safety_instructions)
VALUES
-- PAST (5)
('Takapuna Beach Morning Cleanup',      (SELECT user_id FROM users WHERE username='jack.wilson'),  'Takapuna Beach, Auckland', 'Beach',     CURRENT_DATE - 2,  TIME '09:00', TIME '11:00', 120, 'Beach cleanup focusing on plastics and micro-litter.', 'Gloves, bags, grabbers', 'Closed shoes; be mindful of tides; hydrate.'),
('Onehunga Foreshore Waste Sort',       (SELECT user_id FROM users WHERE username='mia.ngata'),    'Onehunga Bay Reserve, Auckland', 'Community', CURRENT_DATE - 5, TIME '10:00', TIME '12:30', 150, 'Collect and sort waste with quick recycling tips.', 'Sorting bins, gloves, bags', 'Avoid sharp items; report hazards.'),
('Mt Albert Park Litter Patrol',        (SELECT user_id FROM users WHERE username='ethan.chen'),   'Mt Albert, Auckland', 'Park',        CURRENT_DATE - 6,  TIME '08:30', TIME '10:30', 120, 'Short patrol around tracks and picnic areas.', 'Gloves, bags', 'Stay on paths; sun protection.'),
('Meadowbank Stream Edge Cleanup',      (SELECT user_id FROM users WHERE username='ava.patel'),    'Meadowbank, Auckland', 'River',       CURRENT_DATE - 8,  TIME '09:30', TIME '12:00', 150, 'Stream-side cleanup to protect waterways.', 'Gloves, bags, grabbers', 'Keep distance from edges; work in pairs.'),
('Auckland CBD Laneway Clean',          (SELECT user_id FROM users WHERE username='sophie.king'),  'High St & Vulcan Ln, Auckland CBD', 'Community', CURRENT_DATE - 10, TIME '18:00', TIME '20:00', 120, 'Evening laneway cleanup for small litter and butts.', 'Gloves, bags, tongs', 'Hi-vis recommended; watch traffic.'),

-- FUTURE (15)
('Mangere Mountain Reserve Cleanup',    (SELECT user_id FROM users WHERE username='mia.ngata'),    'Mangere Mountain, Auckland', 'Park',     CURRENT_DATE + 7,  TIME '09:00', TIME '11:30', 150, 'Trail and reserve cleanup with short ecology talk.', 'Gloves, bags', 'Stay together; watch uneven ground.'),
('Newmarket Shopping Strip Sweep',      (SELECT user_id FROM users WHERE username='sophie.king'),  'Broadway, Newmarket, Auckland', 'Community', CURRENT_DATE + 8, TIME '17:30', TIME '19:30', 120, 'Sweep high-traffic shopping area and street edges.', 'Gloves, bags', 'Work in pairs; keep entrances clear.'),
('Point Chev Coastal Cleanup',          (SELECT user_id FROM users WHERE username='jack.wilson'),  'Point Chevalier Beach, Auckland', 'Beach',  CURRENT_DATE + 9,  TIME '09:00', TIME '11:00', 120, 'Coastal cleanup plus briefing on common waste sources.', 'Gloves, bags, grabbers', 'Mind tide; sunscreen.'),
('Otahuhu Community Clean Day',         (SELECT user_id FROM users WHERE username='mia.ngata'),    'Otahuhu Town Centre, Auckland', 'Community', CURRENT_DATE + 10, TIME '10:00', TIME '12:00', 120, 'Clean near transport hubs and main streets.', 'Gloves, bags', 'Use crossings; watch vehicles.'),
('Grey Lynn Park Recycling Focus',      (SELECT user_id FROM users WHERE username='ethan.chen'),   'Grey Lynn Park, Auckland', 'Park',      CURRENT_DATE + 11, TIME '09:30', TIME '11:30', 120, 'Cleanup with focus on separating recyclables.', 'Gloves, bags, sorting bins', 'Avoid sharps; tell leader if found.'),
('Mission Bay Early Bird Cleanup',      (SELECT user_id FROM users WHERE username='jack.wilson'),  'Mission Bay Beach, Auckland', 'Beach',   CURRENT_DATE + 12, TIME '07:30', TIME '09:30', 120, 'Early cleanup before peak visitor time.', 'Gloves, bags, grabbers', 'Hydrate; watch for glass.'),
('Western Springs Tracks Patrol',       (SELECT user_id FROM users WHERE username='ethan.chen'),   'Western Springs, Auckland', 'Park',     CURRENT_DATE + 13, TIME '09:00', TIME '11:00', 120, 'Track-side cleanup around lake and lawns.', 'Gloves, bags', 'Stay on paths; keep distance from wildlife.'),
('Kingsland Neighbourhood Sweep',       (SELECT user_id FROM users WHERE username='sophie.king'),  'Kingsland, Auckland', 'Community',  CURRENT_DATE + 14, TIME '16:30', TIME '18:30', 120, 'Neighbourhood sweep targeting wrappers and tops.', 'Gloves, bags', 'Hi-vis near intersections.'),
('Avondale Market Area Clean',          (SELECT user_id FROM users WHERE username='mia.ngata'),    'Avondale, Auckland', 'Community',  CURRENT_DATE + 15, TIME '14:00', TIME '16:00', 120, 'Post-market tidy to reduce storm drain waste.', 'Gloves, bags', 'Be cautious of traffic; watch for sharps.'),
('Panmure Basin Edge Cleanup',          (SELECT user_id FROM users WHERE username='ava.patel'),    'Panmure Basin, Auckland', 'River',     CURRENT_DATE + 16, TIME '09:30', TIME '12:00', 150, 'Cleanup around basin edges to protect water quality.', 'Gloves, bags, grabbers', 'Avoid slippery edges; work in pairs.'),
('Hobsonville Point Coastal Walk',      (SELECT user_id FROM users WHERE username='jack.wilson'),  'Hobsonville Point, Auckland', 'Beach',   CURRENT_DATE + 17, TIME '09:00', TIME '11:30', 150, 'Coastal walk cleanup near paths and lookouts.', 'Gloves, bags', 'Watch footing; sunscreen.'),
('Manukau Harbour Shoreline Cleanup',   (SELECT user_id FROM users WHERE username='ava.patel'),    'Mangere Bridge, Auckland', 'Beach',     CURRENT_DATE + 18, TIME '10:00', TIME '12:30', 150, 'Shoreline cleanup to prevent plastics entering harbour.', 'Gloves, bags, grabbers', 'Mind tides; avoid unknown containers.'),
('Parnell Rose Gardens Quick Clean',    (SELECT user_id FROM users WHERE username='sophie.king'),  'Parnell Rose Gardens, Auckland', 'Park',   CURRENT_DATE + 19, TIME '09:00', TIME '10:30', 90,  'Short tidy around paths and picnic areas.', 'Gloves, bags', 'Stay on paths; respect gardens.'),
('Devonport Waterfront Cleanup',        (SELECT user_id FROM users WHERE username='jack.wilson'),  'Devonport Waterfront, Auckland', 'Beach',  CURRENT_DATE + 20, TIME '09:30', TIME '11:30', 120, 'Waterfront cleanup for wind-blown plastics and bottles.', 'Gloves, bags, grabbers', 'Be mindful near ferry areas.'),
('Henderson Park Community Event',      (SELECT user_id FROM users WHERE username='ethan.chen'),   'Henderson Park, Auckland', 'Community', CURRENT_DATE + 21, TIME '10:00', TIME '12:00', 120, 'Community cleanup plus short recycling talk.', 'Gloves, bags, sorting bins', 'Closed shoes; hydrate; follow leader instructions.');

-- =========================================================
-- 3) REGISTRATIONS (>=20)
--    Past events -> attended; Future events -> registered
-- =========================================================
INSERT INTO eventregistrations (event_id, volunteer_id, attendance, reminder_flag)
VALUES
-- PAST (attended)
((SELECT event_id FROM events WHERE event_name='Takapuna Beach Morning Cleanup'), (SELECT user_id FROM users WHERE username='liam.brown'), 'attended', FALSE),
((SELECT event_id FROM events WHERE event_name='Takapuna Beach Morning Cleanup'), (SELECT user_id FROM users WHERE username='olivia.wang'), 'attended', FALSE),
((SELECT event_id FROM events WHERE event_name='Takapuna Beach Morning Cleanup'), (SELECT user_id FROM users WHERE username='daniel.kim'), 'attended', FALSE),
((SELECT event_id FROM events WHERE event_name='Takapuna Beach Morning Cleanup'), (SELECT user_id FROM users WHERE username='emma.roberts'), 'attended', FALSE),

((SELECT event_id FROM events WHERE event_name='Onehunga Foreshore Waste Sort'), (SELECT user_id FROM users WHERE username='lucas.li'), 'attended', FALSE),
((SELECT event_id FROM events WHERE event_name='Onehunga Foreshore Waste Sort'), (SELECT user_id FROM users WHERE username='henry.zhang'), 'attended', FALSE),

((SELECT event_id FROM events WHERE event_name='Mt Albert Park Litter Patrol'), (SELECT user_id FROM users WHERE username='isla.taylor'), 'attended', FALSE),
((SELECT event_id FROM events WHERE event_name='Mt Albert Park Litter Patrol'), (SELECT user_id FROM users WHERE username='benjamin.ng'), 'attended', FALSE),

((SELECT event_id FROM events WHERE event_name='Meadowbank Stream Edge Cleanup'), (SELECT user_id FROM users WHERE username='william.singh'), 'attended', FALSE),
((SELECT event_id FROM events WHERE event_name='Meadowbank Stream Edge Cleanup'), (SELECT user_id FROM users WHERE username='grace.ahmed'), 'attended', FALSE),

((SELECT event_id FROM events WHERE event_name='Auckland CBD Laneway Clean'), (SELECT user_id FROM users WHERE username='charlotte.lee'), 'attended', FALSE),
((SELECT event_id FROM events WHERE event_name='Auckland CBD Laneway Clean'), (SELECT user_id FROM users WHERE username='zoe.martin'), 'attended', FALSE),

-- FUTURE (registered)
((SELECT event_id FROM events WHERE event_name='Mangere Mountain Reserve Cleanup'), (SELECT user_id FROM users WHERE username='ryan.clark'), 'registered', FALSE),
((SELECT event_id FROM events WHERE event_name='Mangere Mountain Reserve Cleanup'), (SELECT user_id FROM users WHERE username='ella.johnson'), 'registered', FALSE),

((SELECT event_id FROM events WHERE event_name='Newmarket Shopping Strip Sweep'), (SELECT user_id FROM users WHERE username='kai.robinson'), 'registered', FALSE),
((SELECT event_id FROM events WHERE event_name='Newmarket Shopping Strip Sweep'), (SELECT user_id FROM users WHERE username='chloe.moore'), 'registered', FALSE),

((SELECT event_id FROM events WHERE event_name='Point Chev Coastal Cleanup'), (SELECT user_id FROM users WHERE username='leo.anderson'), 'registered', FALSE),
((SELECT event_id FROM events WHERE event_name='Point Chev Coastal Cleanup'), (SELECT user_id FROM users WHERE username='hana.williams'), 'registered', FALSE),

((SELECT event_id FROM events WHERE event_name='Otahuhu Community Clean Day'), (SELECT user_id FROM users WHERE username='mia.harris'), 'registered', FALSE),
((SELECT event_id FROM events WHERE event_name='Grey Lynn Park Recycling Focus'), (SELECT user_id FROM users WHERE username='james.miller'), 'registered', FALSE),

((SELECT event_id FROM events WHERE event_name='Henderson Park Community Event'), (SELECT user_id FROM users WHERE username='liam.brown'), 'registered', FALSE),
((SELECT event_id FROM events WHERE event_name='Henderson Park Community Event'), (SELECT user_id FROM users WHERE username='emma.roberts'), 'registered', FALSE),
((SELECT event_id FROM events WHERE event_name='Henderson Park Community Event'), (SELECT user_id FROM users WHERE username='grace.ahmed'), 'registered', TRUE);

-- =========================================================
-- 4) EVENT OUTCOMES (ONLY for past events)
-- =========================================================
INSERT INTO eventoutcomes
(event_id, num_attendees, bags_collected, recyclables_sorted, other_achievements, recorded_by, recorded_at)
VALUES
((SELECT event_id FROM events WHERE event_name='Takapuna Beach Morning Cleanup'), 14, 22, 6,
 'Found and safely disposed of fishing line; reported one hazardous item to leader.',
 (SELECT user_id FROM users WHERE username='jack.wilson'), NOW() - INTERVAL '1 day'),

((SELECT event_id FROM events WHERE event_name='Onehunga Foreshore Waste Sort'), 12, 18, 7,
 'Did a quick recycling demo; separated glass and cans; flagged one sharp item for safe disposal.',
 (SELECT user_id FROM users WHERE username='mia.ngata'), NOW() - INTERVAL '4 days'),

((SELECT event_id FROM events WHERE event_name='Mt Albert Park Litter Patrol'), 9, 11, 3,
 'Cleared picnic area and track edges; noted bin overflow point for follow-up.',
 (SELECT user_id FROM users WHERE username='ethan.chen'), NOW() - INTERVAL '5 days'),

((SELECT event_id FROM events WHERE event_name='Meadowbank Stream Edge Cleanup'), 10, 14, 5,
 'Removed litter near stream edge; reminded team to keep distance from slippery sections.',
 (SELECT user_id FROM users WHERE username='ava.patel'), NOW() - INTERVAL '7 days'),

((SELECT event_id FROM events WHERE event_name='Auckland CBD Laneway Clean'), 8, 9, 2,
 'Collected many cigarette butts; reminded group about safe handling and disposal.',
 (SELECT user_id FROM users WHERE username='sophie.king'), NOW() - INTERVAL '9 days');

-- =========================================================
-- 5) FEEDBACK (ONLY for past events)
-- =========================================================
INSERT INTO feedback
(event_id, volunteer_id, rating, comments, submitted_at)
VALUES
-- Takapuna
((SELECT event_id FROM events WHERE event_name='Takapuna Beach Morning Cleanup'), (SELECT user_id FROM users WHERE username='liam.brown'), 5,
 'Well organised and the leader explained what to watch out for. Great vibe.', NOW() - INTERVAL '1 day'),
((SELECT event_id FROM events WHERE event_name='Takapuna Beach Morning Cleanup'), (SELECT user_id FROM users WHERE username='olivia.wang'), 4,
 'Loved it. A short wrap-up on sorting recyclables would make it even better.', NOW() - INTERVAL '1 day'),
((SELECT event_id FROM events WHERE event_name='Takapuna Beach Morning Cleanup'), (SELECT user_id FROM users WHERE username='daniel.kim'), 5,
 'Good equipment and clear safety instructions. Happy to join again.', NOW() - INTERVAL '1 day'),

-- Onehunga
((SELECT event_id FROM events WHERE event_name='Onehunga Foreshore Waste Sort'), (SELECT user_id FROM users WHERE username='lucas.li'), 5,
 'Good sorting tips and clear instructions. Felt meaningful and well organised.', NOW() - INTERVAL '4 days'),
((SELECT event_id FROM events WHERE event_name='Onehunga Foreshore Waste Sort'), (SELECT user_id FROM users WHERE username='henry.zhang'), 4,
 'Great community vibe. Would be better with one extra set of sorting bins.', NOW() - INTERVAL '4 days'),

-- Mt Albert
((SELECT event_id FROM events WHERE event_name='Mt Albert Park Litter Patrol'), (SELECT user_id FROM users WHERE username='isla.taylor'), 5,
 'Nice short patrol and easy to follow. Park looked cleaner right away.', NOW() - INTERVAL '5 days'),
((SELECT event_id FROM events WHERE event_name='Mt Albert Park Litter Patrol'), (SELECT user_id FROM users WHERE username='benjamin.ng'), 4,
 'Smooth event. Would love a quick recap at the end of what was collected.', NOW() - INTERVAL '5 days'),

-- Meadowbank
((SELECT event_id FROM events WHERE event_name='Meadowbank Stream Edge Cleanup'), (SELECT user_id FROM users WHERE username='william.singh'), 4,
 'Good teamwork and clear safety guidance around the stream edges.', NOW() - INTERVAL '7 days'),
((SELECT event_id FROM events WHERE event_name='Meadowbank Stream Edge Cleanup'), (SELECT user_id FROM users WHERE username='grace.ahmed'), 5,
 'Well coordinated and the leader kept everyone safe. Great experience.', NOW() - INTERVAL '7 days'),

-- CBD Laneway
((SELECT event_id FROM events WHERE event_name='Auckland CBD Laneway Clean'), (SELECT user_id FROM users WHERE username='charlotte.lee'), 4,
 'Good quick clean after work hours. Gloves/tongs were useful.', NOW() - INTERVAL '9 days'),
((SELECT event_id FROM events WHERE event_name='Auckland CBD Laneway Clean'), (SELECT user_id FROM users WHERE username='zoe.martin'), 4,
 'Meeting point was clear and the leader kept it safe near traffic.', NOW() - INTERVAL '9 days');

COMMIT;