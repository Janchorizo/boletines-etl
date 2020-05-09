"""Utility methods for interacting with XML documents and HTTP apis."""

import functools
import collections
from typing import Callable, Any
import httplib2
from lxml import etree as et


Response = collections.namedtuple('Response', 'headers content')


def pipe(initial_value: Any = None, *args: Callable[[Any], Any]) -> Any:
    """Chain an initial value through a series functions."""
    # chain_function = lambda prev_result, func: func(prev_result)
    def chain_function(prev_result: Any, func: Callable):
        return func(prev_result)

    return functools.reduce(chain_function, args, initial_value)


def fetch_page(url: str, max_tries=3) -> Response:
    """Try to fetch a given url up to max_tries times."""
    if url is None:
        raise ValueError("Can't fetch a None url.")
    if max_tries <= 0:
        raise ValueError("Can't fetch less than one time.")

    h = httplib2.Http(".cache")
    for _ in range(max_tries):
        response = Response(*h.request(url, "GET"))
        if response.headers.get('status') == '200':
            break

    return response


def print_reponse_content(response: Response) -> None:
    """Print to stdout the content of an HTTP response."""
    if response is None:
        return None
    if type(response) is not Response:
        raise TypeError()

    print(response.content.decode('utf-8'))


def tree_from_response(response: Response) -> et._Element:
    """Create lxml.etree._Element from an XML document content."""
    if response is None:
        return None
    if type(response) is not Response:
        raise TypeError()

    return et.fromstring(response.content)


def use_tree_for_search(tree: et._Element) -> Callable:
    """Return a function xpath:str -> List for xpath searches in the tree."""
    if tree is None:
        return None
    if type(tree) is not et._Element:
        raise TypeError()

    namespaces = dict(xmlns="http://www.w3.org/1999/xhtml")
    return lambda xpath: tree.xpath(xpath, namespaces=namespaces)


def use_xpath_for_search(xpath: str) -> Callable:
    """Return a function tree:str -> List for performing the xpath search."""
    if xpath is None:
        return None
    if type(xpath) is not str:
        raise TypeError()

    namespaces = dict(xmlns="http://www.w3.org/1999/xhtml")
    return lambda tree: tree.xpath(xpath, namespaces=namespaces)
