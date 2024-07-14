from datetime import date, timedelta
from . import gimatria

months = ["תשרי", "חשוון", "כסלו", "טבת", "שבט", "אדר", "אדר א", "אדר ב", "ניסן", "אייר", "סיון", "תמוז", "אב", "אלול"]
full_months = ["תשרי", "חשוון", "כסלו", "שבט", "אדר א", "ניסן", "סיון", "אב"]
days_list = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י','יא','יב','יג','יד','טו','טז','יז','יח','יט','כ','כא','כב','כג','כד','כה','כו','כז','כח','כט','ל']
year_months ={"Pshuta": [None] + months[0:6] + months[8:], "Meuberet": [None] + months[0:5] + months[6:]}
months_order = {"תשרי" : 0, "חשוון" : 1, "כסלו" : 2, "טבת" : 3, "שבט" : 4, "אדר":-7, "אדר א":-8, "אדר ב":-7, "ניסן":-6, "אייר":-5, "סיון":-4, "תמוז":-3, "אב":-2, "אלול" : -1}
zero_point = {"Hebrew": (3762,1,1), "Calendar": date(1,9,6)}
weekdays = ["שבת", "יום ראשון", "יום שני", "יום שלישי", "יום רביעי", "יום חמישי", "יום שישי"]
  
def type_year (year): #type of the year: pshuta or meuberet
  return "Meuberet" if (year % 19) in (0,3,6,8,11,14,17) else "Pshuta"
	 
def years_since_0 (year) -> tuple[int,int,int]: #how many years since year 0 to this year.
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
  parts_before_reduction = (a*595)+(b*876)+(c*589) + 204
  parts = parts_before_reduction % 1080
  hours_before_reduction = (parts_before_reduction // 1080) + (a*16)+(b*8)+(c*21) + 5
  hours = hours_before_reduction % 24
  days_before_reduction = (hours_before_reduction // 24) + (a*2)+(b*4)+(c*5) + 2
  days = days_before_reduction % 7
  return days, hours, parts
    
def fix (a):
  return 7 if a == 0 else a
    
def rosh_hashana (year):
  days,hours,parts = molad (year)
  rh = days
  if hours>=18:
    rh += 1
  if rh in (1,4,6):
    rh += 1     
  if (type_year (year) == "Pshuta") and (days == 3) and (((hours == 9) and (parts>=204)) or (hours>9)):
    return 5
  if (type_year (year-1) == "Meuberet") and (days == 2) and (((hours == 15) and (parts>=589)) or (hours>15)):
    return 3
  return fix(rh)
    
def months_in_year (year):
  return 12 if type_year(year) == "Pshuta" else 13

def days_year (year):
  return 366 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 365

def days_month (month,year):
  if month in [4,6,9,11]:
    return 30
  if month == 2:
    return 29 if days_year(year) == 366 else 28
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
  if month == 2 and days_heb_year(year) in (355,385):
    return 30
  if month == 3 and days_heb_year(year) in (353,383):
    return 29
  if type_year(year) == "Meuberet" and month > 5:
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

def format_hebrew_date(hebrew_date):
  year,month,day = hebrew_date
  return ' '.join([days_list[day-1],year_months[type_year(year)][month],gimatria.number_to_hebrew(year)])


class hebrew_date:
  def __init__(self,
               year:int, 
               month_number:int,
               day:int,
               month_name:str=""):
    self.day = day
    self.year = year
    if year == None and month_name !="":
      self.month_name = month_name
      self.month_number = months_order[month_name]
    else:
      self.month_name = year_months[type_year(year)][month_number]
      self.month_number = month_number
      self.list = [self.year,self.month_number,self.day]
      
  def __add__(self, number):
    year,month,day = self.year, self.month_number, self.day
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
    return hebrew_date(year=year,month_number=month,day=day)
    
  def validation(self):
    if self.day not in range (30):
      return 1
    if self.month_name not in months:
      return 1
    if self.day == 29 and self.month_name not in full_months:
      return 1
    if self.year != None:
      if self.year not in range (200000):
        return 1
      if self.month_name not in year_months[type_year(self.year)]:
        return 1
    return 0
  
  def weekday(self):
    day = rosh_hashana(self.year)
    for m in range (1,self.month_number):
      day += days_heb_month(m,self.year)
    day += self.day-1
    return day%7
  
  def strftime(self, string_date):
    string_date = string_date.replace("%y", str(self.year))
    string_date = string_date.replace("%Y", gimatria.number_to_hebrew(self.year))
    string_date = string_date.replace("%m", str(self.month_number))
    string_date = string_date.replace("%M", self.month_name)
    string_date = string_date.replace("%d", str(self.day))
    string_date = string_date.replace("%D", days_list[self.day-1])
    string_date = string_date.replace("%w", str(self.weekday()))
    string_date = string_date.replace("%A", weekdays[self.weekday()])
    return string_date
  
  def __str__(self) -> str:
    if self.validation() != 0:
      return "ERROR"
    if self.year == None:
      return self.strftime("%D %M")
    return self.strftime("%D %M %Y") 
  
  def days_after_rh(self):    
    return (self.day + months_order[self.month_name]*29 + (months_order[self.month_name]+1)//2) % 7
  
  def possible_days(self):
    hebrew_days = []
    days_to_add = self.day
    if self.month_number == 2:
      days = [1,2,3,4,5,6]
    elif self.month_number == 3:
      days = [1,2,3,4,6]
    elif self.month_number == 4:
      days = [2,3,4,5,7]
    elif self.month_number == 1 and self.day == 29:
      days = [2,5,7]
      days_to_add = self.days_after_rh()
    else:
      days = [2,3,5,7]
      days_to_add = self.days_after_rh()
      
    for i in range(len(days)):
      days[i] = fix((days[i] + days_to_add) % 7)
      hebrew_days.append(days_list[days[i]-1])
    return sorted(hebrew_days)
  


def get_calendar_date (day,month_name,year) -> date:
  month = year_months[type_year(year)].index(month_name)        
  delta = days_since_zero(year,month,day)
  return zero_point["Calendar"] + timedelta(days=delta) 

def get_hebrew_date (date: date) -> hebrew_date:
  delta = (date - zero_point["Calendar"]).days  
  zero_year, zero_month, zero_day = zero_point["Hebrew"]
  return hebrew_date(year=zero_year, month_number=zero_month, day=zero_day) + delta

def hebrew_today() -> hebrew_date:
  return get_hebrew_date (date.today())



  