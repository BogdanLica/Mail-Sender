import os


def find(file,folder):
    for root,dirs,files in os.walk(folder):
        if file in files:
            return os.path.join(root,file)





def main():
    file = input("File: ")
    folder = input("Full path to the file: ")
    print(find(file,folder))






if __name__ == '__main__':
    main()