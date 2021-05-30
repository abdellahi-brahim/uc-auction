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

