class TextMessage(object):
    def __init__(self):
        return

    def core(self, event):
        print(event)
        keyword = ["รถ","เรือ"]
        if event.message.text in keyword:
            print("In keyword")
            return "In keyword"
        elif event.message.text == "Hello,world":
            print("Have been verified")
            return "Have been verified"
        else:
            print("eiei")
        return
