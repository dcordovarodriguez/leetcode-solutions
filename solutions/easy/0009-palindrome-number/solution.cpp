class Solution {
public:
    bool isPalindrome(int x) {
        //neg numbers can't be palindromes
        //# enfing in 0 can't either unless it's 0
        if (x < 0 || (x % 10 == 0 && x != 0)) {
            return false;
        }

        int reversedHalf = 0;

        while (x > reversedHalf) {
            reversedHalf = reversedHalf * 10 + x % 10;
            x /= 10;
        }

        return x == reversedHalf || x == reversedHalf / 10;
        
        
    }
};