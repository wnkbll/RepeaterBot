BOT: dict[str, str] = {
    "on_start_command": "What do you want to change?",

    "on_posts_command": "What do you want to do with posts?",
    "on_posts_edit_callback": "Choose the post you want to edit.",
    "on_posts_edit_waiting": "Send edited post.\nYou can attach no more than one image.",
    "on_posts_list_callback": "Choose the post you want to check.",
    "on_posts_delete_callback": "Choose the post you want to delete.",
    "current_posts_number": "Current amount of posts",

    "on_chats_command": "What do you want to do with chats?",
    "on_chats_add_callback": "Add a new chat in the format {link}: {time}.\nThe time must be a number or a sequence in the format {HH:mm, HH:mm}",
    "on_chats_edit_callback": "Choose the chat you want to edit",
    "on_chats_edit_waiting": "Enter a new time for this chat.\nThe time must be a number or a sequence in the format {HH:mm, HH:mm}",
    "on_chats_delete_callback": "Choose the chat you want to delete",
    "current_chats": "Current list of chats",

    "on_sleep_command": "What do you want to do with sleep time?",
    "on_sleep_edit_start": "Send the new sleep start time in HH:mm format. For example, 22:15.",
    "on_sleep_edit_stop": "Send the new sleep end time in HH:mm format. For example, 22:15.",
    "current_sleep_time": "Текущее время сна",

    "on_emtpy_posts_list": "List of posts is empty.",
    "on_empty_chats_list": "List of chats is empty.",

    "on_bad_time": "You entered the wrong time",
    "on_bad_link": "You entered the wrong link",
}

CLIENT: dict[str, str] = {
    "post_sent": "Message has been sent into {title}"
}


def register(strings: dict) -> dict[str, dict[str, str]]:
    lang = "en"
    strings[lang] = {}

    for item in BOT.items():
        strings[lang][item[0]] = item[1]

    for item in CLIENT.items():
        strings[lang][item[0]] = item[1]

    return strings
