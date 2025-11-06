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

    # --- [تعديل هام] 1: تنظيف الجدول قبل البدء ---
    print("...جارٍ تنظيف جدول 'sal_let_word' من البيانات القديمة...")
    cursor.execute("DELETE FROM sal_let_word")
    # قد نحتاج لـ commit هنا لضمان الحذف قبل البدء
    connection.commit() 
    print("تم تنظيف الجدول.")
    # -----------------------------------------------

    # --- 3. سحب قائمة الحروف الأصلية ---
    print("...جارٍ سحب الحروف من جدول Letters...")
    cursor.execute("SELECT LetterID, Letter FROM Letters")
    letters_list = cursor.fetchall()
    if not letters_list:
        print("خطأ: جدول Letters فارغ. لا يمكن المتابعة.")
        sys.exit()
    print(f"تم جلب {len(letters_list)} حرفًا أصليًا.")

    # --- 4. سحب قائمة حروف "سألتمونيها" ---
    print("...جارٍ سحب الحروف من جدول saltmuniha...")
    cursor.execute("SELECT salId, sal_character FROM saltmuniha")
    salt_list = cursor.fetchall()
    if not salt_list:
        print("خطأ: جدول saltmuniha فارغ. لا يمكن المتابعة.")
        sys.exit()
    print(f"تم جلب {len(salt_list)} حرف زيادة.")

    # --- 5. تجهيز البيانات للدمج (التوافيق) ---
    data_to_insert = []
    print("\n...جارٍ توليد التوافيق (الدمج) بدون تكرار...")
    
    skipped_count = 0 # (لمعرفة كم حرف تم تجاهله)

    for letter_row in letters_list:
        letter_id = letter_row.LetterID
        letter_char = letter_row.Letter
        
        for salt_row in salt_list:
            sal_id = salt_row.salId
            sal_char = salt_row.sal_character
            
            # --- [التعديل المطلوب] 2: منع التكرار ---
            if letter_char == sal_char:
                skipped_count += 1
                continue # تجاهل هذا الدمج وانتقل للحرف التالي
            # -----------------------------------------

            new_word = letter_char + sal_char
            data_to_insert.append( (letter_id, sal_id, new_word, None) )

    print(f"تم توليد {len(data_to_insert)} كلمة جديدة.")
    print(f"(تم تجاهل {skipped_count} حالة تكرار مثل 'ءء', 'مم', إلخ)")

    # --- 6. تنفيذ الإدراج في قاعدة البيانات ---
    if data_to_insert:
        print("...جارٍ إدراج الكلمات في جدول sal_let_word...")
        
        insert_query = """
        INSERT INTO sal_let_word (Letters_ID, sal_ID, word, have_mean) 
        VALUES (?, ?, ?, ?)
        """
        
        cursor.executemany(insert_query, data_to_insert)
        
        connection.commit()
        
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
    # --- 7. إغلاق الاتصال ---
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("تم إغلاق الاتصال.")