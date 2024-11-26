import src.ski as ski


##########
# PART 1 #
##########
# TASK: Implement the below function `eval`.

def eval(e: ski.Expr) -> ski.Expr:
    # BEGIN_YOUR_CODE
    prev_rewrite_res = "None"   # store the previous result
    #* Keep rewriting till convergence.
    while str(e) != prev_rewrite_res:
        prev_rewrite_res = str(e)
        e = rewrite(e)
    return e

def rewrite(e: ski.Expr) -> ski.Expr:
    if not isinstance(e, ski.App):
        # curr_e is not an App; must be one of S | K | I | x
        # We only rewrite Apps.
        return e;
    # print("Curr expr ", str(e))
    
    #* Recursively rewrite subexpressions.
    e.e1 = rewrite(e=e.e1)
    e.e2 = rewrite(e=e.e2)

    if is_app_i(app=e):
        rewritten_expr = e.e2
    elif is_app_k(app=e):
        rewritten_expr = e.e1.e2
    
    elif is_app_s(app=e):
        # S e1 e2 e3 = (((S e1) e2) e3)
        rewritten_expr = ski.App(
            ski.App(e.e1.e1.e2, e.e2),
            ski.App(e.e1.e2, e.e2)
        )
    
    else:
        rewritten_expr = e

    return rewritten_expr
    # END_YOUR_CODE

def is_app_i(app: ski.App) -> bool:
    """
    APP(I, e)
    """
    return isinstance(app.e1, ski.I)

def is_app_k(app: ski.App) -> bool:
    """
    APP(APP(K, e1), e2) or APP(K, APP(e1, e2))
    """
    cond = isinstance(app.e1, ski.App) and isinstance(app.e1.e1, ski.K)
    return cond

def is_app_s(app: ski.App) -> bool:
    """
    """
    cond = isinstance(app.e1, ski.App) and isinstance(app.e1.e1, ski.App) and isinstance(app.e1.e1.e1, ski.S)
    return cond
