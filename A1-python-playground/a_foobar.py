"""
The classic interview hazing ritual, now with extra chaos.

Rules:
  - For multiples of 3:           print "Foo"
  - For multiples of 5:           print "Bar"
  - For multiples of 7:           print "Bop"
  - For multiples of 3 AND 5:     print "FooBar"
  - For multiples of 3 AND 7:     print "FooBop"
  - For multiples of 5 AND 7:     print "BarBop"
  - For multiples of 3, 5, AND 7: print "FooBarBop"
  - For multiples of 11:          append "Bap" to whatever you would print
                                  (or print "Bap" alone if no other rule fires)
  - For everything else:          print the number itself

Example: foobar(1, 16) should print:
    1
    2
    Foo
    4
    Bar
    Foo
    Bop
    8
    Foo
    Bar
    Bap
    Foo
    13
    Bop
    FooBar

This file has no ⭐ CORE parts.

DO NOT MODIFY THE FUNCTION SIGNATURES.
"""


def foobar_word(n: int) -> str:
    """
    Returns the foobar string for a single integer n.

    Applies the rules above in order: build a word from the 3/5/7 divisors,
    append "Bap" if divisible by 11, and fall back to str(n) if the word
    would otherwise be empty.

    Arguments:
        n -- any integer

    Returns:
        str -- the word to print for n
    """

    # Write your solution here.


def foobar(start: int, stop: int) -> None:
    """
    Prints one foobar_word per line for each integer in [start, stop).

    Arguments:
        start -- inclusive lower bound
        stop  -- exclusive upper bound
    """

    # Write your solution here.


# ---------------------------------------------------------------------------
# Prompt / demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import contextlib
    import io

    def check(label, get, expected):
        """Print OK if `get()` returns `expected`, NOT YET otherwise."""
        try:
            got = get()
        except Exception as e:
            print(f"NOT YET: {label} (raised {type(e).__name__}: {e})")
            return
        if got == expected:
            print(f"OK: {label}")
        else:
            print(f"NOT YET: {label}\n    expected {expected}\n    got      {got}")

    def printed_lines(start, stop):
        """The lines that `foobar(start, stop)` prints."""
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            foobar(start, stop)
        return buffer.getvalue().splitlines()

    # Smoke test: compares your code with the example in the docstring above.
    example = "1 2 Foo 4 Bar Foo Bop 8 Foo Bar Bap Foo 13 Bop FooBar".split()
    check("foobar_word(1) to foobar_word(15) match the example", lambda: [foobar_word(n) for n in range(1, 16)], example)
    check("foobar(1, 16) prints the example, one word per line", lambda: printed_lines(1, 16), example)

    print()
    print("=== FooBarBop(Bap) ===")
    print("Rules: Foo=÷3  Bar=÷5  Bop=÷7  Bap=÷11  (combined for multiple divisors)\n")

    try:
        start = int(input("Start (inclusive): "))
        stop = int(input("Stop  (exclusive): "))
    except ValueError:
        print("Please enter integers.")
        raise SystemExit(1)

    print()
    foobar(start, stop)
