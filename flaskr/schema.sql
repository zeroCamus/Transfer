drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  author strng not null,
  text string not null
);
create table users (
  username string primary key,
  password string not null,
  email string not null
);