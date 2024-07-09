from datetime import date, timedelta
from . import gimatria

months = ["תשרי", "חשוון", "כסלו", "טבת", "שבט", "אדר", "אדר א", "אדר ב", "ניסן", "אייר", "סיון", "תמוז", "אב", "אלול"]
full_months = ["תשרי", "חשוון", "כסלו", "שבט", "אדר א", "ניסן", "סיון", "אב"]
days_list = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י','יא','יב','יג','יד','טו','טז','יז','יח','יט','כ','כא','כב','כג','כד','כה','כו','כז','כח','כט','ל']
year_months ={"Pshuta": [None] + months[0:6] + months[8:], "Meuberet": [None] + months[0:5] + months[6:]}
months_order = {"תשרי" : 0, "חשוון" : 1, "כסלו" : 2, "טבת" : 3, "שבט" : 4, "אדר":-7, "אדר א":-8, "אדר ב":-7, "ניסן":-6, "אייר":-5, "סיון":-4, "תמוז":-3, "אב":-2, "אלול" : -1}
zero_point = {"Hebrew": [3762,1,1], "Calendar": date(1,9,6)}
  
def type_year (year): #type of the year: pshuta or meuberet
  y = "Pshuta"
  m = (0, 3, 6, 8, 11, 14, 17)
  if (year % 19) in m:
    y = "Meuberet"
  return y
	 
def years_since_0 (year): #how many years since year 0 to this year.
  mahzorim = year//19
  meubarot = 0
  pshutot = 0
  y = year % 19
  for i in range (1,y+1):
    if type_year(i) == "Pshuta":
      pshutot += 1
    else:
      meubarot += 1
  return mahzorim, pshutot, meubarot
	
def molad (year): 
  a,b,c = years_since_0 (year-1)
  parts_a = (a*595)+(b*876)+(c*589) + 204
  parts = parts_a % 1080
  hours_a = (parts_a // 1080) + (a*16)+(b*8)+(c*21) + 5
  hours = hours_a % 24
  days_a = (hours_a // 24) + (a*2)+(b*4)+(c*5) + 2
  days = days_a % 7
  return days, hours, parts
    
def fix (a):
  if a==0:
    a=7
  return a
    
def rosh_hashana (year):
  a,b,c = molad (year)
  rh = a
  if b>17:
    rh += 1
  if (rh == 1) or (rh == 4) or (rh == 6):
    rh += 1     
  if (type_year (year) == "Pshuta") and (a == 3) and (((b == 9) and (c>=204)) or (b>9)):
    rh = 5
  if (type_year (year-1) == "Meuberet") and (a == 2) and (((b == 15) and (c>=589)) or (b>15)):
    rh = 3
  return fix(rh)
    
def months_in_year (year):
  if type_year(year) == "Pshuta":
    return 12
  else:
    return 13

def days_year (year):
  if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    return 366
  else:
    return 365

def days_month (month,year):
  if month in [4,6,9,11]:
    return 30
  elif month == 2:
    if days_year(year) == 366:
      return 29
    else:
      return 28
  else:
    return 31

def days_heb_year (year):
  rh = rosh_hashana(year)
  rh2 = rosh_hashana(year + 1)
  if type_year(year) == "Meuberet":
    if rh == rh2:
      return 385
    else:
      return 378 + ((rh2-rh) % 7)
  else:
    return 350 + ((rh2 - rh) % 7)

def days_heb_month (month, year):
  if month == 2:
    if days_heb_year(year) in (355,385):
      return 30
    else:
      return 29
  elif month == 3:
    if days_heb_year(year) in (353,383):
      return 29
    else:
      return 30
  elif type_year(year) == "Meuberet" and month > 5:
    return 30 - (month % 2)
  else:
    return 29 + (month % 2)

def days_since_zero (year,month,day):
  cnt = 0
  for i in range (zero_point["Hebrew"][0],year):
    cnt += days_heb_year(i)
  for i in range (1,month):
    cnt += days_heb_month(i,year)
  cnt += day - 1
  return cnt

def format_hebrew_date(list):
  year,month,day = list
  return ' '.join([days_list[day-1],year_months[type_year(year)][month],gimatria.number_to_hebrew(year)])

def hebrew_date_plus_num (number, date=zero_point["Hebrew"]): 
  year,month,day = date
  while number >= days_heb_year(year):
    number -= days_heb_year(year)
    year += 1
  while number >= days_heb_month(month,year):
    number -= days_heb_month(month,year)
    if month < months_in_year(year):
      month += 1
    else:
      month = 1
      year += 1
  while number > 0:
    number -= 1
    if day < days_heb_month(month, year):
      day += 1
    elif month < months_in_year(year):
      day = 1
      month += 1
    else:
      day, month = 1, 1
      year += 1
  return [year,month,day]
 


def get_calendar_date (day,month_name,year):
  month = year_months[type_year(year)].index(month_name)        
  num = days_since_zero(year,month,day)
  return zero_point["Calendar"] + timedelta(days=num) 

def get_hebrew_date (year,month,day):
  num = (date(year,month,day) - zero_point["Calendar"]).days  
  return hebrew_date_plus_num(num)

def hebrew_today(numbers_view = False):
  date1 = date.today()
  str_date = str(date1)
  year = int(str_date[0:4])
  month = int (str_date[5:7])
  day = int (str_date[8:])
  return get_hebrew_date (year,month,day)

class hebrew_date:
  def __init__(self,day,month):
    self.day = day
    self.month = month
  
  def validation(self):
    if self.day not in range (30):
      return 1
    if self.month not in months:
      return 1
    if self.day == 29 and self.month not in full_months:
      return 1
    return 0
  
  def days_after_rh(self):    
    return (self.day + months_order[self.month]*29 + (months_order[self.month]+1)//2) % 7
  
  def possible_days(self):
    hebrew_days = []
    days_to_add = self.day
    if self.month == 'כסלו':
      days = [1,2,3,4,5,6]
    elif self.month == "טבת":
      days = [1,2,3,4,6]
    elif self.month == "שבט":
      days = [2,3,4,5,7]
    elif self.month == "חשוון" and self.day == 29:
      days = [2,5,7]
      days_to_add = self.days_after_rh()
    else:
      days = [2,3,5,7]
      days_to_add = self.days_after_rh()
      
    for i in range(len(days)):
      days[i] = (days[i] + days_to_add) % 7
      if days[i] == 0:
        days[i] = 7
      hebrew_days.append(days_list[days[i]-1])
    return sorted(hebrew_days)