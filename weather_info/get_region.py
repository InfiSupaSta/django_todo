import requests
import sys

yandex_url = 'https://yandex.ru/internet/'


def get_region_from_response(ya_url, default='Новосибирск'):
    try:
        return str(requests.get(ya_url).text.split('<div class="location-renderer__value">')[1].split('</div>')[0])
    except Exception as e:
        sys.stderr.write(f'Something unexpected occurs: {e}\nRegion set as default ({default})\n\n')
        return default


if __name__ == '__main__':
    print(get_region_from_response(yandex_url))
