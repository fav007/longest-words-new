# pylint: disable=missing-docstring


def main():
    # We need to import argv inside the main() body to make our tests pass
    # Importing in the main function will force Python to reload argv between each tests
    from sys import argv
    
    return eval(argv[1] + argv[2] + argv[3])



if __name__ == "__main__":
    print(main())
