import datetime

from block import Block

STRP_TIME_STR = '%b-%d-%Y %I:%M:%S %p +%Z'

def convert_block_infos_to_blocks(block_infos):
  #set up array of actual blocks
  blocks = []
  for number, timestamp_str, difficulty_str, uncle in block_infos:
    difficulty = int(difficulty_str.replace(',',''))
    timestamp = int(datetime.datetime.strptime(timestamp_str, STRP_TIME_STR).strftime('%s'))
    next_block = Block(number, timestamp, difficulty, uncle)
    blocks.append(next_block)
  return blocks

frontier_block_infos = [
      (1500000, 'May-11-2016 09:45:33 PM +UTC', '34,982,465,665,323', None),
      (1500001, 'May-11-2016 09:46:17 PM +UTC', '34,931,221,827,326', None),
      (1500002, 'May-11-2016 09:46:28 PM +UTC', '34,931,221,835,518', None),
      (1500003, 'May-11-2016 09:46:31 PM +UTC', '34,948,278,104,371', None),
      (1500004, 'May-11-2016 09:46:41 PM +UTC', '34,948,278,112,563', None),
]


frontier_blocks = convert_block_infos_to_blocks(frontier_block_infos)


homestead_block_infos = [
    (4150000, 'Aug-12-2017 09:14:36 PM +UTC', '1,711,391,947,807,191', None),
    (4150001, 'Aug-12-2017 09:14:47 PM +UTC', '1,711,941,703,621,079', None),
    (4150002, 'Aug-12-2017 09:15:08 PM +UTC', '1,711,655,550,399,996', None),
    (4150003, 'Aug-12-2017 09:15:32 PM +UTC', '1,711,369,536,902,166', None),
    (4150004, 'Aug-12-2017 09:16:38 PM +UTC', '1,707,741,144,432,604', None),
]

homestead_blocks = convert_block_infos_to_blocks(homestead_block_infos)


homestead_block_infos_2 = [
    (4250000, 'Sep-08-2017 01:31:55 AM +UTC', '2,297,313,428,231,280', None),
    (4250001, 'Sep-08-2017 01:32:02 AM +UTC', '2,299,534,674,931,434', None),
    (4250002, 'Sep-08-2017 01:32:03 AM +UTC', '2,301,757,006,224,703', None),
    (4250003, 'Sep-08-2017 01:33:07 AM +UTC', '2,297,236,993,911,504', None),
    (4250004, 'Sep-08-2017 01:33:28 AM +UTC', '2,297,214,807,788,347', None),
]

homestead_blocks_2 = convert_block_infos_to_blocks(homestead_block_infos_2)

homestead_block_infos_3 = [
    (4350000, 'Oct-09-2017 08:02:17 AM +UTC', '2,885,956,744,389,112', None),
    (4350001, 'Oct-09-2017 08:02:48 AM +UTC', '2,885,337,450,511,472', None),
    (4350002, 'Oct-09-2017 08:02:55 AM +UTC', '2,888,945,329,944,031', None),
    (4350003, 'Oct-09-2017 08:03:11 AM +UTC', '2,891,144,353,199,583', None),
    (4350004, 'Oct-09-2017 08:03:12 AM +UTC', '2,894,755,068,033,845', None),
]

homestead_blocks_3 = convert_block_infos_to_blocks(homestead_block_infos_3)


metropolis_block_infos = [
    (4546050, 'Nov-13-2017 05:06:21 PM +UTC', '1,436,507,601,685,486', None),
    (4546051, 'Nov-13-2017 05:06:25 PM +UTC', '1,437,209,021,421,063', None),
    (4546052, 'Nov-13-2017 05:06:41 PM +UTC', '1,437,209,021,429,255', None),
    (4546053, 'Nov-13-2017 05:06:44 PM +UTC', '1,437,910,783,654,941', True),
    (4546054, 'Nov-13-2017 05:07:08 PM +UTC', '1,437,910,783,663,133', None),
    (4546055, 'Nov-13-2017 05:07:24 PM +UTC', '1,437,910,783,671,325', None),
]

metropolis_blocks = convert_block_infos_to_blocks(metropolis_block_infos)

