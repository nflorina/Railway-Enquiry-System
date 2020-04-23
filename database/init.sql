create database airplaneservice;
use airplaneservice;

create table flights (
  source varchar(40),
  dest varchar(40),
  departureHour int,
  departureDay int,
  duration int,
  seats int,
  booked int,
  bought int,
  id int,
  price int,
  class int,
  traintype varchar(30),
  sleeproom int,
  primary key (id)
);

insert into flights
  (source, dest, departureHour, departureDay, duration, seats, booked, bought, id, price, class, traintype, sleeproom)
values
   ('Timisoara', 'Constanta',  9, 10, 2, 120, 132, 0, 1, 20, 2, 'P',  1),
   ('Timisoara', 'Constanta', 10, 10, 3, 120, 132, 0, 2, 34, 2, 'A',  1),
   ('Timisoara', 'Constanta', 12, 10, 4, 120, 132, 0, 3, 40, 1, 'R',  1),
   ('Timisoara', 'Constanta', 15, 10, 1, 120, 132, 0, 4, 23, 2, 'IR', 0),
   ('Timisoara', 'Constanta', 16, 10, 2, 120, 132, 0, 5, 10, 2, 'IC', 0),
   ('Timisoara', 'Constanta', 20, 10, 2, 120, 132, 0, 6, 90, 1, 'EN', 0),
   ('Timisoara', 'Constanta', 22, 10, 2, 120, 132, 0, 7, 33, 2, 'EC', 0),
   ('Timisoara', 'Constanta', 23, 10, 1, 120, 132, 0, 8, 54, 1, 'S',  1);



--   ('Bucharest', 'Rome', 9, 10, 2, 120, 132, 0, 1989),
--   ('Bucharest', 'Rome', 10, 10, 2, 120, 132, 0, 1990),
--   ('Rome', 'Vienna', 12, 23, 2, 120, 132, 0, 1991),
--   ('Vienna', 'London', 17, 29, 2, 120, 132, 0, 1992),
--   ('London', 'Munich', 4, 32, 3, 120, 132, 0, 1993),
--   ('Munich', 'Tel-Aviv', 2, 45, 3, 120, 132, 0, 1994),
--   ('Tel-Aviv', 'Warsaw', 11, 55, 3, 120, 132, 0, 1995),
--   ('Warsaw', 'Malmo', 21, 67, 3, 120, 132, 0, 1996),
--   ('Malmo', 'Bucharest', 2, 78, 2, 120, 132, 0, 1997),
--   ('Bucharest', 'Timisoara', 8, 88, 1, 120, 132, 0, 1998),
--   ('Timisioara', 'Cluj', 10, 93, 1, 120, 132, 0, 1999),
--   ('Cluj', 'Bucharest', 16, 99, 1, 120,132, 0,  2000),
--   ('Bucharest', 'Budapest', 10, 110, 2, 120, 132, 0, 2001),
--   ('Budapest', 'Stockholm', 20, 121, 2, 120, 132, 0, 2002),
--   ('Stockholm', 'London', 20, 131, 3, 120, 132, 0, 2003),
--   ('London', 'Bucharest', 8, 139, 3, 120, 132, 0, 2004),
--   ('Bucharest', 'Zurich', 10, 147, 2, 120, 132, 0, 2005),
--   ('Zurich', 'Dublin', 18, 155, 3, 120, 132, 0, 2006),
--   ('Dublin', 'Paris', 20, 157, 3, 120, 132, 0, 2007),
--   ('Paris', 'Zurich', 21, 160, 1, 120, 132, 0, 2008),
--   ('Zurich', 'Munich', 1, 165, 1, 120, 132, 0, 2009),
--   ('Munich', 'Milan', 19, 171, 2, 120, 132, 0, 2010),
--   ( 'Milan', 'Bucharest', 20, 177, 2, 120, 132, 0, 2011),
--   ('Bucharest', 'Warsaw', 12, 180, 2, 120, 132, 0, 2012),
--   ('Warsaw', 'London', 12, 188, 2, 120, 132, 0, 2013),
--   ('London', 'Stockholm', 3, 190, 2, 120, 132, 0, 2014),
--   ('Stockholm', 'Paris', 3, 200, 3, 120, 132, 0, 2015),
--   ('Paris', 'Brussels', 12, 202, 2, 120, 132, 0, 2016),
--   ('Brussels', 'London', 3, 190, 2, 120, 132, 0, 2017),
--   ('London', 'Luxembourg', 3, 190, 2, 120, 132, 0, 2018),
--   ('Luxembourg', 'Zurich', 3, 190, 2, 120, 132, 0, 2019),
--   ('Zurich', 'Bucharest', 3, 200, 2, 120, 132, 0, 2020);
