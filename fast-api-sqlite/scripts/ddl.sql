DROP 
  TABLE roles;
DROP 
  TABLE genders;
DROP 
  TABLE users;
PRAGMA foreign_keys = ON;
CREATE TABLE roles (
  id INTEGER NOT NULL PRIMARY KEY, 
  role TEXT NOT NULL
);
CREATE TABLE genders (
  id INTEGER NOT NULL PRIMARY KEY, 
  gender TEXT NOT NULL
);
CREATE TABLE users (
  id TEXT NOT NULL PRIMARY KEY, 
  first TEXT NOT NULL, 
  middle TEXT, 
  last TEXT NOT NULL, 
  gender_id INTEGER NOT NULL, 
  role_id INTEGER NOT NULL, 
  FOREIGN KEY (gender_id) REFERENCES genders (id), 
  FOREIGN KEY (role_id) REFERENCES roles (id)
);
INSERT INTO roles 
VALUES 
  (1, 'admin'), 
  (2, 'user'), 
  (3, 'student');
INSERT INTO genders 
VALUES 
  (1, 'male'), 
  (2, 'female');
INSERT INTO users 
VALUES 
  (
    '0fe0f9c8-41d4-46c7-9f83-f2c8630fa12f', 
    'John', 'A', 'Smith', 1, 1
  ), 
  (
    '8efac412-29f1-4069-aa0b-c0a09c095d58', 
    'Bob', 'B', 'Jones', 1, 2
  ), 
  (
    'd199b973-3fa7-4c41-a5d1-725d52162961', 
    'Marry', 'C', 'Foo', 2, 3
  );
  