create database movie_db;

use movie_db;

create table admin(
id int auto_increment,
name varchar(10),
email varchar(30),
password varchar(12),
primary key(id)
);



create table movie(
m_id int primary key auto_increment,
m_name varchar(20),
m_release date,
m_language varchar(10),
m_synopsis text
);

alter table movie 
add column 
image_path varchar(1024);




create table venue(
v_id int primary key auto_increment,
v_capacity int,
v_name varchar(20)
);


create table visitor(
v_id int primary key auto_increment,
v_name varchar(10) not null,
phno numeric(10) not null,
email varchar(30) not null,
password varchar(12) not null
);


alter table visitor 
add constraint primary key(email);



create table payment(
payment_id int primary key,
v_email varchar(20) references visitor(email),
m_name varchar(20) references movie(m_name),
amount int
);

create table book_ticket(
no_of_ticket int,
m_name varchar(20) references movie(m_name) on delete cascade,
show_no varchar(10),
m_date date,
v_name varchar(20) references venue(v_name) on delete cascade,
vis_email varchar(20) references visitor(email) on delete cascade
);

