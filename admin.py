from db import connect as connect

admins_list = ['Cesoneemz']


@connect
def show_all_reports(cursor):
    msg = "***\n\n"
    result = cursor.execute("SELECT * FROM reports")
    result = cursor.fetchall()
    for author, message in result:
        msg += f"Автор сообщения: {author}\n\nСообщение: {message}\n\n***\n\n"
    return msg


@connect
def ban_author(cursor, author):
    cursor.execute("UPDATE messages SET isBanned = 1 WHERE author = %s", (author,))


@connect
def unban_author(cursor, author):
    cursor.execute("UPDATE messages SET isBanned = 0 WHERE author = %s", (author,))


@connect
def delete_report(cursor, author):
    cursor.execute("DELETE FROM reports WHERE author = %s", (author,))


@connect
def clear_all_reports(cursor):
    cursor.execute("DELETE FROM reports")


@connect
def delete_message_from_admin(cursor, author):
    cursor.execute("DELETE FROM messages WHERE author = %s", (author,))


@connect
def add_admin_to_admins_list(cursor, admin_name):
    admins_list.append(admin_name)


@connect
def delete_admin_from_admins_list(cursor, admin_name):
    admins_list.remove(admin_name)
