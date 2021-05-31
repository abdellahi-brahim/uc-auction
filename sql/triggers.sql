/*Message on Mural Notifications*/
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