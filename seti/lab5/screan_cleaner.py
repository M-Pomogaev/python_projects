import os
def clean_screen():
    if (input("\nlinux????(type y/n)") == 'y'):
        os.system("clear")
    else:
        os.system("CLS")