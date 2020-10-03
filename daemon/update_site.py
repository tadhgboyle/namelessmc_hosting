import compose
import db
import nginx
import sftp


def get_website_info(website_id):
    with db.open_db() as conn:
        with conn.cursor() as cur:
            query = "SELECT domain,use_https,db_password FROM users_website WHERE id=%s"
            cur.execute(query, (website_id,))
            data = cur.fetchone()
            return data


def run(website_id):
    (domain, use_https, db_password) = get_website_info(website_id)

    compose.install(website_id, domain, use_https, db_password)
    nginx.install(website_id, domain, use_https)
    sftp.generate_users_config() # in case SFTP password has changed
