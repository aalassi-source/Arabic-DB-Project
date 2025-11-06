# -*- coding: utf-8 -*-
import re
import sys
import io

# Ensure UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def analyze_cv(word):
    chars = list(str(word).strip())
    pattern = ''
    fatha, kasrah, damma = 'َ', 'ِ', 'ُ'
    tanween = ['ً', 'ٍ', 'ٌ']
    sukun = 'ْ'
    shadda = 'ّ'
    long_vows_fixed = ['ى', 'آ']

    def prev_haraka(idx):
        k = idx - 1
        while k >= 0:
            ch = chars[k]
            if ch in (fatha, kasrah, damma):
                return ch
            if ch in tanween:
                return {'ً': fatha, 'ٍ': kasrah, 'ٌ': damma}[ch]
            k -= 1
        return None

    i = 0
    while i < len(chars):
        ch = chars[i]
        nxt = chars[i+1] if i+1 < len(chars) else None

        if ch == sukun:
            i += 1
            continue

        if ch in tanween:
            pattern += 'VC'
            i += 1
            if i < len(chars) and chars[i] == 'ا':
                i += 1
            continue

        if ch == shadda:
            pattern += 'C'
            i += 1
            continue

        if ch == fatha:
            pattern += 'VA'
            i += 1
            continue

        if ch == kasrah:
            pattern += 'VK'
            i += 1
            continue

        if ch == damma:
            pattern += 'VD'
            i += 1
            continue

        if ch in long_vows_fixed:
            pattern += 'V'
            i += 1
            continue

        if ch == 'ا':
            if nxt in (fatha, kasrah, damma):
                pattern += 'C'
            else:
                ph = prev_haraka(i)
                pattern += 'V' if ph == fatha else 'C'
            i += 1
            continue

        if ch == 'و':
            if nxt in (fatha, kasrah, damma):
                pattern += 'C'
            else:
                ph = prev_haraka(i)
                pattern += 'V' if ph == damma else 'C'
            i += 1
            continue

        if ch == 'ي':
            if nxt in (fatha, kasrah, damma):
                pattern += 'C'
            else:
                ph = prev_haraka(i)
                pattern += 'V' if ph == kasrah else 'C'
            i += 1
            continue

        if re.match(r'[\u0600-\u06FF]', ch):
            if nxt == shadda:
                pattern += 'CC'
                i += 2
                continue
            pattern += 'C'
            i += 1
            continue

        i += 1

    return pattern

def main():
    print("\nArabic Word CV Pattern Analyzer")
    print("Enter 'q' or press Ctrl+C to quit")
    print("-" * 40)

    while True:
        try:
            print("\nEnter an Arabic word (with diacritics):")
            word = input().strip()
            
            if word.lower() == 'q':
                print("Goodbye!")
                break
                
            if not word:
                print("Please enter a word")
                continue

            print(f"\nAnalyzing: {word}")
            pattern = analyze_cv(word)
            print(f"CV Pattern: {pattern}")
            print(f"Pattern length: {len(pattern)}")
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error processing word: {str(e)}")
            print("-" * 40)

if __name__ == '__main__':
    main()