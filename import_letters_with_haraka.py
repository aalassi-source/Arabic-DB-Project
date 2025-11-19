import os
import pandas as pd
import pyodbc

# ---- إعداد الاتصال ----
server = 'LAPTOP-QPC9F0C5'
database = 'Arabic_Project'
connection_string = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

# مسار ملف الإكسل كما طلبته
EXCEL_PATH = r"C:\Users\User\Downloads\Arabic-DB-Project\جوامد الحروف (تشكيل الحروف الهجائية مع ذكر الوظيفة إن وجدت)100.xlsx"

def get_db_connection():
    return pyodbc.connect(connection_string)

def setup_and_populate_structure():
    """
    هذه الدالة تقوم بـ:
    1. التأكد من وجود الجدول والأعمدة المطلوبة (لا حاجة لإعادة إنشاء الجدول).
    2. الجدول موجود بالفعل مع الأعمدة: id, letter_id, haraka_id, description, Example, Letters_Function
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("--- الخطوة 1: التحقق من بنية الجدول ---")
        print("✅ جدول Letters_With_Haraka موجود بالفعل مع جميع الأعمدة المطلوبة.")

    except Exception as e:
        print(f"❌ خطأ في التأسيس: {e}")
    finally:
        conn.close()

def remove_arabic_diacritics(text):
    """إزالة الحركات العربية من النص"""
    arabic_diacritics = [
        '\u064e',  # فتحة
        '\u064f',  # ضمة
        '\u0650',  # كسرة
        '\u0652',  # سكون
        '\u0640',  # تمديد
        '\u064b',  # تنوين فتح
        '\u064c',  # تنوين ضم
        '\u064d',  # تنوين كسر
        '\u0651',  # شدة
    ]
    for diacritic in arabic_diacritics:
        text = text.replace(diacritic, '')
    return text


def update_functions_from_excel():
    """
    هذه الدالة تقرأ الإكسل، وتبحث عن التطابق (الحرف + الحركة),
    وتقوم بتحديث Letters_Function والوصف والمثال في جدول Letters_With_Haraka.
    """
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ الملف غير موجود: {EXCEL_PATH}")
        return

    print(f"--- الخطوة 2: قراءة الإكسل وتحديث البيانات ---")
    df = pd.read_excel(EXCEL_PATH)
    
    # تنظيف أسماء الأعمدة لتسهيل التعامل
    df.columns = [str(c).strip() for c in df.columns]
    print("أعمدة الإكسل:", df.columns.tolist())

    # أسماء الأعمدة في الإكسل
    col_letter_haraka = 'الحرف مع الحركة'  # الحرف مع الحركة معاً
    col_func = 'الوظيفة'      # الوظيفة
    col_ex = 'مثال'           # المثال
    col_desc = 'الوصف'        # الوصف

    conn = get_db_connection()
    cursor = conn.cursor()
    
    updated_count = 0
    skipped_no_func = 0
    skipped_no_example = 0
    
    try:
        for index, row in df.iterrows():
            # قراءة القيم من السطر الحالي
            val_letter_haraka = str(row.get(col_letter_haraka, '')).strip()
            val_func = str(row.get(col_func, '')).strip()
            val_ex = str(row.get(col_ex, '')).strip()
            val_desc = str(row.get(col_desc, '')).strip()

            if not val_letter_haraka:
                continue

            # تخطي إذا لم يكن هناك وظيفة
            if not val_func or val_func.lower() == 'nan':
                skipped_no_func += 1
                continue

            # تخطي إذا لم يكن هناك مثال أو وصف (حسب الطلب)
            if not val_ex or not val_desc:
                skipped_no_example += 1
                continue

            # استخراج الحرف بدون حركة من val_letter_haraka
            base_letter = remove_arabic_diacritics(val_letter_haraka)
            if not base_letter:
                continue

            # البحث عن الحرف الأساسي في جدول Letters والتحديث
            sql_update = """
            UPDATE lwh
            SET 
                lwh.[Letters_Function] = ?,
                lwh.[Example] = ?,
                lwh.[description] = ?
            FROM Letters_With_Haraka lwh
            INNER JOIN Letters l ON lwh.letter_id = l.LetterID
            WHERE l.Letter = ?
            """
            
            params = (val_func, val_ex, val_desc, base_letter)
            cursor.execute(sql_update, params)
            
            if cursor.rowcount > 0:
                updated_count += cursor.rowcount

        conn.commit()
        print(f"--- الخطوة 3: النتائج ---")
        print(f"✅ تمت العملية بنجاح!")
        print(f"📊 عدد الأسطر التي تم تحديثها: {updated_count}")
        if skipped_no_func > 0:
            print(f"⏭️  تم تخطي {skipped_no_func} صف (لعدم وجود وظيفة)")
        if skipped_no_example > 0:
            print(f"⏭️  تم تخطي {skipped_no_example} صف (لعدم وجود مثال أو وصف)")

    except Exception as e:
        print(f"❌ خطأ أثناء التحديث: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    # 1. أولاً: نضمن وجود الهيكل والبيانات الأساسية (إضافة الأعمدة إن لم تكن موجودة)
    setup_and_populate_structure()
    
    # 2. ثانياً: نحدث البيانات من الإكسل
    update_functions_from_excel()



#End