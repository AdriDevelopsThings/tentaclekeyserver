def add_fingerprint_spaces(fingerprint):
    fingerprint = fingerprint.replace(" ", "")
    assert len(fingerprint) == 40
    o = ""
    b = 0
    for i in fingerprint:
        b += 1
        if b == 5:
            o += " "
            b = 1
        o += i
    return o