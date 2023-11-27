import ij.IJ;
import ij.ImagePlus;
import ij.plugin.PlugIn;
import ij.process.BinaryProcessor;
import ij.process.ByteProcessor;
import ij.process.ImageProcessor;

import java.awt.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;


public class UETPVisualizerPlugin implements PlugIn {

    public void run(String arg) {
        int N = 0;

        /* Step 1: reading .crs file */
        try {
            File file = new File("../dataset/kfu-s-93.crs");
            Scanner sc = new Scanner(file);

            for (; sc.hasNextLine(); sc.nextLine())
                N++;

            sc.close();
        } catch (FileNotFoundException e) {
            System.err.println("Error opening the .crs file.");
        }

        /* Step2: Create new Imageprocessor */
        ImageProcessor binaryIP = new BinaryProcessor(new ByteProcessor(N, N));
        binaryIP.setColor(255);
        binaryIP.fill();

        /* Step3: Read .stu and color */
        try {
            File file = new File("../dataset/kfu-s-93.stu");
            Scanner sc = new Scanner(file);

            binaryIP.setColor(Color.BLACK);
            while (sc.hasNextLine()) {
                String[] tokens = sc.nextLine().split(" ");

                int n = tokens.length;
                int size = (n % 2 == 0) ? n : n - 1;

                if (tokens.length == 1)
                    continue;

                for (int i = 0; i < size - 1; i++) {
                    int x = Integer.parseInt(tokens[i]);
                    int y = Integer.parseInt(tokens[i + 1]);
                    binaryIP.drawPixel(x, y);
                }
            }
            sc.close();
        } catch (FileNotFoundException e) {
            System.err.println(" Error opening the .stu file.");
        }

        /* Step 4: Made a new ImagePlus */
        ImagePlus image = new ImagePlus("UETP Visualization", binaryIP);
        image.show();
        IJ.saveAs("PNG", "../dataset/binary.png");
    }
}