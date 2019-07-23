import requests
from main.models import CyclparkPoint, ApiInfo
from cyclpark4.settings import MOS_API_DATASET_NUMBER, MOS_API_KEY, MOS_API_URL


# https://apidata.mos.ru/
# v1/datasets/916/features?versionNumber=5&releaseNumber=18&api_key=32c5a393e9cd6da884d581cbc85dba48
def download_points(version, release):
    url = f'{MOS_API_URL}v1/datasets/{MOS_API_DATASET_NUMBER}/' \
        f'features?versionNumber={version}&releaseNumber={release}&api_key={MOS_API_KEY}'
    data = requests.get(url)
    if '200' not in data.text:
        raise Exception(f"Don't get response for version: {version}, release: {release}\n"
                        f"url: {url}")
    else:
        data = data.json()

    data_to_write = {}

    for info in data['features']:
        data_to_write['global_id'] = info['properties']['Attributes']['global_id']
        data_to_write['name'] = info['properties']['Attributes']['Name']
        data_to_write['admarea'] = info['properties']['Attributes']['AdmArea']
        data_to_write['district'] = info['properties']['Attributes']['District']
        data_to_write['address'] = info['properties']['Attributes']['Address']
        data_to_write['capacity'] = info['properties']['Attributes']['Capacity']
        data_to_write['departamentalaffiliation'] = info['properties']['Attributes']['DepartamentalAffiliation']
        data_to_write['objectoperorgname'] = info['properties']['Attributes']['ObjectOperOrgName']
        data_to_write['longitude_WGS84'] = info['geometry']['coordinates'][0]
        data_to_write['latitude_WGS84'] = info['geometry']['coordinates'][1]

        CyclparkPoint.objects.create_object(data=data_to_write)


# https://apidata.mos.ru/v1/classifiers/916/version?api_key=32c5a393e9cd6da884d581cbc85dba48
def check_update():
    url = f'{MOS_API_URL}v1/classifiers/916/version?api_key={MOS_API_KEY}'
    data = requests.get(url).json()
    now_api_info = ApiInfo.objects.all()[0]

    if data['versionNumber'] == now_api_info.versionNumber and data['releaseNumber'] == now_api_info.releaseNumber:
        return {}
    else:
        return data


def update_points():
    data = check_update()
    if data:
        print('updating...')
        version, release = data['versionNumber'], data['releaseNumber']
        download_points(version, release)
        now_api_info = ApiInfo.objects.all()[0]
        now_api_info.versionNumber = data['versionNumber']
        now_api_info.releaseNumber = data['releaseNumber']
        now_api_info.save()

