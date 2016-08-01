#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import random
import threading
import time
from collections import OrderedDict
from logic.commands import Commands, States, Misc, Label
from datetime import datetime

import pytz
import content.survey1 as survey1
import telepot
import logic.utils as utils
from content.survey1 import profile_gender_options
from telepot.delegate import create_open, per_from_id
from telepot.exception import IdleTerminate
from telepot.helper import UserHandler
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide
from logic.utils import markdown

from content import survey2
from database import db_ops
from logic.machine import BotMachine
from pay import pal


def print_terminal(msg):
    print msg


def print_feedback(_id):
    v = survey1.FEEDBACK
    for i in range(5):
        for j in range(3):
            bot.sendMessage(_id, v[i][j])


def ask(chat, q_num):
    o = survey1.OPTIONS  # survey.get_options()
    q = survey1.get_question(q_num - 1)
    markup = ReplyKeyboardMarkup(keyboard=[[o[2], o[1]], [o[3]], [o[5], o[4]]])
    bot.sendMessage(chat, q, reply_markup=markup)


def ask_profile(chat, sub_state):
    q = survey1.USER_INFO_QUESTIONS
    if sub_state == 'Gender':
        markup = ReplyKeyboardMarkup(
            keyboard=[['زن'], ['مرد'], [Commands.to_main_menu]], one_time_keyboard=True )  # resize_keyboard=True)
        bot.sendMessage(chat, q[0], reply_markup=markup)
    elif sub_state == 'Age':
        li = [[str(i)] for i in utils.age_range()]
        li.append([Commands.to_main_menu])
        markup = ReplyKeyboardMarkup(keyboard=li, resize_keyboard=True)
        bot.sendMessage(chat, q[1], reply_markup=markup)


def get_main_menu_keyboard_markup():
    cmd = Commands
    return ReplyKeyboardMarkup(keyboard=[[cmd.test2, cmd.test1], [cmd.help, cmd.account]])


def get_gift_box_keyboard_markup(box_state='xxxxx', sel=None):
    gift = u'\U0001f381'
    opened = u'\U0001f38a'
    key_arr = [InlineKeyboardButton(text=gift, callback_data=str(i)) for i in range(5)]
    if sel is not None:
        key_arr[int(sel)] = InlineKeyboardButton(text=opened, callback_data=str(sel))
    print_terminal(box_state)
    for i, item in enumerate(list(box_state)):
        if item.lower() == 'o':
            print_terminal(str(i) + ' is [o]')
            key_arr[i] = InlineKeyboardButton(text=opened, callback_data=str(i))
    home = InlineKeyboardButton(text=Commands.to_main_menu, callback_data=str('main'))
    markup = InlineKeyboardMarkup(inline_keyboard=[key_arr, [home]])
    return markup


def test1_completed(chat):
    global message_with_inline_keyboard
    bot.sendMessage(chat, survey1.test1_answer_complete,
                    reply_markup=ReplyKeyboardHide())
    res_index_list = []
    for i in range(1, 6):
        res_index, res_msg = survey1.get_feedback(
            i, db_ops.get_test1_answers(chat, len(survey1.QUESTIONS)))
        res_index_list.append(res_index)
    db_ops.save_test1_result(chat, res_index_list)
    time.sleep(random.randint(2, 6))
    message_with_inline_keyboard = bot.sendMessage(chat, survey1.test1_result_ready,
                                                   reply_markup=get_gift_box_keyboard_markup())


def ask2(chat, part, dream_cat=0, part3_q_num=0):
    if part == 1:
        markup = ReplyKeyboardMarkup(keyboard=[[item] for item in survey2.t1])
        bot.sendMessage(chat, survey2.q1, reply_markup=markup)
    elif part == 2:
        markup = ReplyKeyboardMarkup(keyboard=[[item] for item in survey2.t3[dream_cat]])
        bot.sendMessage(chat, survey2.q3, reply_markup=markup)
    elif part == 3:
        o = survey1.OPTIONS
        markup = ReplyKeyboardMarkup(keyboard=[[o[2], o[1]], [o[3]], [o[5], o[4]]])
        q = survey2.t2[part3_q_num]
        bot.sendMessage(chat, q, reply_markup=markup)


def test2_completed(chat, dream_cat, dream_subj):
    x = dream_cat
    y = dream_subj
    res2 = ''
    if x == 0:
        res2 = survey2.t4[y]
    elif x == 1:
        res2 = survey2.t5[y]
    elif x == 2:
        res2 = survey2.t6[y]
    elif x == 3:
        res2 = survey2.t7[y]
    elif x == 4:
        res2 = survey2.t8[y]
    markup = get_main_menu_keyboard_markup()  # ReplyKeyboardHide()
    bot.sendMessage(chat, res2.split(':', 1)[-1], reply_markup=markup)


class UserHandlerSubclass(UserHandler):
    def __init__(self, seed_tuple, timeout):
        super(UserHandlerSubclass, self).__init__(seed_tuple, timeout, flavors='all')
        self.fsm = BotMachine()
        self.new_user, user_data = db_ops.get_user_data(self.user_id)
        self.fsm.set_state(user_data['state'])
        self.thread = threading.Timer(1.4, self.wait_before_ask)

    def on_message(self, msg):
        # super(UserHandlerSubclass, self).on_message(msg)
        if self.new_user:
            self.new_user_notification(msg)
        print_terminal(msg)
        global message_with_inline_keyboard
        flavor = telepot.flavor(msg)
        cmd = Commands
        st = States
        if flavor == 'chat':
            content_type, chat_type, chat_id = telepot.glance(msg)
            print_terminal(telepot.glance(msg))
            print_terminal('-' * 20)

            # Do your stuff according to `content_type`
            if content_type == 'text':
                message = (msg['text']).encode('utf-8')
                if message == cmd.start:
                    f_name = (msg['from']['first_name'])  # .decode('utf-8')
                    has_profile = db_ops.register_user(chat_id)
                    self.fsm.reset()
                    if has_profile:
                        markup = get_main_menu_keyboard_markup()
                        bot.sendMessage(chat_id, 'خوش آمدی ' + f_name.encode('utf-8'), reply_markup=markup)
                    else:
                        bot.sendMessage(chat_id, survey1.fill_info)
                        self.fsm.profile()
                        # ops.set_state(chat_id, st.profile)
                        ask_profile(chat_id, self.fsm.get_state_as_list()[1])

                elif message == cmd.test1:
                    self.fsm.test1()
                    db_ops.clear_pre_session(chat_id)
                    ask(chat_id, 1)

                elif message == cmd.test2:
                    # self.fsm.test2()
                    # ask2(chat_id, 1)
                    bot.sendMessage(chat_id, "به زودی...")

                elif message == cmd.profile:
                    self.fsm.profile()
                    ask_profile(chat_id, self.fsm.get_state_as_list()[1])

                elif message == cmd.account:
                    # self.fsm.account()
                    markup = ReplyKeyboardMarkup(keyboard=[[cmd.profile, cmd.membership], [cmd.to_main_menu]])
                    bot.sendMessage(chat_id, Misc.my_account, reply_markup=markup)

                elif message == cmd.membership:
                    bot.sendMessage(chat_id, Misc.free_membership)
                    # membership, transid = db_ops.get_membership_status(self.user_id)
                    # print membership, transid
                    # if membership == 'gold':
                    #     bot.sendMessage(self.user_id, Misc.golden_user_msg)
                    # elif transid is not None:
                    #     code = pal.verify_transaction(transid)
                    #     if code.isdigit() and int(code) == 1:
                    #         db_ops.set_membership(self.user_id, 'gold')
                    #         bot.sendMessage(self.user_id, Misc.golden_user_new)
                    #     else:
                    #         pay_link = pal.get_pay_link(transid)
                    #         markup = InlineKeyboardMarkup(inline_keyboard=[
                    #             [InlineKeyboardButton(text='پرداخت', url=pay_link, callback_data='payment')]])
                    #         bot.sendMessage(chat_id, Misc.pay_msg, reply_markup=markup)
                    # else:
                    #     code, transid = pal.create_transaction()
                    #     if code == 1:  # successful
                    #         db_ops.save_transaction(self.user_id, transid)
                    #         pay_link = pal.get_pay_link(transid)
                    #         print pay_link
                    #         markup = InlineKeyboardMarkup(inline_keyboard=[
                    #             [InlineKeyboardButton(text='پرداخت', url=pay_link, callback_data='payment')]])
                    #         bot.sendMessage(chat_id, Misc.pay_msg, reply_markup=markup)
                    #     else:  # timeout and other reasons
                    #         bot.sendMessage(self.user_id, Misc.timeout_msg)

                elif message == cmd.share_contact:
                    markup = ReplyKeyboardMarkup(keyboard=[
                        [dict(text=Misc.contact_no, request_contact=True),
                         KeyboardButton(text=Misc.location_zone, request_location=True)],
                        [cmd.to_main_menu]],
                        one_time_keyboard=True)
                    bot.sendMessage(
                        chat_id, Misc.share_contact_msg, reply_markup=markup)
                    self.fsm.main()

                elif message == cmd.help:
                    markup = get_main_menu_keyboard_markup()
                    bot.sendMessage(chat_id, survey1.help_message, reply_markup=markup)

                elif message == cmd.to_main_menu:
                    markup = get_main_menu_keyboard_markup()
                    bot.sendMessage(chat_id, Label.main_menu, reply_markup=markup)

                # For Debugging
                ##########
                elif message.lower() == cmd.box:
                    gift = u'\U0001f381'
                    key_arr = [InlineKeyboardButton(text=gift, callback_data=str(i)) for i in range(5)]
                    markup = InlineKeyboardMarkup(inline_keyboard=[key_arr])
                    message_with_inline_keyboard = bot.sendMessage(chat_id, 'select a box', reply_markup=markup)
                elif message.lower() == cmd.print_db:
                    bot.sendMessage(chat_id, db_ops.print_table_contents('users'))
                    db_ops.set_state(chat_id, st.main_menu)
                elif message.lower() == cmd.feedback:
                    print_feedback(chat_id)

                elif message.lower() == cmd.clear:
                    db_ops.delete_user(chat_id)
                ##########

                else:
                    ''' msg['text'] is not a command '''
                    user_input = msg['text']
                    # ---- Test1 -----
                    if self.fsm.get_state_prefix() == States.test1:
                        if utils.validate_user_input_for_test1(user_input):
                            q_num = int(self.fsm.get_q_num())
                            ans = utils.parse_answer_value_for_test1(user_input)
                            db_ops.save_answer(chat_id, q_num, ans)
                            if self.fsm.get_q_num() < 10:
                                if self.thread.isAlive():
                                    # ask again
                                    self.thread.cancel()
                                    bot.sendMessage(self.user_id, survey1.duplicate_answer_warning1)
                                    ask(chat_id, q_num)
                                else:
                                    # wait before ask
                                    bot.sendChatAction(chat_id, 'typing')
                                    self.thread = threading.Timer(1.4, self.wait_before_ask)
                                    self.thread.start()
                            else:  # Test1 completed
                                self.fsm.result1()
                                test1_completed(chat_id)
                        else:  # invalid user input in test 1
                            bot.sendMessage(chat_id, survey1.invalid_input, reply_markup=ReplyKeyboardHide())
                    # ----- Test2 -----
                    elif self.fsm.get_state_prefix() == States.test2:
                        part = int(self.fsm.get_state_as_list()[1])
                        if utils.validate_user_input_for_test2(user_input, part, self.fsm.t2_dream_category):
                            if part == 1:
                                self.fsm.t2_dream_category = utils.parse_answer_value_for_test2(user_input, 1)
                                self.fsm.next_part()
                                ask2(chat_id, 2, self.fsm.t2_dream_category)
                            elif part == 2:
                                self.fsm.t2_dream_subject = utils.parse_answer_value_for_test2(user_input, 2,
                                                                                               self.fsm.t2_dream_category)
                                # self.fsm.next_part()
                                # ask2(chat_id, 3, self.fsm.t2_dream_category, 0)
                                # skip part 3
                                test2_completed(chat_id, self.fsm.t2_dream_category, self.fsm.t2_dream_subject)
                                self.fsm.reset()
                            else:  # part == 3
                                q_num = self.fsm.get_q_num()
                                if q_num < 7:
                                    self.fsm.next_q()
                                    ask2(chat_id, part, self.fsm.t2_dream_category, q_num)
                                else:
                                    self.fsm.result2()
                                    test2_completed(chat_id, self.fsm.t2_dream_category, self.fsm.t2_dream_subject)
                                    self.fsm.reset()
                        else:  # invalid user input in test 2
                            bot.sendMessage(chat_id, survey1.invalid_input, reply_markup=ReplyKeyboardHide())

                    elif self.fsm.get_state_prefix() == 'Result2':
                        self.fsm.reset()
                        pass
                    # ----- Profile -----
                    elif self.fsm.get_state_prefix() == States.profile:
                        response = (msg['text']).encode('utf-8')
                        markup = get_main_menu_keyboard_markup()
                        if response == Commands.to_main_menu:
                            self.fsm.reset()
                            bot.sendMessage(self.user_id, Misc.back_to_main_menu_message, reply_markup=markup)
                        elif self.fsm.get_state_as_list()[1] == 'Gender':
                            if response in profile_gender_options.keys():
                                db_ops.save_profile(chat_id, 'gender', profile_gender_options[response])
                                self.fsm.next_q()
                                ask_profile(chat_id, self.fsm.get_state_as_list()[1])
                            else:
                                bot.sendMessage(self.user_id, survey1.invalid_input)
                        elif response in utils.age_range():  # sub_state equals 'Age'
                            for i, item in enumerate(utils.age_range()):
                                if response == item:
                                    db_ops.save_profile(chat_id, 'age', i)
                            self.fsm.reset()
                            bot.sendMessage(chat_id, survey1.info_complete, reply_markup=markup)
                        else:
                            bot.sendMessage(chat_id, survey1.invalid_input, reply_markup=ReplyKeyboardHide())
                    # ----- Main -----
                    elif self.fsm.get_state_prefix() == States.main_menu:
                        markup = get_main_menu_keyboard_markup()
                        bot.sendMessage(chat_id, 'منوی اصلی', reply_markup=markup)
                    # ----- Unknown State -----
                    else:
                        markup = get_main_menu_keyboard_markup()  # reply_markup=ReplyKeyboardHide()
                        bot.sendMessage(chat_id, Misc.unknown_state, reply_markup=markup)
                        self.fsm.reset()

            elif content_type == 'contact':
                if 'phone_number' in msg['contact']:
                    db_ops.save_phone_number(chat_id, msg['contact']['phone_number'])
                    markup = get_main_menu_keyboard_markup()
                    bot.sendMessage(chat_id, Label.main_menu, reply_markup=markup)

        elif flavor == 'callback_query':
            print "gotcha"
            query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
            print_terminal('Callback query: {0} {1} {2}'.format(query_id, from_id, data))
            if not str(data).isdigit():
                markup = get_main_menu_keyboard_markup()
                bot.sendMessage(from_id, Misc.back_to_main_menu_message, reply_markup=markup)
                self.fsm.reset()
            else:
                index = int(data)
                if index in range(5):
                    # check to see if user is allowed to open the box[data]
                    res_array = db_ops.get_test1_result(from_id)
                    bot.sendChatAction(from_id, 'typing')
                    time.sleep(1)
                    bot.sendMessage(from_id, text=survey1.FEEDBACK[index][int(res_array[index])])
                    box_state = db_ops.get_box(from_id)
                    box_state = list('xxxxx') if box_state is None else list(box_state)
                    box_state[index] = 'o'
                    db_ops.save_box(from_id, box_state)
                    markup = get_gift_box_keyboard_markup(''.join([str(i) for i in box_state]), index)
                    bot.sendMessage(from_id, survey1.box_opened, reply_markup=markup)
                    # if message_with_inline_keyboard:
                    # msg_idf = telepot.message_identifier(message_with_inline_keyboard)
                    # bot.editMessageReplyMarkup(msg_idf, reply_markup=markup)
                    # message_with_inline_keyboard = bot.sendMessage(from_id, survey1.box_opened)
                    # else:
                    # bot.answerCallbackQuery(query_id, text='No previous message to edit')

                elif data == 'alert':
                    bot.answerCallbackQuery(query_id, text='Alert!', show_alert=True)
                elif data == 'edit':
                    if message_with_inline_keyboard:
                        msg_idf = telepot.message_identifier(message_with_inline_keyboard)
                        bot.editMessageText(msg_idf, 'NEW MESSAGE HERE!!!!!')
                    else:
                        bot.answerCallbackQuery(query_id, text='No previous message to edit')

        elif flavor == 'inline_query':
            pass

        elif flavor == 'chosen_inline_result':
            pass

    def on_close(self, exception):
        db_ops.set_state(self.user_id, self.fsm.state)
        # self.notify_user('Bye Bye.\n(last state:%s)' % self.fsm.state)
        if exception is not None and not isinstance(exception, IdleTerminate):
            bot.sendMessage(users_info_group_id, str(exception))
        print_terminal('%s %d: closed' % (type(self).__name__, self.id))

    def wait_before_ask(self):
        self.fsm.next_q()
        ask(self.user_id, self.fsm.get_q_num())

    def notify_user(self, msg):
        bot.sendMessage(self.user_id, msg)

    def new_user_notification(self, msg):
        _now = str(datetime.now(tz=pytz.timezone('Asia/Tehran')).strftime('%Y-%m-%d %H:%M:%S')) + '\n'
        info = OrderedDict(chat_id=self.user_id)
        if 'from' in msg.keys():
            if 'username' in msg['from'].keys():
                info['username'] = msg['from']['username'].encode('utf-8')
            if 'first_name' in msg['from'].keys():
                info['first_name'] = msg['from']['first_name'].encode('utf-8')
            if 'last_name' in msg['from'].keys():
                info['last_name'] = msg['from']['last_name'].encode('utf-8')
        total = db_ops.add_user(self.user_id)
        info['Total_Users'] = total
        self.new_user = False
        bot.sendMessage(users_info_group_id, _now + str(json.dumps(info, indent=2, separators=(',', ': '))))


if __name__ == "__main__":
    TOKEN = '228572738:AAFAZf9U3i1yt1si2ft4Cz-94cLEYmTiRx4'  # RavanYaarDevBot
    # TOKEN = '232659175:AAHpIcg5Dax6r_15ZlOwTwSkuUEeE1wVWME'  # RavanYaarBot
    # bot = telepot.Bot(TOKEN)
    users_info_group_id = -116540547
    bot = telepot.DelegatorBot(TOKEN, [
        (per_from_id(flavors='all'), create_open(UserHandlerSubclass, timeout=20)),
        # (per_application(), create_open(OneInstanceOnly)),
        # (per_message(), call(simple_function)),
    ])
    print "Listening..."
    bot.message_loop(run_forever=True)
    message_with_inline_keyboard = None
