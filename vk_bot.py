import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token="vk1.a.zZEdRdlMs2gzzDGq6NhF3_Twyq8ukpuRi4MJ0F9yADTHtzNkr8r6n9g3GRrAI00y83RoJhfUG2yh0KlUcs0BCbYHVho3SbvgYBp8LpWy7FR4EugWHaSPlnEpfRABjpK6WrJxQMKnvGaW2Dgy9WwgkGoA7jDjb2WGbifh_pbrMJk5z7EdoBf55KDTDOWj6rn41gCGZbg64mRUJloNJ7h_-w")

longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Новое сообщение:')
        if event.to_me:
            print('Для меня от: ', event.user_id)
        else:
            print('От меня для: ', event.user_id)
        print('Текст:', event.text)