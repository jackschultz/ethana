class Block():
  def __init__(self, number, timestamp, difficulty, uncles=None):
    self.number = number
    self.timestamp = timestamp
    self.difficulty = difficulty
    self.uncles = uncles
