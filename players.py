''' 

makes players for whats the time mr wolf game.

'''
import random

class wolf:
  '''
  wolf player 
  
  init values:
  x
  y
  speed
  min time
  max time
  dinner time chance
  '''

  def __init__(self, x, y, speed, min, max, dinnerChance):
    self.x = x
    self.y = y
    self.speed = speed
    self.min = min
    self.max = max
    self.dinnerChance = dinnerChance
    self.dinnerTime = False

  def time(self):
    ''' 
    finds a new time
    '''
    
    # checks if dinner time 
    if random.randrange(0, 1) < self.dinnerChance:
      self.dinnerTime = True
      return True
    else:
      return random.randint(self.min, self.max) # sets new time based on min and max

class pig:
  '''
  pig player 
  
  init values:
  x
  y
  speed
  name 
  '''

  def __init__(self, x, y, speed, name):
    self.x = x
    self.y = y
    self.speed = speed
    self.name = name

  def time(self):
    ''' 
    finds a new time
    '''
    
    # checks if dinner time 
    if random.randrange(0, 1) < self.dinnerChance:
      self.dinnerTime = True
      return True
    else:
      return random.randint(self.min, self.max) # sets new time based on min and max

