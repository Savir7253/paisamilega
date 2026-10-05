// LeetCode Problem: Palindrome Number
// Link: https://leetcode.com/problems/palindrome-number/
// Difficulty: Easy
// Language: java

class Solution {
    public boolean isPalindrome(int x) {
        int n=x;
        int original=n;
        int reverse=0;
        
        while(n>0){
            int digit = n%10;
            reverse=reverse*10+digit;
            n=n/10;
        }
        if (n < 0) {
    
        return false;
         }
        if(original==reverse){
            return true;
        }
        else{
            return false;
        }
        
    }
}