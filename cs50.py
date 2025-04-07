def requestName():
    try:
        name = input("What's your name? *Case sensitive: ")
    except TypeError:
        print("Please insert your name(Only a-z/A-z and " "). ")
        requestName()
    print(f"Hello, {name}.")
def requestFeeling():
    try:
        feeling = input("How are you feeling today: sad/happy/neutral/angry: *Case sensitive: ")
    except TypeError:
        print("Please insert your feeling(sad/happy/angry/neutral).")
        requestFeeling()
    if feeling == "sad":
        print("Oh, I'm sorry to hear that. Get well soon...")
    elif feeling == "happy":
        print("Oh! I'm happy when you're happy!")
    elif feeling == "neutral":
        print("Oh... kk.")
    elif feeling == "angry":
        print("Awww, why?")
    else:
        print("Invalid input. Please choose either sad/happy/neutral/angry")
        requestFeeling()

while True:
    def Portfolio():
        try:
            def requestPortfolio():
                requestPortfolio = input("Do you want to make a portfolio; yes/no: *Case sensitive ")
        except TypeError:
            print("Please insert yes or no.")
            requestPortfolio()
        if requestPortfolio == "yes":
            print("Okay! Let's start!")
            try:
                name = input("What's your name? ")
            except TypeError:
                print("Please insert your name(Only a-z/A-z and " "). ")
                input("What's your name? ")
            try:
                age = int(input("How old are you? "))
            except TypeError:
                print("Please input your age.")
                int(input("How old are you? "))
            try:
                sex = input("What is your sex? ")
            except TypeError:
                print("Please input your sex.")
                input("What's your sex? ")
            print(f"Name: {name}.")
            print(f"Age: {age}.")
            print(f"Sex: {sex}.")
            print("That's all I can do at the moment. If you want to add more code, please visit: https://github.com/JetSlayer6/Python/blob/main/cs50.py and make any changes you would like!")
        elif requestPortfolio == "no":
            print("Thanks for using me!")
        else:
                print("Input yes/no.")
                requestPortfolio()
            

requestName()
requestFeeling()
requestPortfolio()
