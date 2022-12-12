def get_request_field_index(request, field):
    idx = request.index(f"\r\n{field}:".encode())

    # Calculate the high index
    high_idx = idx + 2
    while True:
        try:
            if request[high_idx] == ord("\r"):
                if request[high_idx + 1] == ord("\n"):
                    break
            else:
                high_idx += 1
        except IndexError:
            high_idx = None
            break

    return idx + 2, high_idx


def replace_request_field(request, field, new_val):
    idx, high_idx = get_request_field_index(request, field)
    return request[:idx] + f"\r\n{field}: {new_val}" + request[high_idx:]
