"""
>>> from data_collection import get_MosPark_response 
Func allows to send requests for geojson data collections from https://data.mos.ru/. API key is required.

>>> from data_collection import get_MosReg_response 
Func allows to save a specified dataset with Moscow geometry data. 

>>> from data_collection import save_to_geojson
Func allows to save response data in geojson file. 
"""

from gather_data import get_MosPark_response, get_MosReg_response, save_to_geojson
from runpackage import runpackage