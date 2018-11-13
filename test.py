from motors import *
import zumo_button


class Test:

    def drive(self):
        m = Motors()
        m.forward(.2, 3)
        print("I bevegelse")



if __name__ == '__main__':
    test = Test()
    test.drive()
