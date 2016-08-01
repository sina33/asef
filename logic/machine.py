from transitions.extensions import HierarchicalMachine
from transitions.extensions.nesting import NestedState


class BotMachine(HierarchicalMachine):
    def before_transition(self):
        print "::::: from ( " + self.state + " ) :::"

    def after_transition(self):
        print "::: to ( " + self.state + " ) :::::"

    def get_q_num(self):
        return int(self.state.split(">")[-1])

    def get_state_prefix(self):
        return self.state.split(">")[0]

    def get_state_as_list(self):
        return list(self.state.split(">"))

    def before_wait(self):
        self.previous_state = self.state

    def proceed(self):
        return True

    def wait_thread(self, chat):
        import threading
        thread = threading.Timer(10.0, self.threaded_function, [chat])
        thread.start()

    def threaded_function(_id):
        from dev_ravanyaar import bot
        from telepot.namedtuple import ReplyKeyboardHide
        bot.sendMessage(_id, 'awake time', reply_markup=ReplyKeyboardHide())

    def __init__(self):
        NestedState.separator = '>'
        states = ['Main',
                  {'name': 'Profile', 'children': ['Gender', 'Age']},
                  {'name': 'Test1', 'children': [str(i) for i in range(1, 11)]},
                  'Result1',
                  {'name': 'Test2', 'children': ['1', '2', {'name': '3', 'children': [str(i) for i in range(1, 8)]}]},
                  'Result2'
                  'Wait',
                  'Admin'
                  ]
        transitions = [
            ['profile', 'Main', 'Profile>Gender'],
            ['next_q', 'Profile>Gender', 'Profile>Age'],
            ['test1', 'Main', 'Test1>1'],
            ['result1', 'Test1>10', 'Result1'],
            ['test2', 'Main', 'Test2>1'],
            ['result2', 'Test2>3>7', 'Result2'],
            ['reset', '*', 'Main'],
            ['admin', '*', 'Admin']
        ]
        HierarchicalMachine.__init__(self, states=states, transitions=transitions, initial='Main')
                                     # before_state_change='before_transition',
                                     # after_state_change='after_transition')
        st_list = list(['Test1>{0}'.format(i) for i in range(1, 11)])
        st_list.append('Result1')
        self.add_ordered_transitions(trigger='next_q', states=st_list, loop=False)
        st_list = list(['Test2>3>{0}'.format(i) for i in range(1, 8)])
        st_list.append('Result2')
        self.add_ordered_transitions(trigger='next_q', states=st_list, loop=False)
        self.add_ordered_transitions(trigger='next_part', states=['Test2>1', 'Test2>2', 'Test2>3>1'], loop=False)
        self.t2_dream_category = int()
        self.t2_dream_subject = int()
        self.add_transition(trigger='wait', source='*', dest='Wait', before='before_wait', conditions=['proceed'])
        self.previous_state = 'Main'
        self.is_waiting = False
        self.wait_interrupted = False


if __name__ == '__main__':
    test = BotMachine()
    print test.state
    test.test1()
    test.next_q()
