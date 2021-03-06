import requests
import pandas as pd
from pymongo import MongoClient
from bs4 import BeautifulSoup

def select_soup(soup, css_selectors): 
    '''
    Input: Beautiful Soup parsedHTML, List of Strings 
    Output: Dictionary

    For the given css_selectors, return a list for all of the inputs
    matching those results. 
    '''
    
    css_selectors = mk_list(css_selectors)
    
    contents = {selector: soup.select(selector) \
                for selector in css_selectors}
    return contents

def mk_list(potential_lst): 
    '''
    Input: Varied
    Output: List

    If the inputted type is not a list, then throw it into a list. 
    '''

    if isinstance(potential_lst, list): 
        return potential_lst
    else: 
        return [potential_lst]

def grab_contents_key(contents, key): 
    '''
    Input: Dictionary, String
    Output: Dictionary

    For the inputted contents, grab the desired key from each soup item 
    in the values lists of the dictionary.
    '''
    if key == 'text': 
        contents_dct = {k: [html.text.encode('ascii', 'xmlcharrefreplace') \
                for html in v] for k, v in contents.iteritems()}
    elif key == 'a': 
        contents_dct = {k: [tag.find(key) for tag in v if tag is not None] \
                for k, v in contents.iteritems()}
    elif key == 'href': 
        contents_dct = {k: [tag.get(key) for tag in v if tag is not None] \
                for k, v in contents.iteritems()}

    return contents_dct

def output_data_to_file(lst, filepath, file_format="csv", replace_nulls=None):
    '''
    Input: List of dictionaries, String, String, Object
    Output: Saved file

    Save the list of dictionaries to the filepath location, 
    using the inputted format (default is csv). Fill nulls with 
    the passed in argument if specified.
    '''

    df = pd.DataFrame(lst)
    if replace_nulls is not None: 
        df = df.fillna(replace_nulls)

    if file_format=="json": 
        df.to_json(filepath)
    else: 
        df.to_csv(filepath, index=False)

