# arabic_letters = [
#     'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش',
#     'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه',
#     'و', 'ي', 'أ', 'إ', 'آ', 'ء', 'ؤ', 'ئ', 'ى', 'ة'
# ]

# arabic_diacritics = [
#     'َ',  # فتحة
#     'ً',  # تنوين فتح
#     'ُ',  # ضمة
#     'ٌ',  # تنوين ضم
#     'ِ',  # كسرة
#     'ٍ',  # تنوين كسر
#     'ْ',  # سكون
#     'ّ'   # شدة
# ]

# # --- هذا الجزء يعمل بشكل سليم كما هو ---
# arabic_with_diacritics = []
# for letter in arabic_letters:
#     for diacritic in arabic_diacritics:
#         arabic_with_diacritics.append(letter + diacritic) 
        
# # print(arabic_with_diacritics)

# # --- تصحيح المنطق المطلوب ---

# # 1. نحدد قائمة الحروف التي نريد معالجتها
# # (هذه هي الحروف التي كنت تحاول إضافتها في الكود الأصلي)
# chars_to_process = [
#     'سَ',  # من arabic_with_diacritics
#     'أَ',  # من arabic_with_diacritics
#     'لْ',  # من arabic_with_diacritics
#     'تُ',  # من arabic_with_diacritics
#     'مْ',  # من arabic_with_diacritics
#     'وْ',  # من arabic_with_diacritics
#     'نِ',  # من arabic_with_diacritics
#     'يْ',  # من arabic_with_diacritics
#     'هَ',  # من arabic_with_diacritics
#     'ا'   # من arabic_letters
# ]

# arabic_saltomoniha = []
# i = 0

# # 2. نستخدم حلقة while لنتمكن من "تخطي" الحرف التالي إذا احتجنا
# while i < len(chars_to_process):
#     current_char = chars_to_process[i]
    
#     # 3. هذا هو المنطق الذي طلبته
#     # إذا كان الحرف الحالي 'هَ'
#     if current_char == 'هَ':
#         # تحقق إذا كان هناك حرف تالٍ، وإذا كان 'ا'
#         if i + 1 < len(chars_to_process) and chars_to_process[i+1] == 'ا':
#             arabic_saltomoniha.append('هَا')  # ادمج الحرفين
#             i += 2  # تحرك خطوتين للأمام (تخطى 'هَ' و 'ا')
#         else:
#             # إذا لم يتبعه 'ا'، أضف 'هَ' فقط
#             arabic_saltomoniha.append(current_char)
#             i += 1
#     else:
#         # 4. باقي الحروف تبقى كما هي
#         arabic_saltomoniha.append(current_char)
#         i += 1  # تحرك خطوة واحدة للأمام

# print(arabic_saltomoniha)
# print(arabic_with_diacritics)

# #الاتصال بقاعدة البيانات!!!!

# import pyodbc

# # 1. تحديد معلومات الاتصال (المحدثة)
# server = 'LAPTOP-QPC9F0C5' # اسم السيرفر الذي زودتني به
# database = 'Arabic_Project' # اسم قاعدة البيانات الصحيح

# # 2. إنشاء جملة الاتصال
# try:
#     connection_string = (
#         f'DRIVER={{ODBC Driver 17 for SQL Server}};'
#         f'SERVER={server};'
#         f'DATABASE={database};'
#         f'Trusted_Connection=yes;'
#     )
    
#     # 3. محاولة الاتصال
#     connection = pyodbc.connect(connection_string)
#     print(f"✅ تم الاتصال بقاعدة البيانات '{database}' بنجاح!")
    
#     cursor = connection.cursor()
#     cursor.execute("SELECT Letter FROM Letters WHERE LetterID = 1;")
#     row = cursor.fetchone()
    
#     if row:
#         print(f"اختبار استعلام: تم جلب أول حرف: {row.Letter}")
#     else:
#         print("اختبار استعلام: الجدول فارغ.")

#     cursor.close()
#     connection.close()
#     print("تم إغلاق الاتصال.")

# except pyodbc.Error as ex:
#     sqlstate = ex.args[0]
#     if '18456' in str(ex):
#         print(f"❌ خطأ: فشل تسجيل الدخول للمستخدم 'LAPTOP-QPC9F0C5\\User'.")
#         print("هذا يعني أن حساب ويندوز الخاص بك لا يملك صلاحية الدخول لـ SQL Server.")
#         print("--- يرجى مراجعة الحلول في الأسفل ---")
#     elif '4060' in str(ex):
#          print(f"❌ خطأ: لا يمكن فتح قاعدة البيانات '{database}'. تأكد من صحة الاسم وأن المستخدم لديه صلاحية عليها.")
#     elif sqlstate == 'IM002':
#         print("❌ خطأ: لم يتم العثور على (Driver) مشغل ODBC.")
#     else:
#         print(f"❌ حدث خطأ في الاتصال: {ex}")




# #USER INPUT!!!!

# import pyodbc
# from tabulate import tabulate  # <--- استيراد المكتبة

# # 1. معلومات الاتصال (كما هي)
# server = 'LAPTOP-QPC9F0C5'
# database = 'Arabic_Project'

# connection_string = (
#     f'DRIVER={{ODBC Driver 17 for SQL Server}};'
#     f'SERVER={server};'
#     f'DATABASE={database};'
#     f'Trusted_Connection=yes;'
# )

# # 2. دالة لجلب كل معلومات الحرف
# def get_all_letter_info(letter_to_search):
#     try:
#         connection = pyodbc.connect(connection_string)
#         cursor = connection.cursor()
#         print(f"\n...جارٍ البحث عن معلومات حرف '{letter_to_search}'...")

#         # 3. الاستعلام (Query) - (كما هو)
#         query = """
#         SELECT 
#             'Morphological' AS FunctionType, Category, Example, Description
#         FROM MorphologicalFunctions mf
#         JOIN Letters l ON mf.LetterID = l.LetterID
#         WHERE l.Letter = ?
        
#         UNION ALL
        
#         SELECT 
#             'Grammatical' AS FunctionType, Category, Example, Description
#         FROM GrammaticalFunctions gf
#         JOIN Letters l ON gf.LetterID = l.LetterID
#         WHERE l.Letter = ?
        
#         UNION ALL
        
#         SELECT 
#             'Semantic' AS FunctionType, Category, Example, Description
#         FROM SemanticFunctions sf
#         JOIN Letters l ON sf.LetterID = l.LetterID
#         WHERE l.Letter = ?
        
#         UNION ALL
        
#         SELECT 
#             'Phonetic' AS FunctionType, Category, Example, Description
#         FROM PhoneticFunctions pf
#         JOIN Letters l ON pf.LetterID = l.LetterID
#         WHERE l.Letter = ?
        
#         ORDER BY FunctionType, Category;
#         """
        
#         # 4. تنفيذ الاستعلام (كما هو)
#         cursor.execute(query, 
#                        letter_to_search, 
#                        letter_to_search, 
#                        letter_to_search, 
#                        letter_to_search)
        
#         results = cursor.fetchall()
        
#         if not results:
#             print(f"لم يتم العثور على أي بيانات للحرف '{letter_to_search}'.")
#         else:
#             # --- 5. [التغيير هنا] طباعة النتائج كجدول ---
#             print(f"--- 📜 تم العثور على {len(results)} وظيفة للحرف '{letter_to_search}' ---")
            
#             # تحويل النتائج (fetchall) إلى قائمة عادية
#             data_list = [list(row) for row in results]
            
#             # تحديد العناوين
#             headers = ["نوع الوظيفة", "الفئة", "المثال", "الوصف"]
            
#             # طباعة الجدول
#             print(tabulate(data_list, headers=headers, tablefmt="grid"))
#             # ---------------------------------------------

#         # 6. إغلاق الاتصال
#         cursor.close()
#         connection.close()

#     except pyodbc.Error as ex:
#         print(f"❌ حدث خطأ أثناء الاستعلام: {ex}")

# # --- البرنامج الرئيسي (كما هو) ---
# while True:
#     user_letter = input("أدخل الحرف الذي تريد البحث عنه (أو 'خروج' للإنهاء): ")
#     if user_letter.lower() == 'خروج':
#         break
#     if user_letter:
#         get_all_letter_info(user_letter)

# print("👍 تم إغلاق البرنامج.")
        



# # #Combining two letters Start With Extra letters!!! (FIXED)
# # # SCRIPT 2: (Extra + Main) -> 'سب'
# # # Fills 'sal_let_word' table (the old one with 4 columns)

# # import pyodbc
# # import sys

# # # --- 1. معلومات الاتصال ---
# # server = 'LAPTOP-QPC9F0C5'
# # database = 'Arabic_Project'

# # connection_string = (
# #     f'DRIVER={{ODBC Driver 17 for SQL Server}};'
# #     f'SERVER={server};'
# #     f'DATABASE={database};'
# #     f'Trusted_Connection=yes;'
# # )

# # connection = None
# # cursor = None

# # try:
# #     # --- 2. الاتصال ---
# #     connection = pyodbc.connect(connection_string)
# #     cursor = connection.cursor()
# #     print(f"✅ تم الاتصال بقاعدة البيانات '{database}'")

# #     # --- 3. تنظيف الجدول وإعادة ضبط العداد ---
# #     print("...جارٍ تنظيف وإعادة ضبط 'sal_let_word'...")
# #     cursor.execute("TRUNCATE TABLE sal_let_word") # <-- الجدول الصحيح
# #     connection.commit() 
# #     print("تم تنظيف الجدول (sal_let_word) وإعادة ضبط العداد إلى 1.")
#Combining two letters Start With Extra letters!!!
import pyodbc
import sys

# --- 1. معلومات الاتصال (كما هي) ---
server = 'LAPTOP-QPC9F0C5'
database = 'Arabic_Project'

connection_string = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

connection = None
cursor = None

try:
    # --- 2. الاتصال ---
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print(f"✅ تم الاتصال بقاعدة البيانات '{database}'")

    # --- 3. تنظيف الجدول ---
    print("...جارٍ تنظيف وإعادة ضبط 'sal_let_word'...")
    cursor.execute("TRUNCATE TABLE sal_let_word") 
    connection.commit() 
    print("تم تنظيف الجدول وإعادة ضبط العداد إلى 1.")
    
    # --- 4. سحب قائمة الحروف الأصلية ---
    print("...جارٍ سحب الحروف من جدول Letters...")
    cursor.execute("SELECT LetterID, Letter FROM Letters")
    letters_list = cursor.fetchall()
    if not letters_list:
        print("خطأ: جدول Letters فارغ. لا يمكن المتابعة.")
        sys.exit()

    # --- 5. سحب قائمة حروف "سألتمونيها" ---
    print("...جارٍ سحب الحروف من جدول saltmuniha...")
    cursor.execute("SELECT salId, sal_character FROM saltmuniha")
    salt_list = cursor.fetchall()
    if not salt_list:
        print("خطأ: جدول saltmuniha فارغ. لا يمكن المتابعة.")
        sys.exit()

    # --- 6. تجهيز البيانات للدمج (التوافيق) ---
    data_to_insert = []
    print("\n...جارٍ توليد التوافيق (البدء بحرف الزيادة)...")
    
# #     # --- 4. سحب القوائم ---
# #     print("...جارٍ سحب الحروف...")
# #     cursor.execute("SELECT LetterID, Letter FROM Letters")
# #     letters_list = cursor.fetchall()
    
# #     cursor.execute("SELECT salId, sal_character FROM saltmuniha")
# #     salt_list = cursor.fetchall()
    
# #     if not letters_list or not salt_list:
# #         print("خطأ: أحد الجداول (Letters أو saltmuniha) فارغ.")
# #         sys.exit()

# #     # --- 5. تجهيز البيانات للدمج (التوافيق) ---
# #     data_to_insert = []
# #     print("\n...جارٍ توليد التوافيق (البدء بحرف الزيادة)...")
    
# #     skipped_count = 0 

# #     # --- [التعديل 1: تم عكس الحلقات] ---
# #     # الحلقة الخارجية أصبحت لحروف "سألتمونيها"
# #     for salt_row in salt_list:
# #         sal_id = salt_row.salId
# #         sal_char = salt_row.sal_character
        
# #         # الحلقة الداخلية أصبحت للحروف الأصلية
# #         for letter_row in letters_list:
# #             letter_id = letter_row.LetterID
# #             letter_char = letter_row.Letter
            
# #             if letter_char == sal_char:
# #                 skipped_count += 1
# #                 continue 

# #             # --- [التعديل 2: تم عكس الدمج] ---
# #             new_word = sal_char + letter_char  # (مثال: 'س' + 'ب' = 'سب')
            
# #             # (Letters_ID, sal_ID, word, have_mean)
# #             data_to_insert.append( (letter_id, sal_id, new_word, None) ) # 4 أعمدة فقط
    # --- [التعديل 1: تم عكس الحلقات] ---
    # الحلقة الخارجية أصبحت لحروف "سألتمونيها"
    for salt_row in salt_list:
        sal_id = salt_row.salId
        sal_char = salt_row.sal_character
        
        # الحلقة الداخلية أصبحت للحروف الأصلية
        for letter_row in letters_list:
            letter_id = letter_row.LetterID
            letter_char = letter_row.Letter
            
            # منع التكرار (مثل 'ءء', 'مم')
            if letter_char == sal_char:
                skipped_count += 1
                continue 
            # ------------------------------------

            # --- [التعديل 2: تم عكس الدمج] ---
            new_word = sal_char + letter_char  # (مثال: 'س' + 'ب' = 'سب')
            # ------------------------------------
            
            # (Letters_ID, sal_ID, word, have_mean, classification)
            data_to_insert.append( (letter_id, sal_id, new_word, None, None) ) 

# #     print(f"تم توليد {len(data_to_insert)} كلمة جديدة.")
# #     print(f"(تم تجاهل {skipped_count} حالة تكرار)")

# #     # --- 6. تنفيذ الإدراج في قاعدة البيانات ---
# #     if data_to_insert:
# #         print("...جارٍ إدراج الكلمات في جدول sal_let_word...")
        
# #         # جملة INSERT خاصة بالجدول القديم (4 أعمدة)
# #         insert_query = """
# #         INSERT INTO sal_let_word (Letters_ID, sal_ID, word, have_mean) 
# #         VALUES (?, ?, ?, ?)
# #         """
        # الكود يستخدم 5 أعمدة، وهو متوافق مع الجدول الجديد
        insert_query = """
        INSERT INTO sal_let_word (Letters_ID, sal_ID, word, have_mean, classification) 
        VALUES (?, ?, ?, ?, ?)
        """
        
# #         cursor.executemany(insert_query, data_to_insert)
        
# #         connection.commit()
        
# #         print(f"🎉 نجاح! تم إدراج {cursor.rowcount} صف جديد في 'sal_let_word'.")

# # except pyodbc.Error as ex:
# #     print(f"❌ حدث خطأ: {ex}")
# #     if connection:
# #         connection.rollback()
# # except Exception as e:
# #     print(f"❌ حدث خطأ غير متوقع في بايثون: {e}")

# # finally:
# #     if cursor:
# #         cursor.close()
# #     if connection:
# #         connection.close()
# #         print("تم إغلاق الاتصال.")

# # #Combining two letters Start With Main_Letters!!!
# # import pyodbc
# # import sys

# # # --- 1. معلومات الاتصال ---
# # server = 'LAPTOP-QPC9F0C5'
# # database = 'Arabic_Project'

# # connection_string = (
# #     f'DRIVER={{ODBC Driver 17 for SQL Server}};'
# #     f'SERVER={server};'
# #     f'DATABASE={database};'
# #     f'Trusted_Connection=yes;'
# # )

# # connection = None
# # cursor = None

# # try:
# #     # --- 2. الاتصال ---
# #     connection = pyodbc.connect(connection_string)
# #     cursor = connection.cursor()
# #     print(f"✅ تم الاتصال بقاعدة البيانات '{database}'")

# #     # --- 3. [تعديل هام] تنظيف الجدول وإعادة ضبط العداد ---
# #     print("...جارٍ تنظيف وإعادة ضبط 'let_sal_word'...")
# #     cursor.execute("TRUNCATE TABLE let_sal_word") # <-- استخدمنا TRUNCATE بدلاً من DELETE
# #     connection.commit() 
# #     print("تم تنظيف الجدول وإعادة ضبط العداد إلى 1.")
# #     # -----------------------------------------------

# #     # --- 4. سحب قائمة الحروف الأصلية ---
# #     print("...جارٍ سحب الحروف من جدول Letters...")
# #     cursor.execute("SELECT LetterID, Letter FROM Letters")
# #     letters_list = cursor.fetchall()
# #     if not letters_list:
# #         print("خطأ: جدول Letters فارغ. لا يمكن المتابعة.")
# #         sys.exit()

# #     # --- 5. سحب قائمة حروف "سألتمونيها" ---
# #     print("...جارٍ سحب الحروف من جدول saltmuniha...")
# #     cursor.execute("SELECT salId, sal_character FROM saltmuniha")
# #     salt_list = cursor.fetchall()
# #     if not salt_list:
# #         print("خطأ: جدول saltmuniha فارغ. لا يمكن المتابعة.")
# #         sys.exit()

# #     # --- 6. تجهيز البيانات للدمج (التوافيق) ---
# #     data_to_insert = []
# #     print("\n...جارٍ توليد التوافيق (البدء بالحرف الأصلي)...")
        print(f"🎉 نجاح! تم إدراج {cursor.rowcount} صف جديد في 'sal_let_word'.")
    
    else:
        print("لم يتم العثور على بيانات لتوليد الكلمات.")

except pyodbc.Error as ex:
    print(f"❌ حدث خطأ: {ex}")
    if connection:
        print("...يتم التراجع عن أي تغييرات...")
        connection.rollback()
        print("تم التراجع.")
except Exception as e:
    print(f"❌ حدث خطأ غير متوقع في بايثون: {e}")

finally:
    # --- 8. إغلاق الاتصال ---
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("تم إغلاق الاتصال.")
        
#Combining two letters Start With Main_Letters!!!
import pyodbc
import sys

# --- 1. معلومات الاتصال ---
server = 'LAPTOP-QPC9F0C5'
database = 'Arabic_Project'

connection_string = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

connection = None
cursor = None

try:
    # --- 2. الاتصال ---
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print(f"✅ تم الاتصال بقاعدة البيانات '{database}'")

    # --- 3. [تعديل هام] تنظيف الجدول وإعادة ضبط العداد ---
    print("...جارٍ تنظيف وإعادة ضبط 'let_sal_word'...")
    cursor.execute("TRUNCATE TABLE let_sal_word") # <-- استخدمنا TRUNCATE بدلاً من DELETE
    connection.commit() 
    print("تم تنظيف الجدول وإعادة ضبط العداد إلى 1.")
    # -----------------------------------------------

    # --- 4. سحب قائمة الحروف الأصلية ---
    print("...جارٍ سحب الحروف من جدول Letters...")
    cursor.execute("SELECT LetterID, Letter FROM Letters")
    letters_list = cursor.fetchall()
    if not letters_list:
        print("خطأ: جدول Letters فارغ. لا يمكن المتابعة.")
        sys.exit()

    # --- 5. سحب قائمة حروف "سألتمونيها" ---
    print("...جارٍ سحب الحروف من جدول saltmuniha...")
    cursor.execute("SELECT salId, sal_character FROM saltmuniha")
    salt_list = cursor.fetchall()
    if not salt_list:
        print("خطأ: جدول saltmuniha فارغ. لا يمكن المتابعة.")
        sys.exit()

    # --- 6. تجهيز البيانات للدمج (التوافيق) ---
    data_to_insert = []
    print("\n...جارٍ توليد التوافيق (البدء بالحرف الأصلي)...")
    
# #     skipped_count = 0 

# #     for letter_row in letters_list:
# #         letter_id = letter_row.LetterID
# #         letter_char = letter_row.Letter
        
# #         for salt_row in salt_list:
# #             sal_id = salt_row.salId
# #             sal_char = salt_row.sal_character
            
# #             if letter_char == sal_char:
# #                 skipped_count += 1
# #                 continue 

# #             new_word = letter_char + sal_char
# #             data_to_insert.append( (letter_id, sal_id, new_word, None, None) ) 

# #     print(f"تم توليد {len(data_to_insert)} كلمة جديدة.")
# #     print(f"(تم تجاهل {skipped_count} حالة تكرار)")

# #     # --- 7. تنفيذ الإدراج في قاعدة البيانات ---
# #     if data_to_insert:
# #         print("...جارٍ إدراج الكلمات في جدول let_sal_word...")
        
# #         insert_query = """
# #         INSERT INTO let_sal_word (Letters_ID, sal_ID, word, have_mean, classification) 
# #         VALUES (?, ?, ?, ?, ?)
# #         """
        
# #         cursor.executemany(insert_query, data_to_insert)
        
# #         connection.commit()
        
# #         print(f"🎉 نجاح! تم إدراج {cursor.rowcount} صف جديد (EntryID سيبدأ من 1).")
    
# #     else:
# #         print("لم يتم العثور على بيانات لتوليد الكلمات.")

# # except pyodbc.Error as ex:
# #     print(f"❌ حدث خطأ: {ex}")
# #     if connection:
# #         connection.rollback()
# # except Exception as e:
# #     print(f"❌ حدث خطأ غير متوقع في بايثون: {e}")

# # finally:
# #     if cursor:
# #         cursor.close()
# #     if connection:
# #         connection.close()
# #         print("تم إغلاق الاتصال.")


# create table Letters_With_Haraka


#End