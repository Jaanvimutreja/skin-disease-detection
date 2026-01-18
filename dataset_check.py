import os
import kagglehub

# Download dataset
path = kagglehub.dataset_download("pacificrm/skindiseasedataset")

print("Dataset path:", path)
print("\nTop level folders:")
print(os.listdir(path))

# Go inside first SkinDisease folder
level1 = os.path.join(path, "SkinDisease")
print("\nInside first SkinDisease folder:")
print(os.listdir(level1))

# Go inside second SkinDisease folder (actual data)
data_dir = os.path.join(level1, "SkinDisease")

print("\nDisease classes found:\n")

for disease in os.listdir(data_dir):
    disease_path = os.path.join(data_dir, disease)
    if os.path.isdir(disease_path):
        print(disease, ":", len(os.listdir(disease_path)))

print("\nDataset structure verified correctly.")
