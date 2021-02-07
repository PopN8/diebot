if __name__ == '__main__':
    import db_manager
    import traceback

    separator = f"\n{'=' * 50}\n"

    try:
        db_manager.update_schemes()

        print(f'{separator}Adding adventurers A,B,C with no inventory{separator}')

        db_manager.add_adventurer('1', 'A')
        db_manager.add_adventurer('2', 'B')
        db_manager.add_adventurer('3', 'C')

        print(f'{db_manager.get_adventurer(1)}\n{db_manager.get_adventurer(2)}\n{db_manager.get_adventurer(3)}')

        print(f'{separator}Adding Location Absentia and Objective fight barmaid{separator}')

        db_manager.add_location('Asbentia')

        db_manager.add_objective('Fight the barmaid', 'Just don\'t hurt her')

        print(f'{db_manager.get_current_location()}\n{db_manager.get_current_objectives()}')

        print(f'{separator}Giving staff to A{separator}')

        db_manager.give_item('1', 'Staff of Balthazaar', 'You can hit things with it', 1, ['hits hard', 'light'])

        print(db_manager.get_inventory('1'))
        print(db_manager.get_adventurer('2'))

        print(f'{separator}Making new objective{separator}')

        db_manager.add_objective('Apologize to the barman', 'You\'re really sorry')
        db_manager.add_location('Jail')
        db_manager.solve_objective(1)

        db_manager.add_objective('Get out of jail', 'Figure it out')

        print(f'{db_manager.get_current_location()}\n{db_manager.get_current_objectives()}')

        print(f'{separator}Confiscating the staff{separator}')
        print(db_manager.get_adventurer('1'))
        db_manager.remove_item('1', 'Staff of Balthazaar', 1)
        print(db_manager.get_adventurer('1'))
        print(db_manager.get_inventory('1'))

        print(f'{separator}Giving multiple items{separator}')
        db_manager.give_item('3', 'Arrows', 'shoot stuff with \'em', 20)
        db_manager.give_item('3', 'Rocks', 'It\'s just gravel', 13, ['heavy'])

        print(db_manager.get_inventory('3'))

        db_manager.give_item('3', 'Arrows', 'shoot stuff with \'em', 4)

        print(db_manager.get_inventory('3'))

        db_manager.remove_item('3', 'Arrows', 18)
        
        print(db_manager.get_inventory('3'))

        db_manager.remove_item('3', 'Arrows', 6)
        
        print(db_manager.get_inventory('3'))
    except:
        traceback.print_exc()
    finally:
        db_manager.clear_db()