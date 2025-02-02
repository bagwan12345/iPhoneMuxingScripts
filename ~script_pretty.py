import os
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def get_base_name(filename):
    """Extracts base name from filenames like IMG_0123(2).JPG or IMG_0123.HEIC."""
    base, _ = os.path.splitext(filename)
    base = base.split('(')[0]  # Remove (2) or other suffixes
    return base

def get_first_frame(video_path):
    """Extracts and corrects the first frame of a video file."""
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    cap.release()
    if success:
        if frame.shape[0] > frame.shape[1]:  # Height > Width means likely rotated
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        return frame
    return None

class ImageComparisonApp:
    def __init__(self, root, images, videos):
        self.root = root
        self.images = images
        self.videos = videos
        self.image_queue = sorted([(img, vid) for base_name in sorted(images) if base_name in videos for img in sorted(images[base_name]) for vid in sorted(videos[base_name])])
        self.current_pair = None
        
        # Set background color for the root window
        root.configure(bg='#5389c2')
        
        # Create and configure the labels
        self.img_label = tk.Label(root, bg='#5389c2', fg='white')
        self.img_label.pack(side='left', padx=10)
        
        self.frame_label = tk.Label(root, bg='#5389c2', fg='white')
        self.frame_label.pack(side='left', padx=10)
        
        # Create a frame for the buttons
        button_frame = tk.Frame(root, bg='#5389c2')
        button_frame.pack(side='right', padx=10)

        # Add the buttons with updated styles
        self.confirm_button = tk.Button(button_frame, text="These look similar", command=self.on_confirm, 
                                         width=20, height=2, bg='#5389c2', fg='white', font=('Arial', 10, 'bold'))
        self.confirm_button.pack(side='top', pady=5)

        self.skip_button = tk.Button(button_frame, text="Skip", command=self.next_pair, 
                                      width=20, height=2, bg='#5389c2', fg='white', font=('Arial', 10, 'bold'))
        self.skip_button.pack(side='top', pady=5)
        
        self.next_pair()
    
    def next_pair(self):
        if not self.image_queue:
            messagebox.showinfo("Finished", "No more images to compare.")
            self.root.quit()
            return
        
        self.current_pair = self.image_queue.pop(0)
        img_path, vid_path = self.current_pair
        
        # print(f"Comparing: {img_path} with {vid_path}")
        
        if not os.path.exists(img_path):
            self.next_pair()
            print(f"@ skipping {img_path}?")
            # root.destroy()
            return None

        img = Image.open(img_path).resize((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        self.img_label.configure(image=img_tk, text=img_path, compound='top')
        self.img_label.image = img_tk
        
        frame = get_first_frame(vid_path)
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame).resize((400, 400))
            frame_tk = ImageTk.PhotoImage(frame)
            self.frame_label.configure(image=frame_tk, text=vid_path, compound='top')
            self.frame_label.image = frame_tk
    
    def on_confirm(self):
        if not self.current_pair:
            return
        
        img_path, vid_path = self.current_pair
        base_name = get_base_name(img_path)
        folder = os.path.dirname(img_path)
        
        suffix = 'a'
        while True:
            new_img_path = base_name + suffix + os.path.splitext(img_path)[1]
            new_vid_path = base_name + suffix + os.path.splitext(vid_path)[1]
            
            if not os.path.exists(new_img_path) and not os.path.exists(new_vid_path):
                break
            
            suffix = chr(ord(suffix) + 1)
            if suffix > 'z':
                messagebox.showwarning("Error", "Too many suffixes, cannot rename.")
                return
        
        print(f"Renaming {img_path} to {new_img_path}")
        print(f"Renaming {vid_path} to {new_vid_path}")
        
        os.rename(img_path, new_img_path)
        os.rename(vid_path, new_vid_path)
        
        self.next_pair()

def process_files():
    folder = 'duplicateFiles'
    image_extensions = {'.jpg', '.jpeg', '.png', '.heic'}
    video_extensions = {'.mp4', '.mov'}
    
    images = {}
    videos = {}
    
    for file in sorted(os.listdir(folder)):
        base_name = get_base_name(file)
        ext = os.path.splitext(file)[1].lower()
        path = os.path.join(folder, file)
        
        if ext in image_extensions:
            images.setdefault(base_name, []).append(path)
        elif ext in video_extensions:
            videos.setdefault(base_name, []).append(path)
    
    # print("Loaded images:", images)
    # print("Loaded videos:", videos)
    
    root = tk.Tk()
    root.title("Compare Image and Video Frame")
    app = ImageComparisonApp(root, images, videos)
    root.mainloop()

if __name__ == "__main__":
    process_files()
