def some_func(*args, **kwargs):
    print(args)
    for i in args:
        print(i)
    print(kwargs)
    print(kwargs.get('a'))



print(some_func(*[2, 3, 4, 5, 6,], a=1, b=2, l=3))


list_ = [1 ,2 ,3 ,4 ,5  ,6 ,7]
for i in list_:
    print(i, end=' ')

print(*list_)