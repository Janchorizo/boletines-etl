from typing import Callable, Set, Generator, Iterable, Dict, List

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

