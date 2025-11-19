import pyodbc
import sys
import json
import pandas as pd
from datetime import datetime
import os

# --- معلومات الاتصال ---
server = 'LAPTOP-QPC9F0C5'
database = 'Arabic_Project'

# مسار ملف الإكسل
excel_file_path = r"C:\Users\User\Downloads\Arabic-DB-Project\data\classified_combinations001.xlsx"

connection_string = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

connection = None
cursor = None

# --- دالة مساعدة لتحميل بيانات الإكسل ---
def load_excel_data(file_path):
    print(f"\n...جارٍ قراءة ملف الإكسل من المسار:\n{file_path}")
    try:
        # قراءة الملف
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        # تنظيف أسماء الأعمدة
        df.columns = df.columns.str.strip()
        
        # 🔴🔴 (تعديل) تم تغيير اسم العمود المتوقع هنا ليطابق ملفك 🔴🔴
        # كان 'combination_word' وأصبح 'combination'
        required_cols = ['combination', 'meaning', 'classification']
        
        # التحقق من وجود الأعمدة
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"⚠️ تحذير: الأعمدة التالية مفقودة في ملف الإكسل: {missing_cols}")
            print(f"الأعمدة الموجودة هي: {list(df.columns)}")
            return {}

        # تحويل البيانات إلى قاموس
        lookup = {}
        for _, row in df.iterrows():
            # 🔴🔴 (تعديل) قراءة العمود بالاسم الصحيح combination 🔴🔴
            word = str(row['combination']).strip() 
            
            meaning = row['meaning'] if pd.notna(row['meaning']) else None
            classification = row['classification'] if pd.notna(row['classification']) else None
            
            lookup[word] = {
                'meaning': meaning,
                'classification': classification
            }
        
        print(f"✅ تم تحميل {len(lookup)} كلمة مصنفة من ملف الإكسل.")
        return lookup

    except FileNotFoundError:
        print(f"❌ خطأ: ملف الإكسل غير موجود في المسار المحدد:\n{file_path}")
        return {}
    except Exception as e:
        print(f"❌ خطأ أثناء قراءة ملف الإكسل: {e}")
        return {}

try:
    # --- الاتصال بقاعدة البيانات ---
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print(f"✅ تم الاتصال بقاعدة البيانات '{database}' بنجاح!")

    # --- تحميل بيانات الإكسل ---
    excel_lookup_data = load_excel_data(excel_file_path)

    # --- إنشاء الجدول ---
    print("\n...جارٍ التحقق من وجود جدول L28_letter_combinations أو إنشائه...")
    create_table_query = """
    IF NOT EXISTS (
        SELECT * FROM sysobjects 
        WHERE name='L28_letter_combinations' AND xtype='U'
    )
    CREATE TABLE L28_letter_combinations(
        id INT,
        LetterId INT FOREIGN KEY REFERENCES Letters(LetterID),
        combination_word NVARCHAR(50),  
        meaning NVARCHAR(MAX),          
        classification NVARCHAR(255)    
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("✅ تم إنشاء الجدول (أو التحقق منه).")

    # --- جلب الحروف ---
    print("\n...جارٍ جلب الحروف من جدول 'Letters'...")
    arabic_letters_data = [] 
    
    try:
        cursor.execute("SELECT LetterID, Letter FROM Letters ORDER BY LetterID")
        arabic_letters_data = cursor.fetchall()
        
        if not arabic_letters_data:
            raise Exception("⚠️ لم يتم العثور على أي حروف في جدول 'Letters'.")
        
        print(f"✅ تم جلب {len(arabic_letters_data)} حرف بنجاح.")
        
    except pyodbc.Error as select_error:
        print(f"❌ خطأ في جلب البيانات: {select_error}")
        sys.exit(1)

    # --- تنظيف الجدول القديم ---
    print("...جارٍ تنظيف جدول 'L28_letter_combinations'...")
    cursor.execute("DELETE FROM L28_letter_combinations") 
    connection.commit()

    # --- توليد التوافيق ودمجها مع بيانات الإكسل ---
    data_to_insert = []
    print(f"\n...جارٍ توليد التوافيق ودمج البيانات من الإكسل...")

    combinations_count = 0

    for i, (first_letter_id, first_letter) in enumerate(arabic_letters_data):
        for j, (second_letter_id, second_letter) in enumerate(arabic_letters_data):

            # تكوين الكلمة
            new_word = first_letter + second_letter
            
            # البحث في الإكسل
            meaning_val = None
            classification_val = None

            if new_word in excel_lookup_data:
                meaning_val = excel_lookup_data[new_word]['meaning']
                classification_val = excel_lookup_data[new_word]['classification']

            data_to_insert.append((
                first_letter_id,  
                new_word,
                meaning_val,      
                classification_val 
            ))
            
            combinations_count += 1

    print(f"📊 عدد التوافيق: {combinations_count}")
    
    # --- إدراج البيانات ---
    if data_to_insert:
        print("...جارٍ إدراج البيانات في SQL Server...")
        
        insert_query = """
        INSERT INTO L28_letter_combinations (id, LetterId, combination_word, meaning, classification)
        VALUES (?, ?, ?, ?, ?)
        """
        
        final_insert_list = []
        for idx, (lid, word, mean, clss) in enumerate(data_to_insert):
            final_insert_list.append((
                idx + 1, 
                lid,
                word,
                mean,
                clss
            ))

        try:
            cursor.fast_executemany = True 
            cursor.executemany(insert_query, final_insert_list)
            connection.commit()
            print(f"🎉 نجاح! تم إدراج {len(final_insert_list)} صف.")
        except Exception as db_error:
            print(f"❌ خطأ في الإدراج السريع: {db_error}")
            try:
                cursor.fast_executemany = False
                cursor.executemany(insert_query, final_insert_list)
                connection.commit()
                print("تم الإدراج بالمحاولة الثانية.")
            except Exception as e2:
                 print(f"❌ فشلت المحاولة الثانية: {e2}")

    # --- عرض عينة للتأكد ---
    print(f"\n📝 فحص عينة للبيانات التي تم إدخالها (التي لها معنى):")
    cursor.execute("SELECT TOP 5 combination_word, meaning, classification FROM L28_letter_combinations WHERE meaning IS NOT NULL")
    rows = cursor.fetchall()
    if rows:
        for r in rows:
            print(f" - الكلمة: {r[0]} | المعنى: {r[1]} | التصنيف: {r[2]}")
    else:
        print("لم يتم العثور على كلمات لها معنى في العينة.")

except Exception as e:
    print(f"❌ حدث خطأ غير متوقع: {e}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("✅ تم إغلاق الاتصال.")

#End