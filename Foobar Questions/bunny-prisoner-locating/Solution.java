public class Solution{
  public static long Gauss (long upTo)
  {
      return (1 + upTo) * upTo / 2;
  }
  public static long thankYouGauss(long first, long last){
      return Gauss(last) - ((first - 1) * first / 2);
  }

  public static String solution(long x, long y) {
      long bottom = Gauss(x);
      return Long.toString(bottom + thankYouGauss(x, x + y - 2));
  }
}
