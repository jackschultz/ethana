import datetime
import rlp
from block import Block

import sha3 as _sha3

def sha3_256(x): return _sha3.keccak_256(x).digest()

def to_string(value):
  return str(value)

def sha3(seed):
  return sha3_256(to_string(seed))

config = dict(
    DIFF_ADJUSTMENT_CUTOFF=13,
    BLOCK_DIFF_FACTOR=2048,
    # Exponential difficulty timebomb period
    EXPDIFF_PERIOD=100000,
    EXPDIFF_FREE_PERIODS=2,
    # Homestead fork
    HOMESTEAD_FORK_BLKNUM=1150000,
    HOMESTEAD_DIFF_ADJUSTMENT_CUTOFF=10,
    # Metropolis fork
    METROPOLIS_DELAY_PERIODS=30,
    METROPOLIS_FORK_BLKNUM=4370000,
    METROPOLIS_DIFF_ADJUSTMENT_CUTOFF=9,
)

##Frontier

def calc_frontier_offset(parent_difficulty):
  offset = parent_difficulty // config['BLOCK_DIFF_FACTOR']
  return offset

def calc_frontier_sign(parent, child_timestamp):
  parent_timestamp = parent.timestamp
  time_diff = child_timestamp - parent_timestamp
  if time_diff < config['DIFF_ADJUSTMENT_CUTOFF']:
    sign = 1
  else:
    sign = -1
  return sign

def calc_frontier_bomb(parent_number):
  period_count = (parent.number + 1) // config['EXPDIFF_PERIOD']
  period_count -= config['EXPDIFF_FREE_PERIODS']
  bomb = 2**(period_count)
  return bomb

def calc_frontier_difficulty(parent, child_timestamp):
  offset = calc_frontier_offset(parent.difficulty)
  sign = calc_frontier_sign(parent.timestamp, child_timestamp)
  bomb = calc_frontier_bomb(parent.number)
  target = (parent.difficulty + offset * sign) + bomb
  return offset, sign, bomb, target


##Homestead

def calc_homestead_offset(parent_difficulty):
  offset = parent_difficulty // config['BLOCK_DIFF_FACTOR']
  return offset

def calc_homestead_sign(parent, child_timestamp):
  parent_timestamp = parent.timestamp
  time_diff = child_timestamp - parent_timestamp
  sign = 1 - (time_diff // config['HOMESTEAD_DIFF_ADJUSTMENT_CUTOFF'])
  return sign

def calc_homestead_bomb(parent_number):
  period_count = (parent_number + 1) // config['EXPDIFF_PERIOD']
  period_count -= config['EXPDIFF_FREE_PERIODS']
  bomb = 2**(period_count)
  return bomb

def calc_homestead_difficulty(parent, child_timestamp):
  offset = calc_homestead_offset(parent.difficulty)
  sign = calc_homestead_sign(parent, child_timestamp)
  bomb = calc_homestead_bomb(parent.number)
  target = (parent.difficulty + offset * sign) + bomb
  return offset, sign, bomb, target



## Metropolis

def calc_metropolis_offset(parent_difficulty):
  offset = parent_difficulty // config['BLOCK_DIFF_FACTOR']
  return offset

def calc_metropolis_sign(parent, child_timestamp):
  parent_timestamp = parent.timestamp
  if parent.uncles:
    uncles = 2
  else:
    uncles = 1
  time_diff = child_timestamp - parent_timestamp
  sign = uncles - (time_diff // config['METROPOLIS_DIFF_ADJUSTMENT_CUTOFF'])
  return sign

def calc_metropolis_bomb(parent_number):
  period_count = (parent_number + 1) // config['EXPDIFF_PERIOD']
  period_count -= config['METROPOLIS_DELAY_PERIODS'] #chop off 30, meaning go back 3M blocks in time
  period_count -= config['EXPDIFF_FREE_PERIODS'] #chop off 2 more for good measure
  bomb = 2**(period_count)
  return bomb

def calc_metropolis_difficulty(parent, child_timestamp):
  offset = calc_metropolis_offset(parent.difficulty)
  sign = calc_metropolis_sign(parent, child_timestamp)
  bomb = calc_metropolis_bomb(parent.number)
  target = (parent.difficulty + offset * sign) + bomb
  return offset, sign, bomb, target

##Overall difficulty calculating

def calc_difficulty(parent, child_timestamp):
  if parent.number > config['METROPOLIS_FORK_BLKNUM']:
    return calc_metropolis_difficulty(parent, child_timestamp)
  elif parent.number > config['HOMESTEAD_FORK_BLKNUM']:
    return calc_homestead_difficulty(parent, child_timestamp)
  else:
    return calc_frontier_difficulty(parent, child_timestamp)

def verify_difficulties(blocks):
  for index, child_block in enumerate(blocks[1:]):
    print 'Finding difficulty of block %s' % child_block.number
    parent_block = blocks[index]
    offset, sign, bomb, target = calc_difficulty(parent_block, child_block.timestamp)
    print 'Parent difficulty: %s' % parent_block.difficulty
    print 'Calc difficulty:   %s' % int(target)
    print 'Child difficulty:  %s' % child_block.difficulty

    #want to show offset, bomb, bomb / float(offset) to show how much the bomb changes time
    print 'Offset:            %s' % offset
    print 'Bomb:              %s' % bomb
    print 'Bomb / Offset:     %s' % (bomb / float(offset))
    print

    assert target == child_block.difficulty

def calc_mining_time(block_number, difficulty, actual_average_mining_time, calc_bomb, calc_offset):
  homestead_goal_mining_time = 14.5 #about that.
  bomb = calc_bomb(block_number)
  offset = calc_offset(difficulty)
  bomb_offset_ratio = bomb / float(offset)
  seconds_adjustment = bomb_offset_ratio * config['HOMESTEAD_DIFF_ADJUSTMENT_CUTOFF']
  average_mining_time = 0.4 * 60
  calculated_average_mining_time = homestead_goal_mining_time + seconds_adjustment
  print "Bomb: %s" % bomb
  print "Offset: %s" % offset
  print "Bomb Offset Ratio: %s" % bomb_offset_ratio
  print "Seconds Adjustment: %s" % seconds_adjustment
  print "Actual Avg Mining Time: %s" % actual_average_mining_time
  print "Calculated Mining Time: %s" % calculated_average_mining_time
  print

if __name__ == '__main__':

  from data import frontier_blocks, homestead_blocks, homestead_blocks_2, homestead_blocks_3, metropolis_blocks

  verify_difficulties(frontier_blocks)
  verify_difficulties(homestead_blocks)
  verify_difficulties(homestead_blocks_2)
  verify_difficulties(homestead_blocks_3)
  verify_difficulties(metropolis_blocks)

  block_number = 4150000
  difficulty = 1711391947807191
  actual_average_mining_time = 0.35 * 60
  calc_mining_time(block_number, difficulty, actual_average_mining_time, calc_homestead_bomb, calc_homestead_offset)

  block_number = 4250000
  difficulty = 2297313428231280
  actual_average_mining_time = 0.4 * 60
  calc_mining_time(block_number, difficulty, actual_average_mining_time, calc_homestead_bomb, calc_homestead_offset)

  block_number = 4350000
  difficulty = 2885956744389112
  actual_average_mining_time = 0.5 * 60
  calc_mining_time(block_number, difficulty, actual_average_mining_time, calc_homestead_bomb, calc_homestead_offset)

  block_number = 4546050
  difficulty = 1436507601685486
  actual_average_mining_time = 0.23 * 60
  calc_mining_time(block_number, difficulty, actual_average_mining_time, calc_metropolis_bomb, calc_metropolis_offset)
