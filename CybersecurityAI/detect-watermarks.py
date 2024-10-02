def detect_watermark(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Error loading image.")
        return None

    # Apply edge detection to highlight any potential watermarks
    edges = cv2.Canny(image, 100, 200)

    # Use thresholding to segment potential watermark areas
    _, thresholded = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY)

    # Find contours from the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter small contours, assuming watermarks are larger and more prominent
    potential_watermarks = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:  # Adjust this value based on image resolution and expected watermark size
            potential_watermarks.append(contour)

    # Draw bounding boxes around detected watermarks for visualization
    output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for contour in potential_watermarks:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Return the processed image with watermarks highlighted
    return output_image, len(potential_watermarks) > 0