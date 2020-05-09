from typing import Dict

def boe_diary_entry_query(item: Dict) -> str:
    '''Create SQL query for the insertion a BOE diary entry.'''

    if not boe_diary_entry_is_valid(item): raise ValueError("Can't make query for item.")
    
    query = "INSERT INTO boe_diary_entry" \
        "(id, date, title, section, department, epigraph, pdf_url, xml_url, htm_url)" \
        f"VALUES ('{item.get('id')}', '{item.get('date')}', '{item.get('title')}'," \
        f"        '{item.get('section')}', '{item.get('department')}', '{item.get('epigraph')}'," \
        f"        '{item.get('pdf_url')}', '{item.get('xml_url')}', '{item.get('htm_url')}');"
    return query

def boe_diary_entry_is_valid(item: Dict) -> bool:
    '''Check wether a dictionary has the required keys an values to create an SQL query.'''

    if type(item) is not dict: return False

    expected_keys = (
        'id',
        'date',
        'title',
        'section',
        'department',
        'epigraph',
        'pdf_url',
        'xml_url',
        'htm_url'
    )
    compulsary_keys = ('id', 'section')

    keys_are_present = all(map(lambda key: key in item.keys(), expected_keys))
    compulsary_not_empty = all(map(lambda key: item.get(key) != '', compulsary_keys))

    return keys_are_present and compulsary_not_empty
