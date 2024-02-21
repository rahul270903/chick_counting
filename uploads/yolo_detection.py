import cv2
import numpy as np

def count_chicks(image_path):
    # Load YOLO model and configuration
    net = cv2.dnn.readNet('yolov7.weights', 'yolov7.cfg')
    with open('yolov7.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getUnconnectedOutLayersNames()

    # Load image
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    # Perform forward pass
    blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(layer_names)

    # Process the detected objects
    chick_count = 0
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and classes[class_id] == 'chick':
                chick_count += 1
                x, y, w, h = list(map(int, detection[0:4] * [width, height, width, height]))
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save the result image
    result_image_path = 'static/result_image.jpg'
    cv2.imwrite(result_image_path, img)

    return chick_count

# Example usage
image_path = 'uploads/uploaded_image.jpg'
chick_count = count_chicks(image_path)
print(f'Number of chicks: {chick_count}')
