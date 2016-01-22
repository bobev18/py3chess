l = list(range(100))

def filt(lst, condition):
    for i in lst:
        if i%2 == 0:
            condition(i)

def test_cond(x):
    if x%3==0: print(x)
    if x>51: break

filt(l, test_cond)
