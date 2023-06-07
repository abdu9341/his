def func(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]