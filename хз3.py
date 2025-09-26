def checker(var_1):
    if type(var_1) != str:
        raise TypeError(f"Sorry, we can't work with type {type(var_1)} we need str")
    else:
        return var_1

first_var = 10
checker(first_var)