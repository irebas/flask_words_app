def create_unique_and_sorted_list(list):
    temp_set = set()
    for element in list:
        element = element.upper()
        temp_set.add(element)

    list_new = sorted(temp_set)
    return list_new

