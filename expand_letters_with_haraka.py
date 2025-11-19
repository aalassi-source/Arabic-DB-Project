import pyodbc
import pandas as pd

# ---- إعداد الاتصال ----
server = 'LAPTOP-QPC9F0C5'
database = 'Arabic_Project'
connection_string = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

def get_db_connection():
    return pyodbc.connect(connection_string)

def create_expanded_view():
    """
    هذه الدالة تقوم بـ:
    1. إنشاء عمود جديد يعرض الحرف مع الحركة (أو الحرف فقط إذا لم تكن هناك حركة)
    2. إظهار كل حرف مع كل الحركات المرتبطة به
    3. إذا لم تكن هناك حركات، إرجاع الحرف فقط مع NaN للبيانات الأخرى
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("--- الخطوة 1: التحقق من وجود العمود الجديد ---")
        
        # التحقق من وجود عمود letter_with_haraka
        check_col = """
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME='Letters_With_Haraka' AND COLUMN_NAME='letter_with_haraka'
        """
        cursor.execute(check_col)
        if not cursor.fetchone():
            print("جارٍ إضافة العمود [letter_with_haraka]...")
            alter_sql = """
            ALTER TABLE Letters_With_Haraka ADD [letter_with_haraka] NVARCHAR(MAX) NULL
            """
            cursor.execute(alter_sql)
            conn.commit()
            print("✅ تمت إضافة العمود بنجاح.")
        else:
            print("✅ العمود [letter_with_haraka] موجود بالفعل.")

        print("\n--- الخطوة 2: ملء العمود الجديد ---")
        
        # ملء العمود بالحرف + الحركة (إن وجدت)
        # في حال عدم وجود حركة، سيظهر الحرف فقط
        update_sql = """
        UPDATE lwh
        SET lwh.[letter_with_haraka] = 
            CASE 
                WHEN h.[Haraka] IS NOT NULL AND h.[Haraka] != '' 
                    THEN l.[Letter] + h.[Haraka]
                ELSE l.[Letter]
            END
        FROM Letters_With_Haraka lwh
        INNER JOIN Letters l ON lwh.letter_id = l.LetterID
        LEFT JOIN Haraka h ON lwh.haraka_id = h.id
        """
        
        cursor.execute(update_sql)
        rows_updated = cursor.rowcount
        conn.commit()
        print(f"✅ تم تحديث {rows_updated} صف بالحرف مع الحركة.")

        print("\n--- الخطوة 3: التحقق من النتائج ---")
        
        # عرض عينة من البيانات
        sample_sql = """
        SELECT TOP 10 
            lwh.id,
            lwh.letter_id,
            lwh.haraka_id,
            lwh.[letter_with_haraka],
            l.[Letter],
            h.[Haraka],
            lwh.[Letters_Function],
            lwh.[Example],
            lwh.[description]
        FROM Letters_With_Haraka lwh
        INNER JOIN Letters l ON lwh.letter_id = l.LetterID
        LEFT JOIN Haraka h ON lwh.haraka_id = h.id
        ORDER BY l.[Letter], h.id
        """
        
        cursor.execute(sample_sql)
        rows = cursor.fetchall()
        
        print("\nعينة من البيانات (أول 10 صفوف):")
        print("-" * 120)
        for row in rows:
            print(f"ID: {row.id} | letter_id: {row.letter_id} | haraka_id: {row.haraka_id} | "
                  f"Letter+Haraka: '{row.letter_with_haraka}' | "
                  f"Function: {row.Letters_Function or 'NaN'} | "
                  f"Example: {row.Example or 'NaN'} | "
                  f"Description: {row.description or 'NaN'}")
        print("-" * 120)

        print("\n--- الخطوة 4: إحصائيات عامة ---")
        
        # عرض إحصائيات
        stats_sql = """
        SELECT 
            COUNT(DISTINCT letter_id) AS عدد_الحروف_الفريدة,
            COUNT(*) AS إجمالي_الصفوف,
            COUNT(DISTINCT CASE WHEN [Letters_Function] IS NOT NULL THEN letter_id END) AS حروف_لها_وظيفة,
            COUNT(CASE WHEN [Letters_Function] IS NULL THEN 1 END) AS صفوف_بدون_وظيفة
        FROM Letters_With_Haraka
        """
        
        cursor.execute(stats_sql)
        stats = cursor.fetchone()
        
        print(f"عدد الحروف الفريدة: {stats[0]}")
        print(f"إجمالي الصفوف: {stats[1]}")
        print(f"حروف لها وظيفة: {stats[2]}")
        print(f"صفوف بدون وظيفة: {stats[3]}")

        print("\n✅ انتهت العملية بنجاح!")

    except Exception as e:
        print(f"❌ خطأ: {e}")
    finally:
        cursor.close()
        conn.close()

def ensure_all_letters_present():
    """
    هذه الدالة تتأكد من أن جميع الحروف موجودة في الجدول
    حتى لو لم تكن لها حركات مرتبطة
    (في هذه الحالة ستظهر مع NaN للحركة والبيانات)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("\n--- الخطوة 5: التأكد من وجود جميع الحروف ---")
        
        # الحصول على جميع الحروف التي ليست موجودة بعد
        insert_sql = """
        INSERT INTO Letters_With_Haraka (letter_id, haraka_id, letter_with_haraka)
        SELECT 
            l.LetterID,
            NULL,
            l.[Letter]
        FROM Letters l
        WHERE NOT EXISTS (
            SELECT 1 FROM Letters_With_Haraka lwh 
            WHERE lwh.letter_id = l.LetterID
        )
        """
        
        cursor.execute(insert_sql)
        rows_added = cursor.rowcount
        conn.commit()
        
        if rows_added > 0:
            print(f"✅ تمت إضافة {rows_added} حرف بدون حركات.")
        else:
            print("ℹ️ جميع الحروف موجودة بالفعل.")

    except Exception as e:
        print(f"❌ خطأ: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("=" * 120)
    print("برنامج توسيع جدول Letters_With_Haraka")
    print("=" * 120)
    
    # 1. أولاً: التأكد من وجود جميع الحروف (مع أو بدون حركات)
    ensure_all_letters_present()
    
    # 2. ثانياً: إنشاء العمود الجديد وملؤه
    create_expanded_view()
    
    print("\n" + "=" * 120)
    print("اكتمل البرنامج بنجاح!")
    print("=" * 120)


#End