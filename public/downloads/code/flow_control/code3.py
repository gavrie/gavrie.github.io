def revive_dead_components():

    # ...

    while True:
        choice_func = choose('"I see dead components..."\n'
            "Do you wish to (r)evive them all, (s)elect components to revive, "
            "(c)ontinue without reviving, d(i)sable reviver, or (q)uit?",
            dict(r = choice_revive,
                 s = choice_select, 
                 c = choice_continue,
                 Q = choice_quit
                 ),
            default = "quit")
        try:
            choice_func()
            break
        except InvalidChoiceError:
            continue

