package com.functionalOOP;
import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

public class FileOperator {
    private static File file;
    private static String filename;

    FileOperator(String fname)
    {
        file = new File(fname);
        filename = fname;
    }

    static ArrayList<Integer> readFile( ) throws FileNotFoundException {
        Scanner scanner = new Scanner( file );
        ArrayList<Integer> arrayList = new ArrayList<>();
        while ( scanner.hasNextInt() )
            arrayList.add(scanner.nextInt());
        System.out.println("Given data is taken.");
        return arrayList;
    }

    static void write2File( ArrayList<Integer> aL ) throws IOException {
        String outFileName;
        if ( filename.contains(".") ){
            outFileName = "";
            for ( char i : filename.toCharArray() ){
                if ( i != '.' )
                    outFileName += i;
                else break;
            }
            outFileName += "sorted.txt";
        } else {
            outFileName = "../Data/output.txt";
        }

        File dFile          = new File( outFileName );
        FileOutputStream fo = new FileOutputStream(dFile);
        PrintWriter pw      = new PrintWriter(fo);

        for ( Integer i : aL ){
            pw.println(i);
        }
        pw.close();
        fo.close();
        System.out.println("\nSorted array is written to output file.");
    }

    static void writeResourceInfo( double fru, double lru, long als, double dur ) throws IOException, InterruptedException {
        File cLogFile = new File("/media/safa/EAC47A27C479F5E3/Documents/Tech-Comm-BLG374E/HW3/Logs/logfile" + String.valueOf(als) + "-CPU.txt" );
        File rLogFile = new File("/media/safa/EAC47A27C479F5E3/Documents/Tech-Comm-BLG374E/HW3/Logs/logfile" + String.valueOf(als) + "-RAM.txt" );

        FileOutputStream cfo = new FileOutputStream(cLogFile, true);
        FileOutputStream rfo = new FileOutputStream(rLogFile, true);

        PrintWriter cpw      = new PrintWriter(cfo);
        PrintWriter rpw      = new PrintWriter(rfo);

        cpw.println( String.format("%.02f", dur));                   // in ms
        rpw.println( String.format("%.02f", (lru - fru) / 1024 ));  // in KB
        cpw.close();
        rpw.close();

        cfo.close();
        rfo.close();
        System.out.println("\nProgram is completed.");
        Thread.sleep(10000);
    }
}
