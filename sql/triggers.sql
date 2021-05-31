/*Message on Mural Notifications*/
CREATE OR REPLACE FUNCTION notify_users_comment()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
$$
BEGIN
    INSERT INTO notification(person_id, auction_id, seen, type, content, date_time)
    SELECT DISTINCT person_id, NEW.auction_id, FALSE, 'Comentário', NEW.content,current_timestamp 
    FROM comment WHERE auction_id = NEW.auction_id;
    RETURN NULL;
END;

$$;

CREATE TRIGGER comment_trigger
    AFTER INSERT
    ON comment
    FOR EACH ROW
    EXECUTE PROCEDURE notify_users_comment();

/*Notify users about auction ending*/
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
        values (NEW.person_id, NEW.id, FALSE, 'Fim de Leilão', "No Bids", current_timestamp);
    END IF;

    RETURN NULL;
END;

$$;

CREATE TRIGGER auction_trigger
    AFTER UPDATE
    ON auction
    FOR EACH ROW
    EXECUTE PROCEDURE notify_users_auction();