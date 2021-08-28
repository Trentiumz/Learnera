def get_id(index):
  hash = 2**55+3
  return ((588829 * index) % hash + 299384) % hash

def next_id(model_class, objects_dict):
  id = get_id(model_class.new_index)
  while id in objects_dict:
    model_class.new_index += 1
    id = get_id(model_class.new_index)
  model_class.new_index += 1
  return id