// LeetCode Problem: Sum Multiples
// Link: https://leetcode.com/problems/sum-multiples/
// Difficulty: Easy
// Language: java

class Solution {
    public int sumOfMultiples(int n) {
        
        int num=0;
        for(int i=1;i<=n;i++){
            if(i%3==0 | i %5==0 | i%7==0 ){
             num+= i;
        }  
        }
        return num;  
    }
}