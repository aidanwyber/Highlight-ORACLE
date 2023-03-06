
id_counter_file_name = 'id_counter.oracle'

def get_id():
	with open(id_counter_file_name, mode='r') as f:
		id_c = int(f.read())
		f.close()
	return id_c
		
	
def set_id(id_c):
	with open(id_counter_file_name, mode='w') as f:
		f.write(str(id_c))
		f.close()
