"""Utility methods for processing BOE diary entries."""

from typing import Dict, Tuple
import lxml
import functools

from . import helpers
from . import boe


def get_labels_from_tree(tree: lxml.etree._Element) -> Tuple:
    """Extract labels of a diary entry's analysis section."""
    tree_search = helpers.use_tree_for_search(tree)
    topics = tree_search(boe.EntryXpath.topics)
    alerts = tree_search(boe.EntryXpath.alerts)

    labels = helpers.pipe(topics + alerts,
                          functools.partial(map, lambda x: x.xpath('text()')),
                          functools.partial(map, ''.join),
                          set,
                          tuple)
    return labels

def get_type_from_tree(tree: lxml.etree._Element) -> Tuple:
    """Extract the type of a diary entry's analysis section."""
    tree_search = helpers.use_tree_for_search(tree)
    entry_type = tree_search(boe.EntryXpath.entry_range)[0]
    entry_type_code = entry_type.get(boe.EntryAttribute.range_code)

    return (entry_type.text, entry_type_code)


def get_reference_details(node: lxml.etree._Element) -> Dict:
    """Extract details of a diary entry reference."""
    tree_search = helpers.use_tree_for_search(node)
    reference_type_search = tree_search(boe.EntryXpath.reference_type)
    reference_text_search = tree_search(boe.EntryXpath.reference_text)

    if len(reference_type_search) == 0 or len(reference_text_search) == 0:
        return {}

    reference_type = reference_type_search = reference_type_search[0]
    reference_text = reference_text_search = reference_text_search[0]

    details = {
        'referenced': node.get(boe.EntryAttribute.reference_entry_id),
        'type': reference_type.text,
        'type_code': reference_type.get(boe.EntryAttribute.reference_type_code),
        'text': reference_text.text
    }
    return details


def get_references_from_tree(tree: lxml.etree._Element) -> Tuple:
    """Extract details and type of the references of a diary entry."""
    tree_search = helpers.use_tree_for_search(tree)
    prev = tree_search(boe.EntryXpath.previous)
    post = tree_search(boe.EntryXpath.posterior)

    prev_references = helpers.pipe(
        prev,
        functools.partial(map, lambda x: {**get_reference_details(x), **{'category': 'previous'}}),
        functools.partial(filter, lambda x: 'referenced' in x))

    post_references = helpers.pipe(
        post,
        functools.partial(map, lambda x: {**get_reference_details(x), **{'category': 'posterior'}}),
        functools.partial(filter, lambda x: 'referenced' in x))

    return (*prev_references, *post_references)
