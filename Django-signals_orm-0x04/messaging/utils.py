

def get_message_thread(message):

    thread = [{
        'id': message.id,
        'sender': message.sender.username,
        'content': message.content,
        'timestamp': message.timestamp,
    }]

    for reply in message.replies.all():
        thread.extend(get_message_thread(reply))
    return thread
