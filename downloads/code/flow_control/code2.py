def revive_dead_components():
    class InvalidChoiceError(Exception): pass

    def choice_revive():    revive_components()
    def choice_quit():      raise TestCannotRunException("Dead components exist")
    def choice_continue_(): pass
    def choice_select():
        selected = show_menu("Which components would you like to revive?")
        if not selected:
            logger.info("Nothing selected...")
            raise InvalidChoiceError

        revive_components(selected)

    while True:
        choice = choose('"I see dead components..."\n'
            "Do you wish to (r)evive them all, (s)elect components to revive, "
            "(c)ontinue without reviving, d(i)sable reviver, or (q)uit?",
            { "r": "revive",
              "s": "select", 
              "c": "continue", 
              "Q": "quit"},
            default = "quit")
        try:
            locals().get('choice_%s' % choice)()
            break
        except InvalidChoiceError:
            continue
