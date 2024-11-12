from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from .utils import rand, formatInputData
import pandas as pd
import os

def index(request):
    if request.method == "POST":
        root = os.path.dirname(os.path.abspath(__file__))

        # Get input data and format it
        fixedVar1 = formatInputData(request.POST["Fixed Var 1"])
        fixedVar2 = formatInputData(request.POST["Fixed Var 2"])
        var1 = formatInputData(request.POST["Var 1"])
        var2 = formatInputData(request.POST["Var 2"])
        var3 = formatInputData(request.POST["Var 3"])

        # Check for invalid range
        if var2[0] <= var1[0] or var3[0] <= var2[0]:
            return render(request, 'core/result.html')

        # Dictionary to store combinations, with each 'fxd1' having its own list
        combinations_dict = {}
        max_length = 0  # Track max length of combinations to pad columns later

        for i in fixedVar1:
            fxd1_combinations = []  # List to store combinations for this `fxd1`
            for j in fixedVar2:
                if i >= j:
                    continue
                combinations = rand(i, j, var1, var2, var3)
                
                # Flatten and store all combinations for the current `fxd1`
                for value in combinations.values():
                    fxd1_combinations.extend(value)
            
            combinations_dict[f"fxd1_{i}"] = fxd1_combinations
            max_length = max(max_length, len(fxd1_combinations))

        # Pad each list in `combinations_dict` to have the same length
        for key, value in combinations_dict.items():
            combinations_dict[key] = value + [None] * (max_length - len(value))

        # Convert dictionary to DataFrame with each `fxd1` as a separate column
        df = pd.DataFrame(combinations_dict)
        df.to_csv(f"{root}/static/core/combinations.csv", index=False)

        return redirect('result')

    context = {}
    return render(request, 'core/index.html', context)

def result(request):
    root = os.path.dirname(os.path.abspath(__file__))
    file_location = f"{root}/static/core/combinations.csv"
    return serve(request, os.path.basename(file_location), os.path.dirname(file_location))
