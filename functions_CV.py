from screeninfo import get_monitors
import cv2
import numpy as np

# SHOW THE IMAGE IN THE CENTER OF THE SCREEN
def imshow_center(img_path, window_name, monitor=0):
    img=cv2.imread(img_path)
    if img is None:
        raise ValueError("Error loading image.")

    # Get the primary monitor (first monitor)
    monitor = get_monitors()[monitor]

    # Get the window size (height, width)
    img_height, img_width = img.shape[:2]

    # Compute the scaling factor to maintain aspect ratio
    scale_factor = min(monitor.width / img_width, monitor.height / img_height)

    # Compute new dimensions
    new_width = int(img_width * scale_factor) - 50
    new_height = int(img_height * scale_factor) - 50

    # Resize the image
    resized_image = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Calculate the center of the screen
    center_x = monitor.width // 2
    center_y = monitor.height // 2

    # Calculate the top-left corner of the window
    top_left_x = center_x - (new_width // 2)
    top_left_y = center_y - (new_height // 2)

    # Create a window and move it to the center of the screen
    cv2.namedWindow(window_name)
    cv2.moveWindow(window_name, top_left_x, top_left_y)  # Adjust window size accordingly

    # Display the object with the index
    cv2.imshow(window_name, resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# RESIZE IMAGE 
def resize_img(img, width=1280, height=720):
    scale_width = width / img.shape[1]
    scale_height = height / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    img = cv2.resize(img, (window_width, window_height))
    return img

def show_pixel_intensity(window_name, image):
    """
    Display an image and show pixel intensity values when hovering with mouse.
    Works with both grayscale (1 channel) and color (3 channels) images.
    """
    # Create a copy of the image to avoid modifying the original
    display_img = image.copy()
    # Store original image for reference when getting pixel values
    original_img = image.copy()
    # Resize image to fit screen
    display_img = resize_img(display_img)
    
    # Flag to track if we're showing intensity values
    showing_values = [False]
    # Store the last position to avoid redrawing when not moving
    last_position = [(-1, -1)]
    
    def mouse_callback(event, x, y, flags, param):
        # Calculate the scaling factors between display and original image
        h_original, w_original = original_img.shape[:2]
        h_display, w_display = display_img.shape[:2]
        
        scale_x = w_original / w_display
        scale_y = h_original / h_display
        
        # Map display coordinates to original image coordinates
        orig_x = min(int(x * scale_x), w_original - 1)
        orig_y = min(int(y * scale_y), h_original - 1)
        
        # Only update if position has changed
        if (x, y) != last_position[0]:
            # Create a copy of the resized image to draw on
            img_with_text = display_img.copy()
            
            # Get pixel values from the original image
            if len(original_img.shape) == 2:  # Grayscale image
                intensity = original_img[orig_y, orig_x]
                text = f"Intensity: {intensity}"
            else:  # Color image (BGR)
                b, g, r = original_img[orig_y, orig_x]
                text = f"RGB: ({r}, {g}, {b})"
            
            # Draw text with background for better visibility
            cv2.rectangle(img_with_text, (x, y-25), (x+160, y+5), (0, 0, 0), -1)
            cv2.putText(img_with_text, text, (x+5, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Update the display
            cv2.imshow(window_name, img_with_text)
            
            # Update last position
            last_position[0] = (x, y)
    
    # Create window and set mouse callback
    cv2.imshow(window_name, display_img)
    cv2.setMouseCallback(window_name, mouse_callback)

def remove_small_objects(binary_img, min_area):
    # Ensure binary image is 0 and 255
    binary_img = (binary_img > 0).astype(np.uint8) * 255

    # Get connected components
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_img, connectivity=8)

    # Create output image initialized to black
    output = np.zeros_like(binary_img)

    # Loop through all components (skip background: label 0)
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area >= min_area:
            output[labels == i] = 255

    return output