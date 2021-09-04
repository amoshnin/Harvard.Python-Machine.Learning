from logic import *

def Xor(A, B):
    return And(Or(A, B), Or(Not(A), Not(B)))

def ImplicationAndYourInverse(A, B):
    return And(Implication(A, B), Implication(Not(A), Not(B)))

# Each character is either a knight or a knave.
# A knight will always tell the truth.
# A knave will always lie.

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")
CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0

# A says "I am both a knight and a knave."
A = And(AKnight, AKnave)

knowledge0 = And(
    Xor(AKnight, AKnave),
    ImplicationAndYourInverse(AKnight, A)
)

# Puzzle 1

# A says "We are both knaves."
A = And(AKnave, BKnave)
# B says nothing.
B = Not(A)

knowledge1 = And(
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),
    ImplicationAndYourInverse(AKnight, A),
    ImplicationAndYourInverse(BKnight, B)
)

# Puzzle 2

# A says "We are the same kind."
A = Or(And(AKnight, BKnight), And(AKnave, BKnave))
# B says "We are of different kinds."
B = Or(And(AKnight, BKnave), And(AKnave, BKnight))

knowledge2 = And(
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),
    ImplicationAndYourInverse(AKnight, A),
    ImplicationAndYourInverse(BKnight, B),
)

# Puzzle 3

# A says either "I am a knight." or "I am a knave.", but you don't know which.
A = Xor(AKnight, AKnave)
# B says "A said 'I am a knave'."
# B says "C is a knave."
B = And(Implication(AKnight, BKnave), CKnave)
# C says "A is a knight."
C = AKnight

knowledge3 = And(
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),
    Xor(CKnight, CKnave),
    ImplicationAndYourInverse(AKnight, A),
    ImplicationAndYourInverse(BKnight, B),
    ImplicationAndYourInverse(CKnight, C),
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
