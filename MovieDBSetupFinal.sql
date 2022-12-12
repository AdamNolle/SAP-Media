create database sapmedia;
use sapmedia;
create table Movie(
id integer primary key auto_increment,
name varchar(80) not null unique,
summary varchar(1000),
director varchar(80),
duration integer,
moviePoster blob,
watched bool not null default false
);

create table User(
username varchar(80) primary key,
password varchar(80),
fName varchar(80) not null,
mName varchar(80) not null,
lName varchar(80) not null,
admin bool not null default false
);

create table User_Genre(
username varchar(80),
favoriteGenre varchar(80),
foreign key(username) references User(username)
	on delete cascade
    on update cascade,
primary key(username, favoriteGenre)
);

create table Movie_Cast(
movieID integer ,
castName varchar(80),
foreign key(movieID) references Movie(id)
	on delete cascade
    on update cascade,
primary key(movieID, castName)
);

create table Platform(
name varchar(80) primary key,
ownerUsername varchar(80),
cost float,
url varchar(80),
foreign key(ownerUsername) references User(username)
	on delete set null
    on update cascade
);

create table Rating(
id integer primary key auto_increment,
platformRating float check(platformRating > 0 and platformRating <= 5),
platformName varchar(80),
username varchar(80),
movieID integer,
foreign key(platformName) references Platform(name)
	on delete cascade
    on update cascade,
foreign key(username) references User(username)
	on delete cascade
    on update cascade,
foreign key(movieID) references Movie(id)
	on delete cascade
    on update cascade
);

create table Watch_On(
movieID integer,
platformName varchar(80),
foreign key(movieID) references Movie(id)
	on delete cascade
    on update cascade,
foreign key(platformName) references Platform(name)
	on delete cascade
    on update cascade,
primary key(movieID, platformName)
);

create table User_Rating(
ratingID integer,
userRating float check(userRating > 0 and userRating <= 5),
foreign key(ratingID) references Rating(id)
	on delete cascade
    on update cascade,
primary key(ratingID, userRating)
);

create table Movie_Genre(
movieID integer,
genreName varchar(80),
foreign key(movieID) references Movie(id)
	on delete cascade
    on update cascade,
primary key(movieID, genreName)
);

insert into user values('sudpot','password','Sudeep','Sai','Potluri',0);
insert into user_genre values('sudpot','Sports');
insert into user values('pjmetz','password','Paul','Joseph','Metzger',0);
insert into user_genre values('pjmetz','Horror');
insert into user values('anolle','password','Adam','Michael','Nolle',0);
insert into user_genre values('anolle','Comedy');

insert into platform values('Netflix', 'pjmetz', 12.99,'https://www.netflix.com/');
insert into platform values('Hulu', 'sudpot', 7.99,'https://www.hulu.com/welcome');
insert into platform values('Amazon Prime', 'anolle', 14.99,'https://www.amazon.com/Prime-Video/b?node=2676882011');
insert into platform values('HBO Max', 'sudpot', 11.99,'https://www.hbomax.com/');
insert into platform values('Paramount', 'anolle', 9.99,'https://www.paramountplus.com/');

insert into movie(name, summary, director, duration, moviePoster, watched) values('Borat', 'Comedy Moviefilm', 'Sacha Baron Cohen', 84, '', 1);
insert into movie(name, summary, director, duration, moviePoster, watched) values('The Shining', 'Scary Jack Nicholson Cold Hotel', 'Stanley Kubrick', 146, '', 1);
insert into movie(name, summary, director, duration, moviePoster, watched) values('Moneyball', 'Sports Movie Bradley Pitt', 'Bennett Miller', 133, '', 0);

insert into movie_cast values(1, 'Sacha Baron Cohen');
insert into movie_cast values(1, 'Ken Davitian');
insert into movie_cast values(1, 'Pamela Anderson');
insert into movie_cast values(2, 'Jack Nicholson');
insert into movie_cast values(2, 'Shelley Duvall');
insert into movie_cast values(2, 'Scatman Crothers');
insert into movie_cast values(3, 'Brad Pitt');
insert into movie_cast values(3, 'Jonah Hill');
insert into movie_cast values(3, 'Chris Pratt');

insert into movie_genre values(1, 'Comedy');
insert into movie_genre values(2, 'Horror');
insert into movie_genre values(3, 'Sports');

insert into watch_on values(1, 'Amazon Prime');
insert into watch_on values(2, 'HBO Max');
insert into watch_on values(3, 'Paramount');

insert into rating(platformRating, platformName, username, movieID) values(4.3, 'Amazon Prime', 'pjmetz', 1);
insert into user_rating values(1, 5);
insert into rating(platformRating, platformName, username, movieID) values(4.8, 'HBO Max', 'anolle', 2);
insert into user_rating values(2, 4.3);