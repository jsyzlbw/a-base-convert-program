#general idea
#1.get an input, deal with the sign(+/-),break up the integer 
#part and the fraction part
#2. examine whether the input is valid
#3.deal with the integer part
#4.deal with the fraction part
#5.formated output
#let's break up into functions
#(1)char_to_value(c)/value_to_char(v):char<->value
#(2)parse_number(num_str):break it into: sign+int+frac
#(3)validate_digits(s,base): check whether each digit is valid
#(4)integer_str_to_int(int_str, base):turn the int_str into dec
#(5)fraction_str_to_int(int_str,base):turn the frac_str into dec
#(6)int_to_base(n,base):turn int part into the target base
#(7)fraction_to_base():turn the frac part into the target base
#(8)convert_base: the main function


from fractions import Fraction #allow us to have fractions
from typing import Tuple, Optional #make the code easier to read

#--basic tools--
def char_to_value(c: str) -> int : #change the letter into the number
    c = c.strip()#strip(func): delete the blankspace on the left and the right(including \n, \t)
    if not c :
        raise ValueError("Empty digit")
    if c.isdigit() :
        return ord(c) - ord("0")
    uc = c.upper()
    if "A" <= uc <= "Z":
        return ord(uc) - ord("A") + 10#change the letter into the number
    raise ValueError(f"Invalid digit charter: {c}")

def value_to_char(v:int) -> str:#change the number into the letter
    if v<0 or v >= 36:
        raise ValueError("value_to_char support 0-35")
    if v < 10:
        return str(v)
    return chr(ord("A")+v-10)

#--deal with the number--
def parse_number(num_str: str) ->Tuple[int, str, str]:
    s = num_str.strip()
    if not s:#check whether the input is empty
        raise ValueError("Empty imput")
    #deal with the sign
    sign = 1
    if s[0] in "+-":
        if s[0] == "-":
            sign = -1
        s = s[1:]
    if "." in s:
        integer_str, fraction_str = s.split(".", 1)
    else:
        integer_str, fraction_str = s, ""
    return sign, integer_str, fraction_str

def validate_digits(s: str , base: int):#check whether the input is in the valid range
    for ch in s:
        v = char_to_value(ch)
        if v >= base:
            raise ValueError(f"Digit {ch} out of range for base {base}")
        
#--change into dec-------------------------------------------------------------------------------
def integer_str_to_int(int_str: str, base: int) -> int:
    val = 0
    for ch in int_str:
        val = val * base + char_to_value(ch)
    return val

def fraction_str_to_frac(frac_str: str, base: int) -> Fraction:
    if not frac_str:
        return Fraction(0, 1)
    numerator = 0
    for ch in frac_str:
        numerator = numerator * base + char_to_value(ch)
    denom = base ** len(frac_str)
    return Fraction(numerator, denom)#Fraction(,) will simplify it automatically
#--------------------------------------------------------------------------------------------------

#--dec->the target base----------------------------------------------------------------------------
def int_to_base(n: int, base: int) ->str :
    if n ==0 :#check whether the int part == 0
        return "0"
    digits=[] #construct a set to save each digit of the integer part
    while n > 0 :
        digits.append(value_to_char( n % base ))
        n //= base
    return "".join(reversed(digits))
def fraction_to_base(frac: Fraction, base: int, max_digits: int=50, detect_repeat:bool = True) -> Tuple[str, Optional[str]]:
    if frac == 0:#check whether the frac == 0
        return "", None
    numerator = frac.numerator#get the numerator and denominator
    denom = frac.denominator

    digits = [] #we construct a tuple to save each digit of the fraction part (in the target base)
    remainders = {} #we construct a dictionary to save the position of the remainder, to check when it begains to repeat
    #key = remainder, value = position
    pos = 0 #position, initially means the first digit of fraction
    remainder = numerator

    while numerator != 0 and pos < max_digits:
        #the first condition: if numerator == 0, means it's 0, a finite fraction, non-repeat
        #the second condition: if pos >= max_digit: save time and avoid infinite loop
        if detect_repeat and remainder in remainders:#check whether it repeats(if detect_repeat mode is on)
            start = remainders[remainder]#get the first position of the remainder appears
            non_repeat = "".join(digits[:start])#get the part that doesn't repeat
            repeat = "".join(digits[start:])#get the part that repeats
            if repeat == "0":
                return non_repeat, None
            else:
                return non_repeat, repeat# return two strings, stands for the repeat and non_repeat part
        #for example:
        #if we input: 0.1(6), it will return ("1","6")

        #if it hasn't repeat yet, execute the following code
        remainders[remainder] = pos#save the position
        remainder *= base
        digit = remainder // denom
        digits.append(value_to_char(digit))
        remainder = remainder % denom
        pos +=1
    return "".join(digits), None
    #for example: change (1/6)dec into bin
    #---initialization---
    #detect_repeat = True
    #base = 2
    #numerator = 1
    #demom = 6
    #remainder = numerator = 1
    #digits = [] empty tuple
    #remaindrs = {} empty dictionary
    #get into the while loop

    #---step 1---
    #in remainders? NO -> can't get into the first if loop
    #remianders[remainder=1] = 0 -> remainders={1:0}
    #remainder *= 2-->remainder = 2
    #digit = 2 // 6 = 0
    #digits = ["0"]
    #remainder = remainder % denom = 2 % 6 =2
    #pos=1

    #--step2--
    #remainder = 2  in remainders? No ->can't go into the first if loop
    #remainders[remainder=2] = 1 -> remainders = {1:0, 2:1}
    #remainder *= 2 -->remainder = 4
    #digit = 4 // 6 = 0
    #digits = ["0","0"]
    #remainder = remainder % denom = 4 % 6 = 4
    #pos = 2

    #--step3--
    #remainder = 4  in remainders? No ->can't go into the first if loop
    #remaiders[remainder=4] = 2 -> remainders = {1:0, 2:1, 4:2}
    #remainder *=2 -->remainder = 8
    #digit = 8//6 = 1
    #digits =["0","0","1"]
    #remainder = remainder % denom = 8 % 6 =2
    #pos = 3

    #--step4--
    #remainder = 2  in remainders? Yes!!! ->go into the first if loop
    #------------------------------------------------------------------
    #if detect_repeat and remainder in remainders:#check whether it repeats(if detect_repeat mode is on)
    #    start = remainders[remainder]#get the first position of the remainder appears
    #    non_repeat = "".join(digits[:start])#get the part that doesn't repeat
    #    repeat = "".join(digits[start:])#get the part that repeats
    #    return non_repeat, repeat# return two strings, stands for the repeat and non_repeat part
    #------------------------------------------------------------------
    #start = remainders[remainder] = remainders[2] = 1
    #non_repeat = "".join(digits[:1]) = "0"
    #repeat = "".join(digits[1:]) = "01"
    
#--the main convert function--------------------------------------------
def convert_base(num_str: str, base_from: int, base_to: int, max_frac_digits: int = 50, detect_repeat: bool = True) ->str:
    
    #check whether the base(from/to) is valid
    if not (2 <= base_from <= 36 and 2 <= base_to <= 36):
        raise ValueError("Base must be between 2 and 36")
    
    #get the three parts of the input number
    sign, integer_str, fraction_str = parse_number(num_str)

    #check whether the number is valid
    validate_digits(integer_str + fraction_str, base_from)

    #change string into dec value
    integer_value = integer_str_to_int(integer_str, base_from)
    fraction_value = fraction_str_to_frac(fraction_str, base_from)

    #change int(dec) part into the target base
    int_out = int_to_base(integer_value, base_to)
    
    #get the non_repeat and repeat part of the fraction part11.25
    non_repeat, repeat = fraction_to_base(fraction_value, base_to, max_digits = max_frac_digits, detect_repeat = detect_repeat)

    #check whether the fraction part is 0(safer than just write:frac_value == 0)
    #only have the int part
    if (non_repeat == "" ) and ( not repeat ) :
        result = int_out
    
    #have frac part
    else:
        frac_part = non_repeat
        if repeat:
            frac_part = frac_part + "(" + repeat + ")"
        result = int_out + "." + frac_part
    if sign < 0 and result != "0":
        result = "-" + result
    return result

#OK, now all the functions have been constructed
#get the input and print it out

ori_number = input("Enter the original number:")
base_from = int(input("Enter the original base(2-36):"))
base_to = int(input("Enter the base you want to convert into:"))
converted_number = convert_base(ori_number, base_from, base_to)
print(converted_number)