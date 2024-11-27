# Part 1: Implement SKI Interpreter

SKI Expr definition:

$$
e\ :=\ S\ |\ K\ |\ I\ |\ x\ |\ e\ e
$$

Property:

$$
e\ \rightarrow^* e'\quad \text{which cannot be rewritten further}
$$

`src/ski.py` defines the expressions in SKI.

> - In our Python framework, the combinators S, K, and I are represented as `S()`, `K()`, and `I()`, a variable x as `Var("x")`, and an application e1 e2 as `App(e1,e2)`
>
> - To check whether an expression e is, for example, the K combinator, you can use `isinstance(e, K)` which returns True if e is indeed the K combinator, and False otherwise.
>
> - cd to `f19hw01`, run `sh testski.sh` to test the output



## Rules & Definitions

A valid expression conforms to [BNF](http://en.wikipedia.org/wiki/Backus–Naur_Form) and can be defined recursively.

Take an example to show the usage of  the definition of SKI:

```py
# e = (((S x) y) z)
> print(e)
(((S x) y) z)

> print(e.e1)
((S x) y)

> print(e.e2)
z

> print(e.e1.e1)
(S x)

>print(e.e1.e1.e1)
S
```



## Implementation

Simple rule: rewrite until cannot rewrite, i.e. previous expr is the same as current expr:

```python
def eval(e: ski.Expr) -> ski.Expr:
    # BEGIN_YOUR_CODE
    prev_rewrite_res = "None"   # store the previous result
    #* Keep rewriting till convergence.
    while str(e) != prev_rewrite_res:
        prev_rewrite_res = str(e)
        e = rewrite(e)
    return e
```

### Rewrite

We only rewrite applications (expressions of the form S x y z | K x y | I x), treating variables as terminals.

We then recursively rewrite the two components of the expression (e.e1 and e.e2), as every expression is composed of two subexpressions. For example, (S x y z) is represented as (((S x) y) z).

>   Method of listing cases: $S\ K\ I$
>
>   If $I$, then `r_expr = e.e2` (for `I x = x` and `I` is `e.e1`);
>
>   If $K$, then `r_expr = e.e1.e2` (for `(K x) y` and `(K x)` is `e.e1`)
>
>   if $S$, then the rewritten expression is: Apply `e.e1.e1.e2` and `e.e1.e1` to `e.e2`



### Conditions

We NEED to varify the specific combinator, and corresponding to rewritten rules, i.e. how we rewrite, how we check (On associativity aspect).

Here we name the expression taken in as `app`, indicating that it is an expression which follows the Application rule.

-   `I x` is quite obvious: `isinstance(app.e1, ski.I)`
-   `K x y` equivalent to `(K x) y` (We followed this associativity when rewriting) , so just check the `e.e1 is ski.App` and `e.e1.e1 is ski.K`
-   `S x y z` evaluated as `(((S x) y) z) `, just like description above

Drawing a tree diagram may help:

```python
"""
App           App            App
| \           |  \           |  \
I  x          App \          App \
              | \  y         |  \ \
              K  x           App \ z
                             | \  y
                             S  x
"""
```

# Part2: Programming in SKI calculus

Implement operations with SKI combinator: `or`, `not`, `is_odd`. Notice that True and False are already implemented as `tt` and `ff` , all of them are higer-order functions.

Example: 

```SKI
or tt ff x y = x
and tt ff x y = y
not ff x y = x
is_odd _3 x y = x
```

Unlike traditional programming, which often requires returning specific variables, this problem primarily focuses on achieving correct behavior without strictly adhering to the given definition. In other words, an expression is considered correct if it exhibits the expected behavior, such as taking two arguments and returning the first when the result is true.

Now let's analyse the concrete behaviour:

>   -    `or`---Since True is defined to return its first argument, the OR function can be implemented by returning the first argument if it is True, and the second argument otherwise. This correctly models the behavior of the logical OR operation.
>   -   `and`---Similarly to OR, the AND function returns the second argument if it's false, and the first argument otherwise.
>   -   `not`---Trivial.



# Part3: Array Programming with NumPy

>   Combinator calculi such as SKI have influenced the design of languages that emphasize using primitive recursive combinators in “whole data type” operations.
>
>   Ref. https://numpy.org/doc/1.19/reference/index.html



```python
def find_missing(n: int, arr: np.ndarray) -> np.ndarray:
    """Given a positive integer `n` and a sorted array `arr` containing a subset
    of the range [0, n), return a sorted array containing the missing integers from
    the range [0, n).

    You can assume that all inputs to the function are valid.

    find_missing(6, [0, 2, 5])
    [1, 3, 4]
    """
    # BEGIN_YOUR_CODE
    return np.sort(np.setdiff1d(np.arange(n), arr))
    # END_YOUR_CODE


def skyline(heights: np.ndarray) -> int:
    """Given an array `heights` that encodes the heights of buildings in a city skyline, return
    the total number of unique buildings that are visible when standing to the left of the skyline.
    A given building is visible if it is taller than all buildings to its left.

    You can assume that all elements in `heights` are positive.

    skyline([5, 5, 2, 10, 3, 15])
    3
    """
    # BEGIN_YOUR_CODE
    return np.unique(np.maximum.accumulate(heights)).size
    # END_YOUR_CODE


def matched(parentheses: np.ndarray) -> bool:
    """Given an array `parentheses` where every element is '(' or ')', return whether it is a
    balanced set of parentheses. Concretely, this means that each opening parenthesis has a closing
    parenthesis, and for each pair of opening and closing parentheses, the opening parenthesis
    exists to the left of the closing parenthesis.

    matched(['(', ')'])
    True

    matched(['(', ')', ')'])
    False
    """
    # BEGIN_YOUR_CODE
    values = 1. * (parentheses == '(') - 1. * (parentheses == ')')
    cum_values = np.cumsum(values)
    return np.logical_and(cum_values[-1] == 0,
                          np.all(cum_values >= 0.))
    # END_YOUR_CODE
```

It's noteworthy that the solution above employs the `.` symbol. This functional composition style, where functions are chained together using the `.` operator, bears a strong resemblance to Haskell. Both languages, influenced by SKI calculus, approach problem-solving through a data-processing pipeline paradigm (while variables are only declared and refferenced).
