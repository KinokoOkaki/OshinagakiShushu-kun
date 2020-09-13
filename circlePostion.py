import re
import emoji

def circlePosition(name):
    #月曜日西地区 "あ"　57a
    
    #正規表現で日にちと場所と方角に分ける
    element = remove_emoji(name)
    element = zenhan(element)
    element = element.replace("97", "")
    element = re.sub('["”　‐\\-\\s]', '', element)
    print("element:"+str(element))
    #南西が記入されている場合
    tmp = re.findall('([月火水木金土日一二三四五六七八九１２３４５６７８９0-9]).*?([南西]).*?([ぁ-んーァ-ヶーa-zA-ZＡ-Ｚａ-ｚ].*?[\d０１２３４５６７８９]{1,2}.*?[あbABa]{1,2}).*?\Z', element)
    print(tmp)
    if(tmp == []):
        sep=None
    else:
        sep=tmp[0]
    print("sep:"+str(sep))
    if(not sep == None):
        print(sep)
        date = sep[0]
        direction = sep[1]
        place = sep[2]
    
    #南西が記入されていない場合(多分精度落ちてる)
    else:
        date = re.match('[月火水木金土]', element)
        if(not re.match('日曜',element) == None):
            date = "日"
        elif(not re.match('[0-9１２２３４５６７８９]日目', element) == None):
            date = element.match('([0-9１２２３４５６７８９])日目')
            date = date[1]
    
    #date = element.match(/[0-9月火水木金土日一二三四五六七八九１２３４５６７８９]/)
        direction =  re.match('[南西]',element) if re.match('[南西]',element) else None
        place = re.match('^.*?[0-9１２３４５６７８９０月火水木金土(日曜)].*?([ぁ-んーァ-ヶーa-zA-ZＡ-Ｚａ-ｚ].*?[\d１２３４５６７８９]:1,2.*?[あbABa]:1,2).*?$',element)
        if(not place == None):
            place=place[1]
    
    print("direction:"+str(direction))
    print("date:"+str(date))
    print("place:"+str(place))

    
    #何も見つけられない場合無視
    if(direction == None and (date== None or date == None) and (place == None or place == None)):
        return ["Not Found"]
    
    
    
    #日にちの表記ブレを修正
    if(not re.match('^[月火水木金土日一二三四五六七八九]',date) == None):
        if(date=="土"):
            date="1"
        elif(date == "日"):
            date = "2"
        elif(date == "月"):
            date = "3"
        elif(date == "火"):
            date = "4"
        elif(date == "一"):
            date = "1"
        elif(date == "二"):
            date = "2"
        elif(date == "三"):
            date = "3"
        elif(date == "四"):
            date = "4"
        elif(date == "五"):
            date = "5"
        elif(date == "六"):
            date = "6"
        elif(date == "七"):
            date = "7"
        elif(date == "八"):
            date = "8"
        elif(date == "九"):
            date = "9"
        else:
            date="error"
        
    
    

    #不要な文字の削除
    if(not place == None):
        place=place.replace('["”　\-\s]', "")
        #place=place.toString().replace(/^(?=.*[\u30e0-\u9fcf])(?.*[西南]).*$/g,"")
        place=place.replace('ブロック', "")
    else:
        place=""
    
    print("place:"+str(place))
        
    #西南が未記入の場合に予測する
    if(direction == "error" and ( place == None and  place == "")):
        code = place[0]
        if(("あ" <= code and 
            "れ" >= code) or 
            ("A" <= code and
            "R" >= code) or
            ("a" <= code and
            "r" >= code)):
                direction = "西"
        elif("ア" <= code and
            "リ" >= code):
            direction = "南"
        else:
            direction="error"
            
        
        
        
    #abの表記ブレを修正
    if(not re.match('[あ]$',direction) == None):
        direction = direction.replace('[あ]$',"a")
    
        
    print("direction:"+direction)
    print("date:"+date)
    print("place:"+place)

    return [date+"日目", direction, place]

def zenhan(a):
    b = a.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    return b

def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)
