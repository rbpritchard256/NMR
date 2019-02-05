from statemachine import StateMachine

def start(f):
    print('start')
    fi = open(f, 'r')
    newState = "read_lines"
    return (newState, fi)

def read_lines(fi):
    print('readlines1')
    try:
        print('1.4')
        for line in fi:
            print('readlines2')
            try:
                print(line)
            except:
                newState = "end_reading"
                return (newState)
    except:
        print('readline3')
        newState='no_text'
        return(newState)

def end_reading():
    print("Finished reading {}".format(f))

def no_text():
    print("No text in {}".format(f))

if __name__== "__main__":
    m = StateMachine()
    m.add_state("Start", start)
    m.add_state("read_lines", read_lines)
    m.add_state("end_reading", None, end_state=1)
    m.add_state("no_text", None, end_state=1)
    m.set_start("Start")
    m.run('txt')


