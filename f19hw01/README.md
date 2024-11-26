# Part 1: Implementation of SKI Interpreter

SKI Expr definition:

$$
e\ :=\ S\ |\ K\ |\ I\ |\ x\ |\ e\ e
$$

Property:

$$
e\ \rightarrow^* e'\quad \text{which cannot be rewritten any further}
$$

`src/ski.py` defines the expressions in SKI.

> - In our Python framework, the combinators S, K, and I are represented as `S()`, `K()`, and `I()`, a variable x as `Var("x")`, and an application e1 e2 as `App(e1,e2)`
>
> - To check whether an expression e is, for example, the K combinator, you can use `isinstance(e, K)` which returns True if e is indeed the K combinator, and False otherwise.
>
> - cd to `f19hw01`, run `sh testski.sh` to test the output