// LeetCode Problem: Count the Digits That Divide a Number
// Link: https://leetcode.com/problems/count-the-digits-that-divide-a-number/
// Difficulty: Easy
// Language: java

class Solution {
    public int countDigits(int num) {
        int temp = num;
        int count= 0;
       
        while(temp!=0){
            int r = temp%10;
            if(num%r==0){
                count++;
            }
            temp/=10;
        }
        return count;
    }
        
    }
