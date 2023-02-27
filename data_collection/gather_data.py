import os 

import numpy as np
import geojson
import requests

from api_setup import read_MosAPIKey


def get_MosPark_response(dataset_id:int, API_KEY_filepath: str) -> requests.Response:
    """Func generates request url and gets response 
    from the Moscow govenrment's open data web-portal. 

    Args:
        dataset_id (int): dataset id from the passport of the data collection. 
        API_KEY_filepath (str): path (abs or rel) to the file with the API Key,
        required to send requests to the web-portal.

    Raises:
        requests.ConnectionError: raises in case if the connection was broken due to any reason.

    Returns:
        requests.Response: response data. 
    """
    MOS_API_KEY = read_MosAPIKey(filepath=API_KEY_filepath)
    request_url = 'https://apidata.mos.ru/v1/datasets/%s/features?api_key=%s' % (str(dataset_id), MOS_API_KEY)
    response = requests.get(request_url)
    if response.status_code == 200:
        return response
    else:
        raise requests.ConnectionError
    

def get_MosReg_response() -> requests.Response:
    """Func gets the geojson response from the github. 
    The geojson contains the geometry of Moscow areas. 

    Raises:
        requests.ConnectionError: raises in case if the connection was broken due to any reason.

    Returns:
        requests.Response: response data. 
    """
    URL = 'https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/moscow.geojson'
    response = requests.get(URL)
    if response.status_code == 200:
        return response
    else:
        raise requests.ConnectionError
    

def save_to_geojson(response: requests.Response, filename: str) -> str:
    """ Func dumps reponse data to geojson. 
    Return nothing, as it saves data into file.

    Args:
        response (requests.Response): reponse, containing geojson data. 

    Returns:
        str: path to the file with the data. 
    """
    resp_data = response.json()
    
    filepath = os.path.abspath(f'data/{filename}.geojson')
    with open(filepath, 'w') as parkings_json:
        geojson.dump(obj=resp_data, fp=parkings_json, default=np.nan)
        
    return filepath