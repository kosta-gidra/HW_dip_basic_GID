import requests
import time
import json


class YaUploader:

    def __init__(self, token: str):
        self.token = token

    def new_folder(self, vk_id):
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources/'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        params = {'path': f'VK_id{vk_id}'}
        response = requests.put(url, headers=headers, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            print(f'\nКаталог VK_id{vk_id} уже существует')
        if response.status_code == 201:
            print(f'\nКаталог VK_id{vk_id} создан')
        return f'VK_id{vk_id}'

    def get_info_folder(self, folder, qty_f):
        print('Информация по загруженным файлам обрабатывается...')
        time.sleep(3)  # без отсрочки get_info_folder не успевает корректно отработать
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources/'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        params = {'path': f'/{folder}/', 'limit': 50}
        response = requests.get(url, headers=headers, params=params)
        output_list = []
        for photo in response.json()['_embedded']['items']:
            _dict = {'file_name': photo['name'], 'size': f"{round((photo['size'] / 1024), 1)} kb"}
            output_list.append(_dict)
        output_json = json.dumps(output_list, indent=4)
        print(f"Файлов в каталоге: {response.json()['_embedded']['total']},"
              f" в отчете(максимум): {response.json()['_embedded']['limit']}")
        return output_json

    def vk_upload(self, upload_dict, vk_id):
        folder = self.new_folder(vk_id)
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload/'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        count = 0
        for name, link in upload_dict.items():
            params = {'path': f'/{folder}/{name}.jpg', 'overwrite': True, 'url': link}
            response = requests.post(url, headers=headers, params=params)
            response.raise_for_status()
            count += 1
            if response.status_code == 202:
                print(f'Файл {count} из {len(upload_dict)} загружен')
        return self.get_info_folder(folder,len(upload_dict))
