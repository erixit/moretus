-- Moretus SQLite Schema
-- Converted from MySQL for SQLite compatibility

-- Table structure for spelers (chess players)
CREATE TABLE IF NOT EXISTS spelers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    voornaam TEXT NOT NULL DEFAULT '',
    achternaam TEXT NOT NULL DEFAULT '',
    fide_elo INTEGER DEFAULT 0,
    sterktelijst_elo INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample data - chess players
INSERT OR IGNORE INTO spelers (id, voornaam, achternaam, fide_elo, sterktelijst_elo) VALUES
(1, 'Gerry', 'De Rop', 2080, 2080),
(2, 'Alain', 'Talon', 2030, 2030),
(3, 'Tim', 'Rüssche', 2002, 2002),
(4, 'Tomas Dias', 'Machado', 1986, 1986),
(5, 'Erik', 'Vande Velde', 1919, 1919),
(6, 'Bart', 'Slachmuylders', 1912, 1912),
(7, 'Sam', 'Van Hoofstat', 1912, 1912),
(8, 'Gert', 'Van Bunderen', 1888, 1888),
(9, 'Benny', 'Kleykens', 1871, 1871),
(10, 'Tom', 'Van Hoofstat', 2009, 2009);
