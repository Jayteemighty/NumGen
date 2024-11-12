from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from .utils import rand, formatInputData
import pandas as pd
import os

def index(request):
    if request.method == "POST":
        # File root
        root = os.path.dirname(os.path.abspath(__file__))

        fixedVar1 = request.POST["Fixed Var 1"]
        fixedVar1 = formatInputData(fixedVar1)

        fixedVar2 = request.POST["Fixed Var 2"]
        fixedVar2 = formatInputData(fixedVar2)

        var1 = request.POST["Var 1"]
        var1 = formatInputData(var1)

        var2 = request.POST["Var 2"]
        var2 = formatInputData(var2)

        var3 = request.POST["Var 3"]
        var3 = formatInputData(var3)

        if var2[0] <= var1[0] or var3[0] <= var2[0]:
            return render(request, 'core/result.html')

        all_combinations = {i: [] for i in var1}
        for i in fixedVar1:
            for j in fixedVar2:
                if i >= j:
                    continue
                combinations = rand(i, j, var1, var2, var3)
                for key, value in combinations.items():
                    all_combinations[key].extend(value)
        
        # Convert dictionary to DataFrame ensuring each list is a column
        df = pd.DataFrame({k: pd.Series(v) for k, v in all_combinations.items()})
        df.to_csv(f"{root}/static/core/combinations.csv", index=False)

        return redirect('result')

    context = {}
    return render(request, 'core/index.html', context)

def result(request):
    root = os.path.dirname(os.path.abspath(__file__))
    file_location = f"{root}/static/core/combinations.csv"
    return serve(request, os.path.basename(file_location), os.path.dirname(file_location))
