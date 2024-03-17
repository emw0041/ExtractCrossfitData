def height(height_str: str) -> float:
	cm_to_in = 0.393701
	height_str = height_str.split()
	if height_str[1].lower() == 'cm':
		height = int(height_str[0])*cm_to_in
	elif height_str[1].lower() == 'in':
		height = int(height_str[0])
	else:
		raise Exception('Error: height units are not cm or in')
	return round(height)

def weight(weight_str: str) -> float:
	kg_to_lb = 2.20462
	weight_str = weight_str.split()
	if weight_str[1].lower() == 'kg':
		weight = int(weight_str[0])*kg_to_lb
	elif weight_str[1].lower() == 'lb':
		weight = int(weight_str[0])
	else:
		raise Exception('Error: weight units are not cm or in')
	return round(weight)
