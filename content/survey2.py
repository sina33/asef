#!/usr/bin/python
# -*- coding: utf-8 -*-

# Options
OPTIONS = dict()
o = [''] * 5
o[0] = 'کاملاً موافق'
o[1] = 'موافق'
o[2] = 'متوسط'
o[3] = 'مخالف'
o[4] = 'کاملاً مخالف'
# o[5] = 'بازگشت به منوی اصلی'
for i, item in enumerate(o):
    OPTIONS[i + 1] = item

q1 = 'بیشتر اوقات چه خوابی می‌بینید؟'
t1 = [''] * 5
t1[0] = 'در مورد خودم'
t1[1] = 'در مورد دیگران'
t1[2] = 'در مورد جهان اطراف'
t1[3] = 'در مورد نیازها و عواطف'
t1[4] = 'کابوس'

t2 = [''] * 7
t2[0] = '۱- مدام در حال ارزیابی خودم هستم.'
t2[1] = '۲- گاهی احساس می‌کنم دنیا در حال تمام شدن است.'
t2[2] = '۳- به چیزهای ماورائی و عجیب درگیری ذهنی دارم.'
t2[3] = '۴- هنوز هم تخیلات کودکانه دارم.'
t2[4] = '۵- اینکه دیگران چه فکری در مورد من می‌کنند خیلی برایم مهم است.'
t2[5] = '۶- گذشته‌ها را بیشتر از اکنون دوست دارم.'
t2[6] = '۷- نسبت به آینده خوش‌بین هستم.'

age = None
gender = None
education = None
married = None
nth_child = None

q3 = 'معمولا در رابطه با کدام موضوع خواب می‌بینید؟'
t3 = [[]] * 5
t3[0] = ['امتحان', 'سقوط', 'صعود', 'قدرت داشتن', 'بیماری یا شفا یافتن', 'در آستانه مرگ بودن', 'رانندگی و تصادف',
         'پول و ثروت']
t3[1] = ['پدر', 'مادر', 'دوستان', 'همسایه', 'افراد ناشناس', 'افراد صاحب قدرت (معلم، سیاسیون و...)',
         'خواهرو برادر و همسر']
t3[2] = ['باران', 'برف', 'طوفان، سیل، زلزله، جنگ', 'معنوی و روحانی', 'مکان­ها و تصاویر عجیب غریب', 'جانوران وحشی',
         'فضاهای سیاه و سفید', 'فضاهای رنگی']
t3[3] = ['عشق و دوست داشتن', 'خوردن و نوشیدن', 'جنسی', 'خشم و پرخاشگری', 'طرد و تحقیر شدن',
         'اعمال قدرت و نفوذ به دیگران']
t3[4] = ['کار شرم آور در ملأ عام', 'کر یا کور شدن، قفل شدن زبان یا عضلات', 'فضای بسته', 'کثیفی و حشرات',
         'موجودات غیر واقعی و ترسناک', 'جنون و دیوانگی']

t4 = [None] * len(t3[0])
t4[0] = 'متحان دادن: کمال‌گرا، خوش‌بین بودن به آینده، خوش‌بینی به توان در حل مشکلات، جنگجو بودن، توانایی مقابله مشکلات'
t4[
    1] = 'سقوط: افسرده خو، احساس نرسیدن به آرمان‌ها و اهداف، احساس شکست مداوم در زندگی، نارضایتی از توانایی‌های خود، احساس گناه'
t4[2] = 'صعود: جاه طلب، تنوع‌خواه، کمی مستبد و خود و رای، تمایل به امور راز آلود، باور به امور فراطبیعی، کمال‌گرا'
t4[
    3] = 'قدرت: غالباً مقهور افراد صاحب قدرت بودن، مشکل در ابراز وجود، ترس از مواجه شدن با ادارات، پلیس، معلم و استاد، پدر، افراد صاحب قدرت'
t4[
    4] = 'بیماری یا شفا یافتن: تمایل یا وسواس به انجام فعالیت بدنی، تمایل به راه رفتن، عاشق سفر، تمایل زیاد به دیدن جاهای جدید، ترس از پیری، پرخور، خودخواه'
t4[
    5] = 'در آستانه مرگ بودن: درگیر در افکار فلسفی، دارای استعداد ادبیات و علوم انسانی، خستگی و سرخوردگی از جهان بیرون، چیزهای زیادی در دنیا باقی نمانده که شما را خوشحال کند، تمایل به فضای آرام با نور کم و موسیقی ملایم، ویژگی‌های انفجاری در بروز خشم یا شادی، درگیری ذهنی نسبت به قضاوت دیگران، آشفتگی ظاهری'
t4[
    6] = 'رانندگی و تصادف: هیجان خواه، تنوع طلب، تلاش برای پنهان کردن افکار درونی خود از دیگران، خودشیفته، باهوش، تفکر راجع به روابط اجتماعی و تلاش برای تاثیر گذاری در دیگران'
t4[
    7] = 'پول و ثروت: احساس خودکم بینی، مشکل در اعتماد به نفس، لجوج، وسواس ذهنی نسبت به دخل و خرج، علاقمند به ارتباط گرفتن با آدم‌های پولدار، ظاهر بین، خودشیفته، توان مدیریتی، قاطع'

t5 = [None] * len(t3[1])
t5[0] = 'پدر: احساس مسئولیت در قبال خانواده، نارضایتی از روابط خانوادگی، تمایل به استقلال، مدیر و مدبر، کینه‌توز'
t5[1] = 'مادر: ناکامی در روابط عاطفی، زودرنج، نیاز به حضور دیگران، وابسته، تمایل به روابط اجتماعی بالا'
t5[2] = 'دوستان: احساس طرد شدن، درگیری ذهنی با قضاوت دیگران، احساس تنهایی، تمایل به ادبیات و شعر و موسیقی'
t5[3] = 'همسایه: محافظه‌کار، ترس از روابط اجتماعی، تمایل به حفظ موقعیت فعلی و ترس از عوض کردن فضا، منظم، خوش قول'
t5[4] = 'افراد ناشناس: درگیری ذهنی با اخلاق و مسئولیت، مشکل‌تراشی، مشغله کاری ودرسی، درگیری ذهنی با تلف کردن وقت و نظم'
t5[
    5] = 'افراد صاحب قدرت (معلم، سیاسیون و...): دارای افکار عجیب و غریب، تمایل به پنهان کردن تمایلات درونی، دقیق، حسابگر، توانایی شناخت دیگران، درگیری با فلسفه، سیاست و جامعه‌شناسی، تمایل به پرهیز از درگیری'
t5[6] = 'خواهرو برادر و همسر: جاه طلب، خودرای، حسادت، پر تلاش، پشتکار بالا، وسواس فکری، تنوع طلب'

t6 = [None] * len(t3[2])
t6[
    0] = 'باران: شاعر مسلک، تمایل مفرط به هنر و زیبایی‌شناسی، علاقه به طبیعت گردی، میل به تنهایی و درون‌گرایی، احساسات معنوی'
t6[1] = 'برف: غمگین، تمایلات عرفانی، تمایل به مسائل ماوراء طبیعت، عاشق، علاقه به هنر'
t6[
    2] = 'طوفان، سیل، زلزله، جنگ: میل به پس کشیدن از دنیا، تمایل مفرط به خواب، تاریکی، میل به نظریه‌های انتقادی، تمایل به فرار کردن از شهر، درونگرایی'
t6[
    3] = 'معنوی و روحانی: تنهایی، اندوه، دارای تعارضات درونی زیاد، ذهن پیچیده، کم حرف و متمایل به سکوت، علاقه به تغییر فصول'
t6[
    4] = 'مکان‌ها و تصاویر عجیب غریب: احساس سرو صدای زیاد در سر، تحلیل‌گر، حسابگر، محافظه‌کار، زیرک، دارای ویژگی‌های رهبری'
t6[
    5] = 'جانوران وحشی: مرتب، به هم ریختگی در مواقع شلوغ و بی‌نظم، ترسو، حفظ ظاهری جسور در نگاه دیگران، سرسخت در مواقع بروز مشکل'
t6[
    6] = 'رؤیاهای سیاه و سفید: گذشته بازی، تمایل مفرط به یادآوری خاطرات، کم حرف، علاقه به تاریخ، افسرده خو، ذهن فلسفی، تمایل به اندیشه‌های پیچیده، دوستان اندک، مشکل در اعتماد کردن'
t6[
    7] = 'رؤیاهای رنگی: تنوع طلب، تمایل به محیط‌های جدید، علاقه مفرط به سفر، علاقه به ارتباط گرفتن با آدمهای جدید، زودرنج، اعتماد به اطرافیان'

t7 = [None] * len(t3[3])
t7[
    0] = 'عشق و دوست داشتن: اعتماد به نفس پایین، درگیری ذهنی با قضاوت دیگران، احساس متفاوت بودن، تفکرات رمانتیک، علاقه به فیلم و رمان، اجتماعی و در عین حال دارای احساس تنهایی'
t7[1] = 'خوردن و نوشیدن: خودخواه، لجوج، حساس، کینه‌توز، پرخاشگر، توانایی رهبری، دارای ذهن اقتصادی'
t7[
    2] = 'جنسی: مقید به چارچوب‌های جنسی، تلاش برای خودشناسی، تلاش برای بهتر جلوه دادن خود، درگیری ذهنی با تعهد و مسئولیت، انتقاد داشتن به فضای اخلاقی موجود، خلاق و باهوش'
t7[
    3] = 'خشم و پرخاشگری: بی‌قرار، ناتوانی در تمرکز روی کارهای پیچیده، ناتوانی در انتظار کشیدن، دارای افکار انتقادی و تند و تیز، تلاش برای اصلاح اجتماع'
t7[
    4] = 'طرد و تحقیر شدن: لجوج، کینه‌توز، توانایی در ضربه زدن ظریف به دشمنان، زیرک، خوددار، تلاش برای دور نگه داشتن افراد دیگر از حریم شخصی'
t7[
    5] = 'اعمال قدرت و نفوذ به دیگران: غالباً مقهور افراد صاحب قدرت بودن، مشکل در ابراز وجود، ترس از مواجه شدن با ادارت، پلیس، معلم و استاد، پدر، افراد صاحب قدرت، احساس اینکه حق فرد ضایع شده است، دارای توانایی‌های ویژه و متفاوت'

t8 = [None] * len(t3[4])
t8[
    0] = 'کار شرم آور در ملأ عام: ترس از فاش شدن راز شخصی، دارای تجارب ویژه و خاص زندگی، توانایی تأمل به مسائل انتزاعی، ریزبین، دقیق و عاقل، کم حرف، خشم نسبت به حماقت'
t8[
    1] = 'کر یا کور شدن، قفل شدن زبان یا عضلات: مشغله زیاد، خوش قول و مسئولیت پذیر، ترس از بی‌اعتبار شدن، اهل مدارا و کوتاه آمدن'
t8[2] = 'فضای بسته: ترسو، افسرده خو، ناتوانی در تصمیم‌گیری، احساس فشار و استرس زیاد، علاقه‌مند به فضاهای غیر شهری، قانع'
t8[3] = 'کثیفی و حشرات: وسواس فکری و عملی، به هم ریختگی شدید در مواقع بروز مشکل، خودشیفته، اخلاقی و مسئولیت پذیر، قاطع'
t8[4] = 'موجودات غیر واقعی و ترسناک: گذشته‌گرا، علاقه‌مند به تاریخ، تمایل به فیلم و رمان، کم حوصله، لجباز، خودمحور'
t8[
    5] = 'جنون و دیوانگی: اضطرابها و تضادهای زیاد در فضای روحی، یک بحران بزرگ در زندگی داشتن، در آستانه یکی از بزرگترین تغییرات شخصیتی و روحی'
