drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  year text not null,
  term text not null,
  type text not null,
  title text not null,
  link text not null,
  checksum text not null
);