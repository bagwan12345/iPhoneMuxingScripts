# iPhone Muxing Scripts

This is some code that I used to mix-and-match images and videos when trying to convert iPhone Live Photos into Google Motion Photos. This was only necessary in the very specific case of images overflowing after IMG_9999 was taken on the iPhone, causing duplicate images to being formed (e.g. IMG_0123(1).JPG), thus ruining the integrity of the match between the image and its supposedly-corresponding video.  

### createDuplicatesFolder.cmd
- Makes a subfolder called "duplicateFiles" for any files that have a (1) or (2) in their name (as well as the "base" file without brackets).
- If this doesn't run, then just open with Notepad, copy the text, and run it in your own cmd (in the same directory you want to create the duplicateFiles folder in of course).

### moveFilesThatHaveABCInThem.py
- Moves files that end in a, b, c, etc. (e.g. IMG_0123c.JPG would be moved) to a new folder called "fixed."

### runScript.cmd
- Allows you to run "~script.py" if you want to actually see the command line errors (if there are any). 
- Make sure runScript.cmd and script.py are both on the same directory level as the duplicateFiles folder.

### script.py
- This Program that looks at ALL files inside the duplicateFiles folder and allows you to compare each image with a corresponding video's first frame. You then get to decide whether those images match or not. 
- Why is this important? This comes in useful when you have weird filename clashes due to iPhone only allowing up to IMG_9999. If this occurs and you move Live Photos off of an iPhone, those Live Photos that the iPhones create are "separated" into 2 files (a HEIC/JPG and a MP4/MOV). You can rejoin them (using "MotionPhoto2") but that program looks at the file names, and if the file names are all weird then it can cause weird combos of still-images to live-videos.