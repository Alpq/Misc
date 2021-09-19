public class Solution
{
    public static int XORHax(int i){
    int rem = i % 4;
    switch(rem){
        case 0:
        return i;
        case 1:
        return 1;
        case 2:
        return i + 1;
    }
    return 0;
    }
    public static int rangeXOR(int start, int end){
        return XORHax(start - 1) ^ XORHax(end);
    }
    public static int solution(int start, int length){
        int checksum = 0;
        for (int i = 0; i < length - 1; i ++){
            int end = start + length - i - 1;
            checksum ^= rangeXOR(start, end);
            System.out.print(i + " " + start + " " + end + " " + (end - start));
            start += length;
            System.out.println();
        }
        return checksum ^ start;
    }
}
