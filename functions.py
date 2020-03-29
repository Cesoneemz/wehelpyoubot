from db import connect as connect
from bad_words import bad_words as bad_words


def check_bad_words(message):
    msg = ''
    for word in bad_words:
        if word in message.replace(' ', ''):
            msg += f"{str(word)} "

    return msg


@connect
def check_is_banned(cursor, member_id):
    try:
        result = cursor.execute("SELECT isBanned FROM messages WHERE author = %s", (member_id,))
        (result,) = cursor.fetchone()
    except:
        result = 0
    return False if result == 0 else True


@connect
def check_is_message_exists(cursor, member_id):
    result = cursor.execute("SELECT id FROM messages WHERE author = %s", (member_id,))
    result = cursor.fetchall()
    return True if len(result) > 0 else False


@connect
def like_on_message(cursor, author):
    cursor.execute("UPDATE messages SET likes = likes + 1 WHERE author = %s", (author,))


@connect
def report_to_message(cursor, author, text):
    cursor.execute("INSERT INTO reports (author, message) VALUES (%s, %s)", (author, text))


@connect
def get_help_message(cursor):
    cursor.execute("SELECT message, author FROM messages WHERE isBanned = 0 ORDER BY random() LIMIT 1")
    (help_text, author) = cursor.fetchone()
    return help_text, author


@connect
def add_new_message(cursor, message):
    cursor.execute("INSERT INTO messages (author, message) VALUES (%s, %s)", (message.chat.username, message.text))


@connect
def send_user_his_message(cursor, message):
    result = cursor.execute("SELECT message, likes FROM messages WHERE author = %s", (message.chat.username,))
    (his_text, his_likes) = cursor.fetchone()
    msg = f"Ваше сообщение:\n\n{his_text}\n\nЛайки у сообщения: {his_likes}"
    return msg


@connect
def edit_message(cursor, message):
    cursor.execute("UPDATE messages SET message = ? WHERE author = %s",
                   (message.text, message.chat.username))


@connect
def delete_message(cursor, message):
    cursor.execute("DELETE FROM messages WHERE author = %s", (message.chat.username,))
