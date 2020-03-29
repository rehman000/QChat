from sys import argv
import covid19 

if __name__ == '__main__':
    if argv[1].lower() == 'covid19':
        if argv[2] == 'json':
            covid19.json_train()
        else:
            covid19.mongo_train()
    else:
        print('no valid arguments given')
