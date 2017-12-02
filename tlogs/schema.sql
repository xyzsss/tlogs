drop table if exists tlog;
create table tlog (
  id integer primary key autoincrement,
  'context' text not null,
  'extra' text not null,
  'time' text not null
);
