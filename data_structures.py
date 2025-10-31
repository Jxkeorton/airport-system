# ------------------------------------------
# Data Structures & Algorithms: Merge Sort applied 
# ------------------------------------------

def merge_sort(data, key, reverse=False):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid], key, reverse)
    right = merge_sort(data[mid:], key, reverse)

    return merge(left, right, key, reverse)


def merge(left, right, key, reverse):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if reverse:
            condition = left[i][key] > right[j][key]
        else:
            condition = left[i][key] < right[j][key]

        if condition:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
