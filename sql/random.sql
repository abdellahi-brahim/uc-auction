insert into person(phone, city, street, zipcode, username, password, first_name, last_name)
values(938258422, 'Coimbra', 'Rua Cidade Dili, Bloco 13, 1º Direito', '3020-208', 'abd', 'password', 'Abdellahi', 'Brahim');

update auction set title = 'novo titulo de eleicao',minimum_price = 200 where id = id and person_id = 1;

insert into version(title, description, edited, auction_id)
select a.title, a.description, current_timestamp, a.id
from auction a
where a.id = 1;

insert into comment(person_id, auction_id, content, comment_date)
values(1, 1, 'Conteudo', current_timestamp);

select coalesce((select id from person where id = 2), 0);

select password, id from person where username = 'abd';

select * from auction where id = 2;

drop table if exists auction cascade;
drop table if exists comment cascade;
drop table if exists notification cascade;
drop table if exists person cascade;
drop table if exists bid cascade;

CREATE TABLE person (
	id	 BIGINT,
	phone	 VARCHAR(9) UNIQUE,
	city	 VARCHAR(512) NOT NULL,
	street	 VARCHAR(512) NOT NULL,
	zipcode	 VARCHAR(7) NOT NULL,
	username	 VARCHAR(50) UNIQUE NOT NULL,
	password	 VARCHAR(50) NOT NULL,
	first_name VARCHAR(512) NOT NULL,
	last_name	 VARCHAR(512) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE auction (
	id			 BIGINT,
	title		 VARCHAR(50) NOT NULL,
	description	 VARCHAR(512) NOT NULL,
	minimum_price	 BIGINT NOT NULL,
	start_time		 TIMESTAMP NOT NULL,
	end_time		 TIMESTAMP NOT NULL,
	winner_id		 VARCHAR(512),
	product_isbn	 VARCHAR(512),
	product_description VARCHAR(512),
	person_id		 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE comment (
	content	 VARCHAR(512) NOT NULL,
	comment_date TIMESTAMP NOT NULL,
	auction_id	 BIGINT,
	person_id	 BIGINT,
	PRIMARY KEY(auction_id,person_id)
);

CREATE TABLE bid (
	bid_date	 TIMESTAMP,
	increase	 BIGINT,
	auction_id BIGINT,
	person_id	 BIGINT,
	PRIMARY KEY(auction_id,person_id)
);

CREATE TABLE version (
	title		 BOOL,
	description	 VARCHAR(512),
	edited		 TIMESTAMP,
	auction_id BIGINT NOT NULL
);

CREATE TABLE notification (
	type	 VARCHAR(512) NOT NULL,
	content	 VARCHAR(512) NOT NULL,
	date_time	 TIMESTAMP NOT NULL,
	seen	 BOOL NOT NULL,
	auction_id BIGINT,
	person_id	 BIGINT,
	PRIMARY KEY(auction_id,person_id)
);

ALTER TABLE auction ADD CONSTRAINT auction_fk1 FOREIGN KEY (person_id) REFERENCES person(id);
ALTER TABLE comment ADD CONSTRAINT comment_fk1 FOREIGN KEY (auction_id) REFERENCES auction(id);
ALTER TABLE comment ADD CONSTRAINT comment_fk2 FOREIGN KEY (person_id) REFERENCES person(id);
ALTER TABLE bid ADD CONSTRAINT bid_fk1 FOREIGN KEY (auction_id) REFERENCES auction(id);
ALTER TABLE bid ADD CONSTRAINT bid_fk2 FOREIGN KEY (person_id) REFERENCES person(id);
ALTER TABLE version ADD CONSTRAINT version_fk1 FOREIGN KEY (auction_id) REFERENCES auction(id);
ALTER TABLE notification ADD CONSTRAINT notification_fk1 FOREIGN KEY (auction_id) REFERENCES auction(id);
ALTER TABLE notification ADD CONSTRAINT notification_fk2 FOREIGN KEY (person_id) REFERENCES person(id);

CREATE TABLE comment (
	content	 VARCHAR(512) NOT NULL,
	comment_date TIMESTAMP NOT NULL,
	id		 BIGINT,
	auction_id	 BIGINT,
	person_id	 BIGINT,
	PRIMARY KEY(id,auction_id,person_id)
);


CREATE OR REPLACE FUNCTION notify_users_comment()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
$$
BEGIN
    INSERT INTO notification(person_id, auction_id, seen, type, content, date_time)
    SELECT DISTINCT person_id, NEW.auction_id, FALSE, 'Comentário', NEW.content,current_timestamp FROM comment WHERE auction_id = NEW.auction_id;
    RETURN NULL;
END;

$$;

CREATE TRIGGER comment_trigger
    AFTER INSERT
    ON comment
    FOR EACH ROW
    EXECUTE PROCEDURE notify_users_comment();

begin;
lock table bid in access exclusive mode;
insert into bid(auction_id, person_id, increase, bid_date)
select 1, 1, 102, current_timestamp
where not exists
(select * from bid where auction_id = 1 and increase >= 102);
end;

select coalesce(max(increase), 0) from bid;

truncate bid; delete from bid;

alter table bid
	add id BIGINT not null;

create unique index bid_id_uindex
	on bid (id);

alter table bid drop constraint bid_pkey;

alter table bid
	add constraint bid_pk
		primary key (id);

alter table bid
	add constraint bid_pkey
		unique (auction_id, person_id);

create unique index bid_increase_uindex
	on bid (increase);


select min(end_time) from auction where winner_id is null;

update notification set seen = TRUE where person_id = 1 and seen = FALSE;

CREATE OR REPLACE FUNCTION notify_users_auction()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
$$
BEGIN
    IF NEW IS NOT NULL THEN
        INSERT INTO notification(person_id, auction_id, seen, type, content, date_time)
        SELECT DISTINCT person_id, NEW.id, FALSE, 'Fim de Leilão', NEW.winner_id, current_timestamp
        FROM bid WHERE auction_id = NEW.id;

        INSERT INTO notification(person_id, auction_id, seen, type, content, date_time)
        values (NEW.person_id, NEW.id, FALSE, 'Fim de Leilão', NEW.winner_id, current_timestamp);
    END IF;

    RETURN NULL;
END;

$$;

CREATE TRIGGER auction_trigger
    AFTER UPDATE
    ON auction
    FOR EACH ROW
    EXECUTE PROCEDURE notify_users_auction();


select * from auction;

update auction a
set winner_id = coalesce((select a.id
from bid b
where a.id = b.auction_id
group by a.id), 0)
where winner_id is null and end_time < current_timestamp;

select a.id
from auction a, bid b
where a.id = b.auction_id and b.increase =
(select max(b2.increase) from bid b2 where a.id = b2.auction_id)
group by a.id;

CREATE OR REPLACE FUNCTION notify_users_auction()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
$$
BEGIN
    IF NEW IS NOT NULL THEN
        INSERT INTO notification(person_id, auction_id, seen, type, content, date_time)
        SELECT DISTINCT person_id, NEW.id, FALSE, 'Fim de Leilão', NEW.winner_id, current_timestamp
        FROM bid WHERE auction_id = NEW.id;

        INSERT INTO notification(person_id, auction_id, seen, type, content, date_time)
        values (NEW.person_id, NEW.id, FALSE, 'Fim de Leilão', NEW.winner_id, current_timestamp);
    ELSE
        INSERT INTO notification(person_id, auction_id, seen, type, content, date_time)
        values (NEW.person_id, NEW.id, FALSE, 'Fim de Leilão', 'No Bids', current_timestamp);
    END IF;

    RETURN NULL;
END;

$$;

select * from auction where id = 1;

select * from comment where auction_id = 1;


select id, title, description from auction where end_time>current_timestamp;

select current_timestamp;

