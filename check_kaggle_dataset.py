import os

BASE = r"C:\Users\jaanv\.cache\kagglehub\datasets\pacificrm\skindiseasedataset\versions\6"

print("Listing folders inside BASE:\n")
for f in os.listdir(BASE):
    print(" -", f)

print("\nSearching for train/test folders:\n")
for root, dirs, files in os.walk(BASE):
    if "test" in dirs or "train" in dirs:
        print(root)
        print("  contains:", dirs)
