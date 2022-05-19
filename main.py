import requests
import datetime
from pprint import pp, pprint
from yandex import YaUploader


class vkuser:

    def __init__(self, _id: str):
        self.id = _id

    def get_photo(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': 'profile',
            'extended': '1',
            'access_token': read_token()[0].strip(),
            'v': '5.131'
        }
        res = requests.get(url, params=params)
        return res.json()

    def all_topsize_ph(self):
        photo_dct = {}  # {кл-во лайков: url}
        photo_dct_size = {}  # {размер:{кл-во лайков: url}}
        count = -1
        for photo in self.get_photo()['response']['items']:
            max_size = 0
            size_dict = {}
            count += 1
            for sizes in photo['sizes']:
                if int(sizes['height']) * int(sizes['width']) > max_size or \
                        int(sizes['height']) * int(sizes['width']) == 0:
                    max_size = int(sizes['height']) * int(sizes['width'])
                    max_size_url = sizes['url']
            if str(photo['likes']['count']) not in photo_dct:
                photo_dct[str(photo['likes']['count'])] = max_size_url
                size_dict[str(photo['likes']['count'])] = max_size_url
            else:
                photo_dct[str(photo['likes']['count']) + self.time_reform(photo['date'])] = max_size_url
                size_dict[str(photo['likes']['count']) + self.time_reform(photo['date'])] = max_size_url
            if max_size not in photo_dct_size:
                photo_dct_size[max_size] = size_dict
            else:
                photo_dct_size[max_size + count] = size_dict
        return photo_dct_size

    def time_reform(self, timestamp):
        value = datetime.datetime.fromtimestamp(timestamp)
        return value.strftime('__%Y-%m-%d')

    def top_photos(self, qty):
        top_list = sorted(self.all_topsize_ph().items())[-qty:]
        top_dict = {}
        for photo in top_list:
            top_dict.update(photo[1])
        return top_dict

def read_token():
    with open('input.txt', 'r') as file:
        token = file.readlines()
        return token

def write_json(input):
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(input)

def interface():
    check = input('ПРЕДУПРЕЖДЕНИЕ! токены и id вносятся в файл "input.txt": '
                  '\nПервая строка - токен вконтакте \nВторая строка - токен яндекс'
                  '\nТретья строка - id пользователя вконтакте'
                  '\n\nТокены и id внесены в "input.txt" ? (y/n) ')
    if check == 'y':
        count = int(input('Введите количество обрабатываемых фотографий профиля: '))
        ya_token = read_token()[1].strip()
        vk_id = read_token()[2].strip()
        VK_USER_1 = vkuser(vk_id)
        vk_uploader = YaUploader(ya_token)
        data = vk_uploader.vk_upload(VK_USER_1.top_photos(count), vk_id)
        write_json(data)
        print('Отчет по загруженным файлам записан в файл "data.json"')
    else:
        return


if __name__ == '__main__':
    interface()
