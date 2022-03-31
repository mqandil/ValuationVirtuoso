def npv(wacc, fcf = []):
    npv = 0
    i = 0
    for value in range(len(fcf)):
        npv += (fcf[i] / ((1 + wacc)**(i+1)))
        i += 1
    return npv