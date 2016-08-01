# -*- coding: utf-8 -*-
class Commands:
    def __init__(self):
        pass

    payment = '/p'
    feedback = '/feedback'
    start = '/start'
    test1 = 'آزمون تصویر خودآگاه من'
    profile = 'مشخصات من'
    account = 'حساب من'
    membership = 'عضویت'
    share_contact = 'اشتراک گذاری'
    print_db = '/print'
    help = 'راهنما'
    box = 'نمایش نتیجه آزمون'
    to_main_menu = 'بازگشت به منوی اصلی'
    # test2 = 'آزمون تحلیل رویا'
    test2 = 'آزمون تحلیل رویا'
    clear = '/cl'
    admin = '/admin'


class States:
    def __init__(self):
        pass

    main_menu = 'Main'
    test1 = 'Test1'
    test2 = 'Test2'
    profile = 'Profile'


class Misc:
    free_membership = "در حال حاضر، شما عضو ربات روان‌یار هستید."
    timeout_msg = "خطا در برقراری ارتباط با درگاه پرداخت. لطفا مجددا تلاش کنید"
    my_account = "در این قسمت می توانید از وضعیت اشتراک خود باخبر شوید یا اطلاعات حساب خود را ویرایش کنید."
    unknown_state = "unknown state, you shouldn't be in here"
    pay_msg = 'لطفا جهت پرداخت از لینک زیر اقدام نمایید' + '\n'
    pay_msg += "پس از پرداخت برای مطلع شدن از وضعیت حساب کاربری خود به قسمت 'عضویت' حساب خود مراجعه کنید"
    golden_user_new = "تبریک! شما عضو طلایی روان‌یار هستید"
    golden_user_msg = "شما عضو طلایی روان‌یار هستید"
    enter_admin_pass = 'کلمه عبور خود را وارد کنید'
    help_msg = 'راهنما'
    share_contact_msg = 'به اشتراک گذاری شماره تماس و مکان فعلی خود'
    location_zone = 'موقعیت مکانی'
    admin_invalid = "Invalid password"
    admin_approved = "here's a list of commands you can use:\n"
    admin_approved += "{}: {}\n".format(Commands.feedback, 'Test1 feedback')
    # admin_approved += "{}: {}\n".format(Commands.feedback, 'Test1 questions')

    def __init__(self):
        pass

    link = '@ravanyaarbot'
    back_to_main_menu_message = 'شما به منوی اصلی بازگشته اید'
    contact_no = 'شماره تماس'




class Label:
    def __init__(self):
        pass

    main_menu = 'منوی اصلی'