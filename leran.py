import cv2
import matplotlib.pyplot as plt
import numpy as np

def erode(image, kernel):
    # Lấy kích thước ảnh và kernel
    height, width = image.shape
    k_height, k_width = kernel.shape

    # Tính toán padding cần thiết cho ảnh
    padding_height = k_height // 2
    padding_width = k_width // 2

    # Tạo ma trận ảnh sau khi co
    eroded_image = np.zeros((height, width), dtype = np.uint8)

    # Duyệt qua từng pixel trong ảnh
    for i in range(padding_height, height - padding_height):
      for j in range(padding_width, width - padding_width):
        # Trích xuất phần ảnh tương ứng với kernel
        image_patch = image[i - padding_height:i + padding_height + 1,
                            j - padding_width:j + padding_width + 1]

        # Tính toán giá trị nhỏ nhất trong phần ảnh tương ứng với kernel
        min_value = np.min(image_patch)

        # Gán giá trị nhỏ nhất cho pixel tương ứng trong phần ảnh khi co
        eroded_image[i, j] = min_value

    return eroded_image

def extract_edges(image, eroded_image):
  # Tách biên của đối tượng trong hình ảnh
  edges = np.abs(image - eroded_image)
  return edges

# Bức ảnh đầu vào A
image_A = cv2.imread("a.jpg", cv2.IMREAD_GRAYSCALE)

# Phần tử cấu trúc kernel 2x2
kernel = np.array([[1,1], [1,1]], dtype = np.uint8)

# Thực hiện phép co ảnh
eroded_image_A = erode(image_A, kernel)

# Tách biên của đối tượng trong ảnh
edges_A = extract_edges(image_A, eroded_image_A)

# In ảnh đầu vào A
plt.subplot(1, 2, 1)
plt.imshow(image_A, cmap="gray") # Hiển thị ảnh gốc
plt.title('Ảnh gốc')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(eroded_image_A, cmap="gray") # Hiển thị ảnh nhị phân
plt.title('Ảnh sau khi tách')
plt.axis('off')

plt.show()

plt.show()
