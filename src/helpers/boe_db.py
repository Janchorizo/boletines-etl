def boe_diary_entry_query(item):
    return f"""
        INSERT INTO boe_diary_entry
        (id, date, title, section, department, epigraph, pdf_url, xml_url, htm_url, economic_impact)
        VALUES ('{item.get('id')}', '{item.get('date')}', '{item.get('title')}', 
                '{item.get('section')}', '{item.get('department')}', '{item.get('epigraph')}',
                '{item.get('pdf_url')}', '{item.get('xml_url')}', '{item.get('htm_url')}',
				'{item.get('economic_impact')}');
    """

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
		'economic_impact'
	)

	keys_are_present = all(map(lambda key: key in item.keys(), expected_keys))
	return keys_are_present
