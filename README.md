# Task 2 – Change Detection Algorithm

This script detects differences between BEFORE (X.jpg) and AFTER (X~2.jpg) images.
Missing or changed objects in the AFTER image are highlighted with bounding boxes.

## How to run

1. Install dependencies:
   pip install -r requirements.txt

2. Place input images inside /input:
   - A.jpg
   - A~2.jpg
   - B.jpg
   - B~2.jpg

3. Run the script:
   python change_detection.py

4. Output images with bounding boxes are saved in /output:
   - A_diff.jpg
   - B_diff.jpg
