def count_e(digits):
    fract = 0
    n = 2
    mul = 10 ** digits
    fact = 1
    while True:
        fact *= n
        n += 1
        d = ( 10 * mul // fact + 5 ) // 10
        fract += d
        if d == 0:
            break
    return "2.%s" % str(fract)[:digits]
