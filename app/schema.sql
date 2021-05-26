DROP TABLE IF EXISTS users;

create table users (
  id int generated by default as identity not null,
  login text not null,
  password_hash text not null,
  name text default 'not inserted',
  mail text default 'not inserted',
  primary key (id)
);

insert into users (login, password_hash, name, mail)
values (
  'mj', 
  'qwerty', 
  'Michael Jackson', 
  'first@one'
);

insert into users (login, password_hash, name, mail)
values (
  'user2', 
  'qwerty', 
  'John Adams', 
  'second@one'
);