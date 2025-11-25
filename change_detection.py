import cv2
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

def load_pairs(folder):
    before_files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(".jpg") and "~2" not in f
    ]

    pairs = []
    for bf in before_files:
        name = bf.rsplit(".", 1)[0]

        # before = name.jpg
        # after = name~2.jpg
        after_name = f"{name}~2.jpg"

        before_path = os.path.join(folder, bf)
        after_path = os.path.join(folder, after_name)

        if os.path.exists(after_path):
            pairs.append((before_path, after_path, name))

    return pairs

def detect_changes(before_path, after_path):
    before = cv2.imread(before_path)
    after = cv2.imread(after_path)

    if before is None:
        raise ValueError(f"Cannot read: {before_path}")
    if after is None:
        raise ValueError(f"Cannot read: {after_path}")

    gray_before = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    gray_after = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

    # Absolute difference
    diff = cv2.absdiff(gray_before, gray_after)

    # Threshold
    _, thresh = cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY)

    # Dilate
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=2)

    # Contours
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    result = after.copy()

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 150:  # ignore noise
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 3)

    return result

def main():
    if not os.path.exists(INPUT_FOLDER):
        print("ERROR: input folder missing.")
        return
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    pairs = load_pairs(INPUT_FOLDER)

    if not pairs:
        print("No valid before/after image pairs found.")
        return

    for before_path, after_path, name in pairs:
        result_image = detect_changes(before_path, after_path)

        save_path = os.path.join(OUTPUT_FOLDER, f"{name}_diff.jpg")
        cv2.imwrite(save_path, result_image)

        print(f"Saved → {save_path}")

if __name__ == "__main__":
    main()
