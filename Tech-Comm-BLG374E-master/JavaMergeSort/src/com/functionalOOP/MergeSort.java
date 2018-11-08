package com.functionalOOP;

/*
    This code is an changed version of the code written by Rajat Mishra and published at https://www.geeksforgeeks.org/merge-sort/
    for our project.
*/
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;

/* Java program for Merge Sort */
class MergeSort
{
    // Merges two subarrays of arr[].
    // First subarray is arr[l..m]
    // Second subarray is arr[m+1..r]
    void merge(ArrayList<Integer> arr, int l, int m, int r)
    {
        // Find sizes of two subarrays to be merged
        int n1 = m - l + 1;
        int n2 = r - m;

        /* Create temp arrays */
        int L[] = new int [n1];
        int R[] = new int [n2];

        /*Copy data to temp arrays*/
        for (int i=0; i<n1; ++i)
            L[i] = arr.get(l + i);
        for (int j=0; j<n2; ++j)
            R[j] = arr.get(m + 1 + j);


        /* Merge the temp arrays */

        // Initial indexes of first and second subarrays
        int i = 0, j = 0;

        // Initial index of merged subarry array
        int k = l;
        while (i < n1 && j < n2)
        {
            if (L[i] <= R[j])
            {
                arr.set(k, L[i]);
                i++;
            }
            else
            {
                arr.set(k, R[j]);
                j++;
            }
            k++;
        }

        /* Copy remaining elements of L[] if any */
        while (i < n1)
        {
            arr.set(k, L[i]);
            i++;
            k++;
        }

        /* Copy remaining elements of R[] if any */
        while (j < n2)
        {
            arr.set(k, R[j]);
            j++;
            k++;
        }
    }

    // Main function that sorts arr[l..r] using
    // merge()
    void sort(ArrayList<Integer> arr, int l, int r)
    {
        if (l < r)
        {
            // Find the middle point
            int m = (l+r)/2;

            // Sort first and second halves
            sort(arr, l, m);
            sort(arr , m+1, r);

            // Merge the sorted halves
            merge(arr, l, m, r);
        }
    }

    /* A utility function to print array of size n */
    static void printArray(ArrayList<Integer> arr)
    {
        int n = arr.size();
        for (int i=0; i<n; ++i)
            System.out.print(arr.get(i) + "\n");
        System.out.println();
    }

    // Driver method
    public static void main(String args[])
    {
        FileOperator fileOperator = new FileOperator(args[0]);
        try {
            ArrayList<Integer> arL = fileOperator.readFile();

            double startTime, endTime, sru, eru;

            sru = (double)Runtime.getRuntime().totalMemory();
            startTime = System.nanoTime();
            MergeSort ob = new MergeSort();
            ob.sort(arL, 0, arL.size()-1);
            endTime = System.nanoTime();
            eru = (double)Runtime.getRuntime().totalMemory();

            double duration = ( endTime - startTime ) / 1000000;  //milliseconds

            fileOperator.write2File(arL);

            fileOperator.writeResourceInfo(sru, eru, arL.size(), duration);


        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
/* This code is contributed by Rajat Mishra */