from decimal import *

"""
sources: https://en.wikipedia.org/wiki/Beatty_sequence

"Sometimes, it's easier to take a step back and 
concentrate not on what you have in front of you, 
but on what you don't," Foobar

The sum that we are tasked with finding has the elements:
1, 2, 4, 5, 7, 8, 9, 11, 12, ...

This sequence of numbers is a Beatty sequence. But rather
than focus on the elements of this sequence, we have to focus
on the elemnents that are "missing:" 
3, 6, 10 ...

Rayleigh's Theorem states that this sequence is itself a Beatty Sequence,
and is also found by flooring the product of an index and an irrational value.
(This irrational value is the reciprocal to sqrt(2))

Since these sequences don't intersect, together they form the set of all 
positive integers, which provides us a solution. Rather than adding up what 
we have, we must subtract what we do not. Given an index, n, that we must calculate 
the sum up to, we can easily calculate the sum of all integers below n with
a simple gauss sum: n*(n+1)/2. From this sum, we can subtract all the numbers 
that are not in our sequence (a.k.a the values of the reciprocal series) up to
that point. (To find the right index of the reciprocal sequence, all we have to
do is floor the quotient of our sequences' last element and our reciprocal 
irrational value.)

Therefore, letting r = sqrt(2), s = the reciprocal of r, 
and v = floor(nr), we know that:

    sum(r, n) = (n + 1)*n/2 - sum(s, floor(v / s)))

After simplifying floor(v / s):

                v               v                       v                                                                         
    let c  =    _       =       _       =       v   -   _       =       nr   -   n       =       n(r   -   1)
                s               r                       r
                               ___
                               r-1
we get:

    sum(r, n) = (n+1)*n/2 - sum(s, c)
    
We can evaluate the sum() call to get a basic recursive expression:

    sum(r,n) = (n+1)*n/2 - c*(c+1) - sum(r, c)
    
This expression makes up the logic behind the bigSum() method. Using the Decimal class, we can manipulate
values with >100 digits without losing precision. 


"""

def bigSum(index):
    if index == 0:
        return 0
    getcontext().prec = 500
    cIndex = int((Decimal(2).sqrt() - 1) * index)
    totalIndex = index+cIndex
    return (totalIndex) * (totalIndex+1)/2 - bigSum(cIndex) - cIndex*(cIndex+1)


def solution(s):
    return bigSum(int(s))


print(solution(str(5)))


print("3656251862507334448148179357411972294813205338243570072399608556509885357" +
"2501592156627075023977411067341589424590108494452342577069275381301528664" +
"8713467314724409580700486858456282969735344383354280498317253684972423688" +
"0399137190063559454262133821524826418317800715699648839069268323667413740" +
"3742614331223435935402453035423695823538445283290619837000290506129738885" +
"5837817678284818646327428940940798745085837091696852308958883678563866545" +
"5192211168001061493525287792007324647921921998049795017289928866989976959" +
"3068942778535840280145136631201950415699342212774262487665784007034469384" +
"2275855344226240937331812480075580")

