'''
Since the only operations we can do involve adding and subracting single values and dividing
by 2, the world of binary can make our lives much easier. In binary, dividing by two means
simply taking off the rightmost zero, whereas adding and subtracting one simply switch out the
rightmost value for it's opposite. Starting at the binary representation of our integer, we
want to arrive at 1, or in decimal, 1. To do this, we can represent the binary operations with
simple string manipulations. To arrive at the most efficient solution we will always choose to
divide by two when we can by chopping of the right most zero. When we arrive at a one (odd number),
we will have to look further to see if there are more 1s adjacent. If there aren't, subtracting
a 1 from our number will the switch the 1 to a 0, and next round we can chop it off.
However if there are multiple 1s, we can add 1 to our number. The added one carries over and turns
all the adjacent ones to 0, turning the next 0 into a 1. By counting our steps we can find the
fastest way to arrive at 1.



EX
11101010 234 chop off a zero
1110101 117 switch 1 -> 0
1110100 116 chop off a zero
111010 58 chop off a zero
11101 29 switch 1 -> 0
11100 28 chop off a zero
1110 14 chop off a zero
111 7 add one
1000 8 chop off a zero
100 4 chop off a zero
10 2 chop off a zero
1 All Done !
'''

def solution(n):
    n = int(n) # an integer is needed to convert to binary
    binary = format(n,"b") # binary conversion
    steps = 0; # counting variable
    while binary != "1": # will keep going until our final value is 1
        if binary[-1] == "0": # if the last value is a 0, we have an even number and divide by 2
            binary = binary[:-1] # to divide by 2, we can just chop off the last 0
        elif binary[-1] == "1": # if the last value is a 1, our number is odd
            if binary[-2] == "1" and len(binary) != 2: # if there are adjacent ones, adding gets rid of them
                binary = int(binary, 2) # to save time we can convert our binary back to decimal to add
                binary += 1
                binary = format(binary, "b") # we return to the binary
            else:
                binary = binary[:-1] # if we have a sole 1 then subtracting 1 will get us back to halving our number
                binary += "0"
        steps += 1 # incrementation
    return steps
