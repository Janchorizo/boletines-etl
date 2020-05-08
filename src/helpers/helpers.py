import functools
import collections
from typing import Callable, Any
import httplib2
from lxml import etree as et

Response = collections.namedtuple('Response', 'headers content')

def pipe(initial_value: Any, *args:Callable[[Any], Any]) -> Any:
    '''Chaining functions in order of execution.'''
    
    chain_function = lambda prev_result, func: func(prev_result)
    
    return functools.reduce(chain_function, args, initial_value)

def fetch_page(url: str, max_tries=3)->Response:
    '''Try to fetch a given url up to max_tries times.'''
    
    h = httplib2.Http(".cache")
    
    for _ in range(max_tries):
        response = Response(*h.request(url, "GET"))
        if response.headers.get('status') == '200':
            break
    
    return response

def print_reponse_content(response: Response)->None:
    print(response.content.decode('utf-8'))
    
def tree_from_response(response: Response)->et._Element:
    '''Create lxml.etree._Element from an XML document content.'''
    
    return et.fromstring(response.content)

def use_tree_for_search(tree)->Callable:
    '''Return a function xpath:str->List for performing 
    xpath-based search over the provided lxml tree.'''
    
    namespaces = dict(xmlns="http://www.w3.org/1999/xhtml")
    return lambda xpath: tree.xpath(xpath, namespaces=namespaces)

def use_xpath_for_search(xpath)->Callable:
    '''Return a function tree:str->List for performing 
    the provided xpath-based search over the tree.'''
    
    namespaces = dict(xmlns="http://www.w3.org/1999/xhtml")
    return lambda tree: tree.xpath(xpath, namespaces=namespaces)
