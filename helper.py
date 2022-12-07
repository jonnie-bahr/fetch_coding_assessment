# Convert request into tuple of values for SQL call
def convert_request(request):
    return tuple(vars(request).values())


# Method to add all values with the same key together
def spend_points_response(track_record):
    result = {}
    for d in track_record:
        for k in d.keys():
            result[k] = result.get(k, 0) + d[k]
    return result