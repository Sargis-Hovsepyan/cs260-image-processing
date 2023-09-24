import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.Blitter;
import ij.process.ImageProcessor;

public class SwapPanelsPluginFilter implements PlugInFilter {

    public int setup(String arg, ImagePlus imp) {
        return DOES_8G | DOES_RGB;
    }

    public void run(ImageProcessor ip) {
        int width = ip.getWidth();
        int height = ip.getHeight();

        /* Step 1: Divide the image into left and right panels */
        int leftWidth = width / 2;
        int rightWidth = width - leftWidth;

        /* Step 2: Swap the left and right panels horizontally */
        ImageProcessor leftPanel = ip.createProcessor(leftWidth, height);
        ImageProcessor rightPanel = ip.createProcessor(rightWidth, height);

        leftPanel.copyBits(ip, 0, 0, Blitter.COPY);
        rightPanel.copyBits(ip, leftWidth, 0, Blitter.COPY);

        leftPanel.flipHorizontal();
        rightPanel.flipHorizontal();

        // Combine the left and right panels
        ip.copyBits(leftPanel, 0, 0, Blitter.COPY);
        ip.copyBits(rightPanel, leftWidth, 0, Blitter.COPY);

        /* Step 3: Divide the combined image into top and bottom panels */
        int topHeight = height / 2;
        int bottomHeight = height - topHeight;

        /* Step 4:  Swap the top and bottom panels vertically */
        ImageProcessor topPanel = ip.createProcessor(width, topHeight);
        ImageProcessor bottomPanel = ip.createProcessor(width, bottomHeight);

        topPanel.copyBits(ip, 0, 0, Blitter.COPY);
        bottomPanel.copyBits(ip, 0, topHeight, Blitter.COPY);

        topPanel.flipVertical();
        bottomPanel.flipVertical();

        // Combine the top and bottom panels to create the final modified image
        ip.copyBits(topPanel, 0, 0, Blitter.COPY);
        ip.copyBits(bottomPanel, 0, topHeight, Blitter.COPY);

        /* Step 5: Save the modified image as "copy.png" and display it */
        ImagePlus image = new ImagePlus("Modified Image", ip);
        IJ.saveAs(image, "PNG", "../dataset/copy.png");
        image.show();
    }
}

