import re

def normalize_phone(digits: str) -> str:
    """Привести к 11 цифрам, начинающимся с 7, или вернуть '' если невалидно."""
    digits = re.sub(r"\D", "", digits)
    if not digits:
        return ""
    if len(digits) == 11 and digits.startswith("8"):
        digits = "7" + digits[1:]
    elif len(digits) == 11 and digits.startswith("7"):
        pass
    elif len(digits) == 10:
        # например "9872588333" -> "79872588333"
        digits = "7" + digits
    else:
        return ""
    return digits

def extract_phones_from_line(line: str) -> list:
    """
    Из строки возвращает список нормализованных телефонных кандидатів,
    пытаясь склеивать соседние группы цифр (напр. '+7 987 258-83-33').
    """
    result = []
    # кандидаты — последовательности только из цифр, +, скобок, пробелов, дефисов и т.п.
    candidates = re.findall(r"[+\d\(\)\s\-\.\u2013/]{5,}", line)
    for cand in candidates:
        groups = re.findall(r"\d+", cand)
        i = 0
        while i < len(groups):
            found = None
            # ищем минимальную последовательность groups[i..k] такую, что длина 10..11
            for k in range(i, len(groups)):
                comb = "".join(groups[i:k+1])
                if 10 <= len(comb) <= 11:
                    found = comb
                    i = k + 1
                    break
                if len(comb) > 11:
                    break
            if not found:
                # если не нашли комбинируя, попробуем взять одиночную группу, если она подходит
                grp = groups[i]
                if 10 <= len(grp) <= 11:
                    found = grp
                i += 1
            if found:
                norm = normalize_phone(found)
                if norm:
                    result.append(norm)
    return result

def process_file(inp="input.txt", out="output.txt"):
    phones = []
    seen = set()
    with open(inp, "r", encoding="utf-8") as f:
        for line in f:
            for phone in extract_phones_from_line(line):
                if phone not in seen:
                    phones.append(phone)
                    seen.add(phone)
    with open(out, "w", encoding="utf-8") as f:
        for p in phones:
            f.write(p + "\n")
    print(f"Got {len(phones)} phones -> saved to {out}")

if __name__ == "__main__":
    process_file("input.txt", "output.txt")
