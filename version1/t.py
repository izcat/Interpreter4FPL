Points = dict(X=[], Y=[])
print(Points)
print(Points['X'])

a = 100

def test1():
	# print(a)
	a = 1

def test2():
	a = 2

test2()
print(a)
test1()
print(a)