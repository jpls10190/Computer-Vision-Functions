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
def resize_img(img, width, height):
    scale_width = width / img.shape[1]
    scale_height = height / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    img = cv2.resize(img, (window_width, window_height))
    return img
