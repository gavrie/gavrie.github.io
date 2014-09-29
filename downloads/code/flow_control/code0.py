def revive_dead_components():
    choice = choose('"I see dead components..."\n'
       "Do you wish to (r)evive them, (c)ontinue without reviving, or (q)uit?",
       { "r": "revive", 
         "c": "continue", 
         "Q": "quit"}, 
       default = "quit")

    if choice == "revive":
        revive_components()
    elif choice == "quit":
        raise TestCannotRunException("Dead components exist")
    elif choice == "continue":
        pass

