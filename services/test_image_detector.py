from services.image_detector import analyze_image

image_path="uploads/test_image.jpg"
result=analyze_image(image_path)
print(result)
