// HackerRank Problem: Java Loops I
// Link: https://www.hackerrank.com/challenges/java-loops-i/problem
// Difficulty: Easy
// Language: java

import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.*;



public class Solution {
    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));

        int N = Integer.parseInt(bufferedReader.readLine().trim());
        for(int i=1;i<11;i++){
            int multi = N*i;
            System.out.println(N+" x "+i +" = " +multi);

        }
        
        bufferedReader.close();
    }
}
