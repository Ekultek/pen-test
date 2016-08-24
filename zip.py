import zipfile
import sys


def obtain_password(path_to_zip):
    print "Attempting to crack password..."
    dictionary = 'wordlist.txt'
    password = None
    attempts = 0
    zip_file = zipfile.ZipFile(path_to_zip)

    with open(dictionary, 'r') as dict:
        for line in dict.readlines():
            possible = line.strip('\n')
            attempts += 1
            if attempts % 1000 == 0:
                sys.stdout.write("\rAttempts: #{} with {}          ".format(str(attempts), possible))
                sys.stdout.flush()

            try:
                zip_file.extractall(pwd=possible)
                password = 'Password found: {}'.format(possible)
            except RuntimeError:
                pass

    print password
    return password


if __name__ == '__main__':
    obtain_password("C:\dev\zipfiles\zipfiles.zip")

