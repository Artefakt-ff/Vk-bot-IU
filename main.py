from components.answering import get_answer
from components.connection import get_message, send_message
from components.broadcasting import broadcasting

with open("components/previous_id.txt", 'r') as f:
    previous_message_id = int(f.readline())
broadcasting_flag = False
while True:
    while True:
        message = get_message()['response']['items'][0]
        if message['id'] != previous_message_id:
            previous_message_id = message['id']
            with open("components/previous_id.txt", 'w') as f:
                f.write(str(previous_message_id))
            user_id = message['user_id']
            body = message['body']
            if user_id == 81416042:
                send_message(user_id, 'иди нахуй &#128525;')
            elif broadcasting_flag:
                broadcasting_flag = False
                broadcasting(user_id, body)
            else:
                if body == 'Широкое вещание':
                    broadcasting_flag = True
                    send_message(user_id, 'Введите сообщение для вещания: ')
                else:
                    send_message(user_id, get_answer(body))
