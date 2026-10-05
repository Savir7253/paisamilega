// LeetCode Problem: Trapping Rain Water
// Link: https://leetcode.com/problems/trapping-rain-water/
// Difficulty: Hard
// Language: java

class Solution {
    public int trap(int[] height) {
        int leftmost[] = new  int[height.length];
        leftmost[0] = height[0];
        for(int i = 1 ;i<height.length;i++){
            leftmost[i] = Math.max(leftmost[i-1] , height[i]);
        }
        int rightmost[] = new int[height.length];
        rightmost[height.length-1] = height[height.length-1];
        for(int i = height.length-2; i>=0;i--){
            rightmost[i] =  Math.max(rightmost [i+1] , height[i]);
        }
        int trappedWater= 0 ; 
        for(int i = 0;i<height.length;i++){
            int waterLevel = Math.min(leftmost[i] , rightmost[i]);
            trappedWater += waterLevel-height[i];
        }
        return trappedWater;
    
    }
}