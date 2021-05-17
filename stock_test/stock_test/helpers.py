


def read_companies(file):

    '''
    read companies and returen a list of those
    '''
    companies = []
    with open(file,'r') as f:
        companies = f.read().splitlines()

    return companies

if __name__ == "__main__":
    file=''
    read_companies(file)