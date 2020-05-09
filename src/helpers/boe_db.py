"""Utilities for interacting with the BOE database."""

from typing import Dict


def insert_subscription_query(item: Dict) -> str:
    """Create insert query for boe_subscription table."""
    expected_keys = (
        'hash',
        'email',
        'search',
        'search_type'
    )
    compulsary_keys = expected_keys

    if not dict_is_valid(item, expected_keys, compulsary_keys):
        raise ValueError(f"Can't make query for item. {item}")

    query = "INSERT INTO boe_subscription" \
        "(hash, email, search, search_type)" \
        f"VALUES ('{item.get('hash')}','{item.get('email')}'," \
        f"'{item.get('search')}','{item.get('search_type')}');"

    return query


def insert_entry_label_query(item: Dict) -> str:
    """Create insert query for boe_diary_entry_label table."""
    expected_keys = ('name', 'entry')
    compulsary_keys = expected_keys

    if not dict_is_valid(item, expected_keys, compulsary_keys):
        raise ValueError(f"Can't make query for item. {item}")

    query = "INSERT INTO boe_diary_entry_label" \
        "(name, entry)" \
        f"VALUES ('{item.get('name')}','{item.get('entry')}');"

    return query


def insert_entry_reference_query(item: Dict) -> str:
    """Create insert query for boe_diary_entry_reference table."""
    expected_keys = (
        'source',
        'referenced',
        'type',
        'type_code',
        'text'
        )
    compulsary_keys = ('source', 'referenced')

    if not dict_is_valid(item, expected_keys, compulsary_keys):
        raise ValueError(f"Can't make query for item. {item}")

    query = "INSERT INTO boe_diary_entry_reference" \
        "(source, referenced, type, type_code, text)" \
        f"VALUES ('{item.get('source')}','{item.get('referenced')}'," \
        f"'{item.get('type_code')}','{item.get('type_code')}',"
        f"'{item.get('text')}');"

    return query


def insert_entry_query(item: Dict) -> str:
    """Create insert query for boe_diary_entry table."""
    expected_keys = (
        'id',
        'date',
        'fetch_date',
        'title',
        'section',
        'department',
        'epigraph',
        'pdf_url',
        'xml_url',
        'htm_url'
    )
    compulsary_keys = ('id', 'section')

    if not dict_is_valid(item, expected_keys, compulsary_keys):
        raise ValueError(f"Can't make query for item. {item}")

    query = "INSERT INTO boe_diary_entry" \
        "(id, date, title, section, department, epigraph, pdf_url, xml_url, htm_url)" \
        f"VALUES ('{item.get('id')}', '{item.get('date')}', '{item.get('fetch_date')}'," \
        f"'{item.get('title')}', '{item.get('section')}', '{item.get('department')}'," \
        f"'{item.get('epigraph')}', '{item.get('pdf_url')}', '{item.get('xml_url')}'," \
        f"'{item.get('htm_url')}');"

    return query


def dict_is_valid(item: Dict, expected_keys: tuple, compulsary_keys: tuple) -> bool:
    """Check the required keys an values to create an entry SQL query."""
    if not isinstance(item, dict):
        return False

    keys_are_present = all(map(
        lambda key: key in item.keys(),
        expected_keys))

    all_are_str = all(map(
        lambda value: isinstance(value, str),
        item.values()))

    compulsary_not_empty = all(map(
        lambda key: len(str(item.get(key))) > 0,
        compulsary_keys))

    return keys_are_present and all_are_str and compulsary_not_empty

