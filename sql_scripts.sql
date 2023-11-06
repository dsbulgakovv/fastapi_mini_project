CREATE TABLE if not exists dogs (
	pk SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT null,
	kind VARCHAR(255) NOT NULL
);

CREATE table if not exists post (
	id SERIAL PRIMARY KEY,
	timestamp_log TIMESTAMP UNIQUE NOT NULL
);

--drop table dogs;

select * from dogs;

select * from post;

insert into
	dogs(name,kind)
values
	('Bob', 'terrier'),
	('Marli', 'bulldog'),
    ('Snoopy', 'dalmatian'),
    ('Rex', 'dalmatian'),
    ('Pongo', 'dalmatian'),
    ('Tillman', 'bulldog'),
    ('Uga', 'bulldog');


