import collections
import fractions

'''
Sources used for this solution:
"Markov Chains" series by patrickJMT on youtube.com
"Finding the Inverse of a 3 x 3 Matrix using Determinants and Cofactors" by patrickJMT on youtube.com

The pattern of the doomsday feul can be represented as markov chains, where the chance
of landing in each state is dictated by the chance of landing in the states before it.
Furthermore since some of these states are inescapable, or absorbing, and the chance
of landing in each state from another remains constant, we can precisely calculate these
probabilities. By manipulating the original matrix we are given, we can arrive at the desired
array with the probabilities of landing in each absorbing state.

getP()

     First, we must convert the array we are given into a transition matrix containing the 
     possibilities of moving from one state to another. Rather than convert this matrix to
     standard form, we only need the non-absorbing/transient states. To do this
     we return all the rows that are not filled with zeros, and divide every value by the sum of
     all the values in the row.

getR() and getQ()

    Next, we want to return two different matrices from the transition matrix we just created.
    First, we want a transition matrix that defines the probability of moving between transient
    states (Matrix Q) and one that defines the probaility of moving between transient and absorbing
    states (Matrix R). To create matrix R, we will return the probMatrix with only columns
    of absorbing states, and vice versa for matrix Q

getF()

    From Matrix Q, we need to return the fundamental matrix defined as [Identity - Q]**-1. In order to 
    perform this formula, we need several new functions: 
        eye() 
            returns an identity matrix given the size of Q.
        cutMatrix()
            returns a subsection of a given matrix given a height and width.
        multiply()
            returns the dot product of two arrays. Does this by creating a new array, with element e at x, y,
            such that e = the sum of the products of corresponding values of row x in the first matrix and 
            column y in the second matrix.
        subtract()
            substracts the elements in one array by the corresponding elements in another
        getD
            Finds the determinant of the given array. Since finding the determinant involves adding the products
            of each element in a matrix by the determinant of the submatrix that does not share any rows or
            columns, we can find the determinant recursively, with a base case where the matrix has a size of 2.
        getI
            Finds the inverse of the given array using cofactors and determinants. Creates a new array where each
            element is the determinant of the submatrix from the given array that does not share any rows or columns.
            To get the inverse, we divide each value of this new array by the determinant of the original array.

equalize()

    Once we have calculated the fundamental array, we can multiply it by R and we get the
    chance of arriving at each absorbing state starting from each transient state. Since 
    we only need A0, we can take the first row of this matrix. To get the chances in final
    form, we can first turn all the values into fractions. To find the least common multiple
    between the denominators, we use euclid's method and multiply each fraction in our array
    by this value. Finally, we have our output.


'''


def fractinate(m):
    return [fractions.Fraction(cell).limit_denominator() for cell in m]


def getP(m):
    m = [row for row in m if collections.Counter(row)[0] != len(row)]
    return [[item / (1.0 * sum(row)) for item in row] for row in m]


def getT(m):
    return [collections.Counter(row)[0] != len(row) for row in m]


def getR(m, t):
    height = len(m)
    width = len(m[0])
    correct = [i for i, j in zip(range(width), t) if not j]
    return [[m[row][col] for col in range(width) if col in correct] for row in range(height)]


def getQ(m, t):
    height = len(m)
    width = len(m[0])
    correct = [i for i, j in zip(range(width), t) if j]
    return [[m[row][col] for col in range(width) if col in correct] for row in range(height)]


def eye(size):
    return [[0] * i + [1] + [0] * (size - i - 1) for i in range(size)]


def multiply(m1, m2):
    return [[sum(m1Num * M2Num for m1Num, M2Num in zip(row, col)) for col in zip(*m2)] for row in m1]


def cutMatrix(m, width, height):
    return [row[:height] + row[height + 1:] for row in (m[:width] + m[width + 1:])]


def getD(m):
    size = len(m)
    if size == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    determinant = 0
    sign = 1
    for col in range(size):
        determinant += (sign * m[0][col] * getD(cutMatrix(m, 0, col)))
        sign *= -1
    return determinant


def getI(m):
    size = len(m)
    if size == 1:
        return [[1 / m[0][0]]]
    determinant = getD(m)
    if size == 2:
        return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                [-1 * m[1][0] / determinant, m[0][0] / determinant]]
    c = [[((-1) ** (row + col)) * getD(cutMatrix(m, row, col)) for col in range(size)] for row in range(size)]
    c = map(list, zip(*c))
    size = len(c)
    return [[c[row][col] / determinant for col in range(size)] for row in range(size)]


def subtract(m1, m2):
    dim = len(m1)
    return [[m1[i][j] - m2[i][j] for j in range(dim)] for i in range(dim)]


def getF(q):
    dim = len(q)
    identity = eye(dim)
    return getI(subtract(identity, q))


def equalize(l):
    denom = 1
    for num in [frac.denominator for frac in l]:
        denom = denom * num // fractions.gcd(denom, num)
    l = [(frac * denom).numerator for frac in l]
    l.append(denom)
    return l


def solution(m):
    if len(m) == 1 and len(m[0]) == 1:
        return [1, 1]
    t = getT(m)
    pMatrix = getP(m)
    r = getR(pMatrix, t)
    q = getQ(pMatrix, t)
    f = getF(q)
    fin = fractinate(multiply(f, r)[0])
    return equalize(fin)

 

