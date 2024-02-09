import os
def search():
    disk = input("select which disk to hash: ")
    file_paths = []
    for root, dirs, files in os.walk(disk, topdown=True):
        for name in files:
            file_paths.append(os.path.join(root, name))
        
        for name in dirs:
            file_paths.append(os.path.join(root, name))

    with open(r"hash.txt", "w") as text_file:
        for path in file_paths:
            try:
                text_file.write(path + '\n')
            except:
                print(f"Error writing to file:")
search()
print("we are finished")
