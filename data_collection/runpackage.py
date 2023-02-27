import os
import requests

from api_setup import read_MosAPIKey
from gather_data import get_MosPark_response, get_MosReg_response, save_to_geojson


def runpackage():
    mos_APIKey = os.path.abspath('data_collection/MOS_API_KEY.txt') 
    
    try:
        print('Sending request for Moscow street parkings data')
        mospark_response = get_MosPark_response(dataset_id=623, API_KEY_filepath=mos_APIKey)
        print(f'{mospark_response.status_code} - successful')
        
        mospark_filepath = save_to_geojson(response=mospark_response, filename='moscow_parkings')
        print(f'Parkings data was saved to {mospark_filepath}')
    except requests.ConnectionError:
        print('The connection was not established. Try again')
        
    try:
        print('Sending request for Moscow geometry data')
        mosreg_response = get_MosReg_response()
        print(f'{mosreg_response.status_code} - successful')
        
        mosreg_filepath = save_to_geojson(response=mosreg_response, filename='moscow_regions')
        print(f'Regions data was saved to {mosreg_filepath}')
    except requests.ConnectionError:
        print('The connection was not established. Try again')
    
    print('Completed')


if __name__ == '__main__':
    runpackage()