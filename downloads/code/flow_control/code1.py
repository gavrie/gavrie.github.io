def revive_dead_components():
    while True:
        choice = choose('"I see dead components..."\n'
            "Do you wish to (r)evive them all, (s)elect components to revive, "
            "(c)ontinue without reviving, d(i)sable reviver, or (q)uit?",
            { "r": "revive",
              "s": "select", 
              "c": "continue", 
              "Q": "quit"},
            default = "quit")

        if choice == "revive":
            revive_components()
            break
        elif choice == "quit":
            raise TestCannotRunException("Dead components exist")
        elif choice == "continue":
            break
        elif choice == "select":
            selected = show_menu("Which components would you like to revive?")
            if selected:
                revive_components(selected)
                break
            else:
                logger.info("Nothing selected...")
