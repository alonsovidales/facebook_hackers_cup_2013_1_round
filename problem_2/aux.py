origin = list('?feedbfcaabfeab?b???fddcfbfbdcaeeecf')
chars = list('?b?ceffedfba?bdfffadbcefa?edeebaddbf')

print chars
for charOrig in origin:
    print "Removing %s" % (charOrig)
    try:
        chars.remove(charOrig)
    except:
        print "NotFound: %s" % (charOrig)
