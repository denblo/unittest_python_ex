def count_e(digits):

    fract = 0
    n = 2
    mul = 10 ** digits

    fact = 1

    droub = 0
    while True:
        fact *= n
        n += 1
        droub += (mul % fact) / fact
        d = mul // fact

        if d == 0:
            break

        fract += d

    fract += int(droub)

    return "2.%s" % str(fract)[:digits]
