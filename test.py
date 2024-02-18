l = ['hello', 'world', 'everyone']
new = []
for i in l:
	new.append(i[0])
print(new)

b = [i[0] for i in l]
print(b)
