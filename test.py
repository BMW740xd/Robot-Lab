from motors import Motors
from zumo_button import ZumoButton


class Test:

    def drive(self):
        ZumoButton().wait_for_press()
        m = Motors()
        m.forward(.2, 10)
        print("I bevegelse")



if __name__ == '__main__':
    test = Test()
    test.drive()
