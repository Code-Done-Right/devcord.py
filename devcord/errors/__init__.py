# About all the errors, you might have noticed that Devcord never makes all
# error classes a child class of some parent class, say `Exception`, or `SyntaxError`.
# There is a reason why this is the case.

# Suppose we had to inherit the parent exception class. The class takes in a message only,
# but rich does not have a method for making strings translate to color, unlike colorama's
# `Fore` and `Back`. Therefore, we cannot make the classes give messages to the
# parent class via super().

# This is why all custom error classes have an `error` method, and it MUST be called to
# raise the error.
