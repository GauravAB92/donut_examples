import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def generate_pixel_grid(image_path):
    try:
        # Load the image and ensure transparency is treated as black
        image = Image.open(image_path).convert("RGBA")
        rgba_array = np.array(image)

        # Extract red channel and ensure all alpha-transparent areas are black
        alpha_channel = rgba_array[:, :, 3]
        r_channel = rgba_array[:, :, 0]
        r_channel[alpha_channel == 0] = 0

        # Get image dimensions
        image_height, image_width = r_channel.shape

        # Scale for visualization
        scale = 40  # Scale factor for pixel display
        output_image = Image.new("RGB", (image_width * scale, image_height * scale), "black")
        draw = ImageDraw.Draw(output_image)

        # Load font for labeling
        try:
            font = ImageFont.truetype("arial.ttf", int(scale * 0.5))  # Use a larger font size
        except:
            font = ImageFont.load_default()

        # Iterate over each pixel in the image
        for i in range(image_height):
            for j in range(image_width):
                pixel_value = r_channel[i, j]
                color = (pixel_value, pixel_value, pixel_value)

                # Draw pixel rectangle
                x_start, y_start = j * scale, i * scale
                x_end, y_end = (j + 1) * scale, (i + 1) * scale
                draw.rectangle([x_start, y_start, x_end, y_end], fill=color)

                # Add label to the center of the pixel
                text_color = "white" if pixel_value < 128 else "black"
                text_position = (x_start + scale // 2, y_start + scale // 2)
                draw.text(text_position, str(pixel_value), fill=text_color, anchor="mm", font=font)

        # Save the output image with appropriate naming
        if "." in image_path:
            base_name = image_path.rsplit(".", 1)[0]  # Remove extension
            extension = image_path.rsplit(".", 1)[1]  # Extract extension
        else:
            base_name = image_path
            extension = "png"  # Default to png if no extension is found

        output_path = f"{base_name}_labeled.{extension}"
        output_image.save(output_path)
        print(f"Labeled image saved as {output_path}")

    except Exception as e:
        print(f"Error processing the image: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    generate_pixel_grid(image_path)
