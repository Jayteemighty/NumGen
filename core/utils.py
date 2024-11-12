def rand(fxd1, fxd2, var1, var2, var3):
    res = {i: [] for i in var1}
    for i in var1:
        for j in var2:
            for k in var3:
                if fxd2 < i and i < j and j < k:
                    res[i].append(f"{fxd1}{fxd2}{i}{j}{k}")
    return res

def formatInputData(var):
    temp = var.split(",")
    var = list(map(int, temp))
    return var
