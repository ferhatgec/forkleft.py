import forkleft
data = ''
tok = forkleft.Forkleft.Tokenize()
with open('test.forkleft', 'r') as file:
    for line in file:
        data += line

    tok.init(data)

    with open('test.html', 'w') as outfile:
        outfile.write(tok.get())
