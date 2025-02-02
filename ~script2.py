import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def get_base_name(filename):
    """Extracts base name from filenames like IMG_0123(2).JPG or IMG_0123.HEIC."""
    base, _ = os.path.splitext(filename)
    base = base.split('(')[0]  # Remove (2) or other suffixes
    return base

def get_first_frame(video_path):
    """Extracts the first frame of a video file."""
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    cap.release()
    if success:
        return frame
    return None

def compare_images(img1, img2):
    """Compares two images using SSIM."""
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img1_resized = cv2.resize(img1_gray, (img2_gray.shape[1], img2_gray.shape[0]))
    similarity = ssim(img1_resized, img2_gray)
    return similarity

def process_files():
    folder = 'duplicateFiles'
    image_extensions = {'.jpg', '.jpeg', '.png', '.heic'}
    video_extensions = {'.mp4', '.mov'}
    
    images = {}
    videos = {}
    
    for file in os.listdir(folder):
        base_name = get_base_name(file)
        ext = os.path.splitext(file)[1].lower()
        path = os.path.join(folder, file)
        
        if ext in image_extensions:
            if base_name not in images:
                images[base_name] = []
            images[base_name].append(path)
        elif ext in video_extensions:
            if base_name not in videos:
                videos[base_name] = []
            videos[base_name].append(path)
    
    for base_name, img_paths in images.items():
        if base_name in videos:
            for img_path in img_paths:
                img = cv2.imread(img_path)
                if img is None:
                    continue
                
                for vid_path in videos[base_name]:
                    frame = get_first_frame(vid_path)
                    if frame is None:
                        continue
                    
                    similarity = compare_images(img, frame)
                    print(f"Similarity between {img_path} and {vid_path}: {similarity:.2f}")
                    
                    if similarity > 0.75:
                        new_name = input(f"{img_path} and {vid_path} seem similar. Enter new name (or press Enter to skip): ")
                        if new_name:
                            new_img_path = os.path.join(folder, new_name + os.path.splitext(img_path)[1])
                            new_vid_path = os.path.join(folder, new_name + os.path.splitext(vid_path)[1])
                            os.rename(img_path, new_img_path)
                            os.rename(vid_path, new_vid_path)
                            print(f"Renamed to {new_img_path} and {new_vid_path}")

if __name__ == "__main__":
    process_files()
