import motors1
import zumo_button


class Test:

    def drive(self):
        m = motors1.Motors
        m.forward(.2, 3)
        print("I bevegelse")



if __name__ == '__main__':
    test = Test()
    test.drive()
