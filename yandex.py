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
            print(f'Folder VK_id{vk_id} already exists')
        if response.status_code == 201:
            print(f'Folder VK_id{vk_id} created')
        return f'VK_id{vk_id}'

    def get_info_folder(self, folder):
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources/'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        params = {'path': f'/{folder}/'}
        response = requests.get(url, headers=headers, params=params)
        output_list = []
        for photo in response.json()['_embedded']['items']:
            _dict = {'file_name': photo['name'], 'size': f"{round((photo['size'] / 1024), 1)} kb"}
            output_list.append(_dict)
        output_json = json.dumps(output_list, indent=4)
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
                print(f'File {count} of {len(upload_dict)} uploaded')
        time.sleep(3)  # без отсрочки get_info_folder не успевает корректно отработать
        return self.get_info_folder(folder)
