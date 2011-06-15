from metalfinder.existing import Finder
from metalfinder.notify import Notifier
from config import py
import getpass

def main():
    finder = Finder(py)
    finder.to_file(py['existing_file'])
    username = raw_input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    notifier = Notifier(py)
    notifier.connect(username, password)
    notifier.update_albums()

if __name__ == "__main__":
    main()



