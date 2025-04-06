def startup():
    def requestName():
        try:
            name = input("What's your name? ")
        except TypeError:
            print("Cannot use an integer as a name.")
            requestName()
        print(f"Hello, {name}.")
    def requestFeeling():
        try:
            feeling = input.lower("How are you feeling today: Sad/Happy/Neutral/Angry")
        except TypeError:
            print("Cannot use an integer as a feeling.")
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
startup()