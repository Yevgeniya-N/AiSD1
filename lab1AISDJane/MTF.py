def MTF(data):
    alphabet = [_ for _ in range(256)]
    new_d = []
    for byte in data:
        index = alphabet.index(byte)
        new_d.append(index)
        alphabet = [alphabet[index]] + alphabet[:index] + alphabet[index + 1:]
    return bytes(new_d)


def MTF_decode(c_data):
    alphabet = [_ for _ in range(256)]
    original = []
    for i in c_data:
        byte = alphabet[i]
        original.append(byte)
        alphabet = [alphabet[i]] + alphabet[:i] + alphabet[i + 1:]
    return bytes(original) 