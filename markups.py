from telebot import types as t

markup = t.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
i_need_help_btn = t.KeyboardButton('Мне нужна помощь!')
add_message_btn = t.KeyboardButton('Добавить сообщение')
my_message_btn = t.KeyboardButton('Моё сообщение')
markup.add(i_need_help_btn, add_message_btn, my_message_btn)

my_message_markup = t.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
edit_my_message_btn = t.KeyboardButton('Изменить сообщение')
delete_my_message_btn = t.KeyboardButton('Удалить сообщение')
go_back_btn = t.KeyboardButton('Назад')
my_message_markup.add(edit_my_message_btn, delete_my_message_btn, go_back_btn)

admin_markup = t.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
show_reports_btn = t.KeyboardButton('Показать все жалобы')
delete_report_btn = t.KeyboardButton('Удалить жалобу')
clear_reports_btn = t.KeyboardButton('Очистить жалобы')
ban_message_btn = t.KeyboardButton('Забанить автора')
unban_message_btn = t.KeyboardButton('Разбанить автора')
delete_message_btn = t.KeyboardButton('Удалить сообщение(Админ)')
go_back_admin_btn = t.KeyboardButton('Выход из админ-панели')
admin_markup.add(show_reports_btn, delete_report_btn, clear_reports_btn, ban_message_btn, unban_message_btn,
                 delete_message_btn, go_back_admin_btn)

like_dismiss_markup = t.InlineKeyboardMarkup(row_width=2)
like_btn = t.InlineKeyboardButton(text="Лайк", callback_data="like")
dismiss = t.InlineKeyboardButton(text="Репорт", callback_data="report")
like_dismiss_markup.add(like_btn, dismiss)
