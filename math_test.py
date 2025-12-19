from my_math import Variable,Term

v1 = Variable(
    name="x",
    koeffizient=2,
    exponent=2
)
v2 = Variable(
    name="y",
    koeffizient=3,
    exponent=2
)
print(v1.ausrechnen(10))

term = Term(
    variables=[v1],
    vorzeichen="-"
)
print(term.ausrechnen(x=10))