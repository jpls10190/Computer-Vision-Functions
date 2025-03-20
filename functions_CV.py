from screeninfo import get_monitors
import cv2

# SHOW THE IMAGE IN THE CENTER OF THE SCREEN
def imshow_center(img_path, window_name, monitor=0):
    img=cv2.imread(img_path)
    if img is None:
        raise ValueError("Error loading image.")

    # Get the primary monitor (first monitor)
    monitor = get_monitors()[monitor]

    # Get the window size (height, width)
    window_height, window_width = img.shape[:2]

    # Compute the scaling factor to maintain aspect ratio
    scale_factor = min(monitor.width / window_width, monitor.height / window_height)

    # Compute new dimensions
    new_width = int(window_width * scale_factor)
    new_height = int(window_height * scale_factor)

    # Resize the image
    resized_image = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Calculate the center of the screen
    center_x = monitor.width // 2
    center_y = monitor.height // 2

    # Calculate the top-left corner of the window
    top_left_x = center_x - (window_width // 2)
    top_left_y = center_y - (window_height // 2)

    # Create a window and move it to the center of the screen
    cv2.namedWindow(window_name)
    cv2.moveWindow(window_name, top_left_x, top_left_y)  # Adjust window size accordingly

    # Display the object with the index
    cv2.imshow(window_name, resized_image)

# RESIZE IMAGE 
def resize_img(img, width, height):
    scale_width = width / img.shape[1]
    scale_height = height / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    img = cv2.resize(img, (window_width, window_height))
    return img