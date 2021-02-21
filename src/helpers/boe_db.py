def boe_diary_entry_query(item):
    query = f"""
        INSERT INTO boe_diary_entry
        (id, date, title, section, department, epigraph, pdf_url, xml_url, htm_url, economic_impact, type, type_desc)
        VALUES (
            '{item.get('id')}',
            '{item.get('date')}',
            '{item.get('title')}',
            '{item.get('section')}',
            '{item.get('department')}',
            '{item.get('epigraph')}',
            '{item.get('pdf_url')}',
            '{item.get('xml_url')}',
            '{item.get('htm_url')}',
            '{item.get('economic_impact')}',
            '{item.get('type')}',
            '{item.get('type_desc')}');
    """
    return query

def boe_diary_entry_is_valid(item):
	expected_keys = (
		'id', 
		'date', 
		'title', 
		'section', 
		'department', 
		'epigraph', 
		'pdf_url', 
		'xml_url', 
		'htm_url',
		'economic_impact',
		'type',
		'type_desc'
	)

	keys_are_present = all(map(lambda key: key in item.keys(), expected_keys))
	return keys_are_present
