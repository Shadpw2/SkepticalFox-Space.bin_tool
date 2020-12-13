""" Space Assembler """

from struct import unpack, pack
from versioning import get_sections



def space_assembly(bin_path, sections, wotver, unpver):
	all_data = b''
	sec_num = len(sections)
	offset = (sec_num+1)*24
	new_sections = []

	bwtb = pack(
		'4s5I',
		b'BWTB',
		1,
		offset,
		0,
		0,
		sec_num
	)

	ordered_secs = get_sections(wotver)
	for cls in ordered_secs:
		if cls.header not in sections:
			continue
		new_sections.append({
			'header': cls.header.encode('ascii'),
			'int1': cls.int1,
			'data': sections.pop(cls.header).to_bin()
		})

	assert not sections

	for item in new_sections:
		data = item['data']
		all_data += data
		bwtb += pack(
			'4s5I',
			item['header'],
			item['int1'],
			offset,
			0,
			len(data),
			0
		)
		offset += len(data)

	with open(bin_path, 'wb') as out:
		out.write(bwtb)
		out.write(all_data)
		out.write(b'\0SkepticalFox utility v.%s' % unpver.encode('ascii'))
