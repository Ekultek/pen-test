import argparse
import crypt
import threading
from multiprocessing import Pool, Queue


queue = Queue()


def test_pass(user, crypt_pass, wordlist):
    salt = crypt_pass[0:2]
    for word in wordlist:
        crypt_word = crypt.crypt(word, salt)
        if crypt_word.strip() == crypt_pass.strip():
            queue.put("Password for {} is: {}".format(user, word))
            return

    queue.put("Password for {} not found.".format(user))


class UnixPasswordCracker(object):
    pool = Pool()

    def user_threads(self, function, arguments):
        t = threading.Thread(target=function, args=arguments)
        t.start()
        t.join()

    def multi_thread_pools(self, function, arguments):
        return self.pool.apply_async(function, arguments)

    def begin(self, mode=None):
        wordlist = 'worldlist.txt'
        with open(wordlist, 'r') as possibles:
            dict_words = [possibles.strip("\n").strip() for line in possibles.readlines()]

        passwords = 'passwords.txt'
        with open(passwords, 'r') as passes:
            for line in passes.readlines():
                if ":" in line:
                    user = line.split(":")[0]
                    crypt_pass = line.split(":")[1].strip(' ')
                    args = [user, crypt_pass, wordlist]

                    if mode == "threading":
                        self.user_threads(test_pass, args)
                    elif mode == "pool":
                        self.multi_thread_pools(test_pass, args)
                    else:
                        test_pass(*args)

        self.pool.close()
        self.pool.join()

        while not queue.empty():
            print queue.get()


if __name__ == '__main__':
    mode = None
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', help="Valid choices: 'pool' and 'threading'")
    args = parser.parse_args()
    if args.mode:
        mode = args.mode

    UnixPasswordCracker().begin(mode=mode)
