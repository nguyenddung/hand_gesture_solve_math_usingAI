import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import google.generativeai as genai
from PIL import Image

# Mở webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Khởi tạo HandDetector
detector = HandDetector(
    staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5
)

# Cấu hình API Google Generative AI
try:
    genai.configure(api_key="your api key")
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    print(f"Error with Google Generative AI API: {e}")
    exit()


# Hàm lấy thông tin từ cử chỉ tay
def getHandInfo(img):
    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        hand = hands[0]  # Lấy thông tin tay đầu tiên
        lmList = hand["lmList"]  # Danh sách các điểm mốc tay
        fingers = detector.fingersUp(hand)  # Kiểm tra các ngón tay giơ lên
        return fingers, lmList
    else:
        return None


# Hàm vẽ và xử lý cử chỉ tay
def draw(info, prev_pos, canvas):
    fingers, lmList = info
    current_pos = None
    if fingers == [0, 1, 0, 0, 0]:  # Cử chỉ vẽ (ngón tay cái và ngón trỏ lên)
        current_pos = lmList[8][0:2]  # Đỉnh ngón tay vẽ
        if prev_pos is None:
            prev_pos = current_pos
        cv2.line(canvas, current_pos, prev_pos, (255, 0, 255), 10)
    elif fingers == [1, 0, 0, 0, 0]:  # Cử chỉ xoá (ngón tay cái lên)
        canvas = np.zeros_like(img)  # Xoá màn vẽ
    return current_pos, canvas


# Hàm gửi ảnh đến AI để xử lý
def sendToAI(model, canvas, fingers):
    if fingers == [
        0,
        0,
        1,
        1,
        1,
    ]:  # Cử chỉ yêu cầu giải toán (ngón tay giữa, áp út, út lên)
        pil_image = Image.fromarray(canvas)
        response = model.generate_content(["Solve this math problem", pil_image])
        return response.text


# Khởi tạo biến
prev_pos = None
canvas = None

# Vòng lặp chính
while True:
    success, img = cap.read()
    if not success:
        break  # Nếu không đọc được ảnh từ webcam, thoát chương trình

    img = cv2.flip(img, 1)  # Lật ảnh theo chiều ngang
    if canvas is None:
        canvas = np.zeros_like(img)

    info = getHandInfo(img)  # Nhận thông tin cử chỉ tay
    if info:
        fingers, lmList = info
        prev_pos, canvas = draw(info, prev_pos, canvas)  # Vẽ trên canvas
        result = sendToAI(
            model, canvas, fingers
        )  # Gửi canvas cho mô hình AI nếu có yêu cầu
        if result:
            print("AI Response:", result)  # In kết quả từ AI

    image_combined = cv2.addWeighted(
        img, 0.7, canvas, 0.3, 0
    )  # Kết hợp webcam và canvas để hiển thị

    # Vẽ nút "Thoát"
    cv2.rectangle(image_combined, (20, 20), (170, 80), (0, 0, 255), -1)
    cv2.putText(
        image_combined,
        "THOAT",
        (40, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 255, 255),
        3,
    )

    cv2.imshow("Image", image_combined)  # Hiển thị ảnh kết hợp
    key = cv2.waitKey(1)

    # Nhấn 'q' để thoát chương trình
    if key & 0xFF == ord("q"):
        break

    # Kiểm tra nếu click chuột vào nút "Thoát"
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if 20 <= x <= 170 and 20 <= y <= 80:
                cv2.destroyAllWindows()
                cap.release()
                exit()

    cv2.setMouseCallback("Image", mouse_callback)

# Giải phóng tài nguyên và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
