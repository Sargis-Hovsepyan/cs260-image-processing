import ij.*;
import ij.process.*;
import ij.gui.*;
import java.awt.*;
import ij.plugin.*;
import ij.plugin.frame.*;

import java.io.File;
import java.util.Scanner;
import java.io.FileNotFoundException;

public class UETPVisualizerPlugin implements PlugIn {

    public void run(String arg) {
        N = 0;

        // Step 1: reading .crs file
        try {
            File    file = new File("../dataset/kfu-s-93.crs");
            Scanner sc = new Scanner(file);

            while (sc.hasNextLine()) {
                sc.nextLine();
                N++;
            }
            sc.close();
        } catch (FileNotFoundException e){
            System.err.println("Error opening the .crs file.");
        }

        
    }

}