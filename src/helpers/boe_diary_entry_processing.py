from typing import Callable, Set, Generator, Iterable, Dict, List
import locale
import re
import functools

from . import helpers
from . import boe

def get_labels_from_tree(tree):
    tree_search = helpers.use_tree_for_search(tree)
    topics = tree_search(boe.EntryXpath.topics)
    alerts = tree_search(boe.EntryXpath.alerts)
    
    labels = helpers.pipe(topics + alerts,
        functools.partial(map, lambda x: x.xpath('text()')),
        functools.partial(map, ''.join),
        set,
        tuple)
    return labels

def get_reference_details(node):
    tree_search = helpers.use_tree_for_search(node)
    reference_type = tree_search(boe.EntryXpath.reference_type)[0]
    reference_text = tree_search(boe.EntryXpath.reference_text)[0]

    details = {
        'referenced': node.get(boe.EntryAttribute.reference_entry_id),
        'type': reference_type.text,
        'type_code': reference_type.get(boe.EntryAttribute.reference_type_code),
        'text': reference_text.text
    }
    return details

def get_references_from_tree(tree):
    tree_search = helpers.use_tree_for_search(tree)
    prev = tree_search(boe.EntryXpath.previous)
    post = tree_search(boe.EntryXpath.posterior)
    
    prev_references = map(
            lambda x: {**get_reference_details(x), **{'category': 'previous'}}, 
            prev)
    post_references = map(
            lambda x: {**get_reference_details(x), **{'category': 'posterior'}}, 
            post)
    
    return [*prev_references, *post_references]

_supported_modalities = (boe.code_to_modality_name['F'], boe.code_to_modality_name['L'])
_money_regex = re.compile('[0-9]+\.?[0-9]*\,?[0-9]* euros')
_amount_regex = re.compile('[0-9]+\.?[0-9]*\,?[0-9]*')
_preceding_regex = re.compile('(oferta seleccionada)|(valor estimado)', re.IGNORECASE)
locale.setlocale(locale.LC_ALL,"")
def get_cost(tree):
    '''
    All evaluated costs appear in a `<dd/>` element after a `<dt/>` with a 
    _"valor estimado"_ or _"oferta seleccionada"_ text in it.
    See notebook 'boe_diary_entry_processing' for further information.
    '''
    search = helpers.use_tree_for_search(tree)
    cost = 0
    
    modality = search(boe.EntryXpath.modality)
    if len(modality) != 1 or modality[0].text not in _supported_modalities:
        return cost
    
    for dd in search('//dt/following-sibling::dd'):
        ammounts = _money_regex.findall(dd.text)
        preceding_texts = _preceding_regex.findall(dd.getprevious().text)

        if len(ammounts) == 1 and len(preceding_texts) > 0:
            cost = locale.atof(_amount_regex.match(dd.text)[0])
            break
    
    return cost
