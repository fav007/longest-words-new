# pylint: disable=missing-docstring
# pylint: disable=fixme
import sys
if __name__ == "__main__":
    #print(type(sys.argv[1]))*
    try: 
        print((int(sys.argv[1]))**2)
        
    except:
        print("An error occurred.")
