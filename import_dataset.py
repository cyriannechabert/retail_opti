import kagglehub

# Download latest version
path = kagglehub.dataset_download("yapwh1208/supermarket-sales-data")

print("Path to dataset files:", path)
import shutil

dest = r"C:/Users/cycyc/retail_opti"
shutil.copytree(path, dest, dirs_exist_ok=True)
print("Dataset copied to:", dest)