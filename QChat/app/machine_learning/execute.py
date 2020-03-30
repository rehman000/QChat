from app.machine_learning import train, check

def execute(*args):
    args = args[0]
    if args[0] == 'check':
        if args[1] == 'covid19':
            check.check_if_covid19_works()
        else:
            print('error: you must type a valid AI')
    elif args[0] == 'train':
        if args[1] == 'covid19':
            if len(args) > 2:
                train.train_covid19(args[2])
            else:
                train.train_covid19('')
        else:
            print('error: you must type a valid AI')
    else:
        print('error: you must input a valid machine learning action')