def letter_value(letter):
  num = ord(letter)
  if 1488 <= num <= 1497:    
    return num - 1487
  if 1511 <= num <= 1514:    
    return (num - 1510) * 100
  other_values = [20,20,30,40,40,50,50,60,70,80,80,90,90]
  return other_values[num-1498]

def gimatria(word):
  num = 0
  for i in word:
    if 1488 <= ord(i) <= 1514:
      num += letter_value(i)
  return num

def number_to_hebrew(num):
  word=''
  if num >= 1000:
    return number_to_hebrew(num//1000) + "'" + number_to_hebrew(num%1000)
  while num >=400:
    word+='ת'
    num-=400
  values = [20,20,30,40,40,50,50,60,70,80,80,90,90,100,200,300]
  for i in range(len(values)):
    if num >=values[-i-1]:
      word+=chr(1513-i)
      num-=values[-i-1]
  for i in range(10,0,-1):
    if num >=i:
      word +=chr(i+1487)
      num -=i
  word = word.replace("יה", "טו")
  word = word.replace("יו", "טז")
  if len(word) > 1:
    return word[:-1]+'"'+word[-1] 
  return word 

def hebrew_year_to_number(word, deafault_value = 0):
  if len(word) == 0:
    return deafault_value 
  if len(word) > 1 and 1488 <= ord(word[0]) <= 1497:
    num = 1000 * letter_value(word[0])
    word = word[1:]
  else:
    num = 5000
  return num + gimatria(word)

