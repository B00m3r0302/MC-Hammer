import cmd

class Menu(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = '> '
        self.intro = 'Welcome to the MC Hammer system. Type help or ? to list commands.\n'
        self.scan_results = []
        self.discrepancies = []

    def do_exit(self, inp):
        '''Exit the application. Shorthand: x q Ctrl-D.'''
        print("Bye")
        return True

    def help_exit(self):
        print('Exit the application. Shorthand: x q Ctrl-D.')

    def do_show_scan_results(self, inp):
        '''Show the scan results.'''
        for result in self.scan_results:
            print(result)

    def help_show_scan_results(self):
        print('Show the scan results.')

    def do_show_discrepancies(self, inp):
        '''Show the discrepancies.'''
        for discrepancy in self.discrepancies:
            print(discrepancy)

    def help_show_discrepancies(self):
        print('Show the discrepancies.')

    def display(self, scan_results, discrepancies):
        '''Display the scan results and discrepancies.'''
        self.update(scan_results, discrepancies)
        self.cmdloop()

    def update(self, scan_results, discrepancies):
        '''Update the scan results and discrepancies.'''
        self.scan_results = scan_results
        self.discrepancies = discrepancies
