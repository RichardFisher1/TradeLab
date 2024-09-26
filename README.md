# Trading-App

# DEALING WITH ADDING MUTIPLE SIGNALS ON SAME TIME AND ALSO FAULY BACKTESTER WHEN POSTIONS MOVE TO INTRADAY 
#    DATA_ITORATOR IS WRONG FOR DAILY BARS WHEN CHOSEN TIME IS NOT WHOLE DAY AS THE DAILY DAILY DATABASE DOESNT ACCOUNT FOR THIS WHEN USING IN BACKTEST DATA

# current_time needs fixing - so it is always correct - if '1sec' isnt in resolutions then step to next hour gives eg 11:55 when it should be 11:59:59

# work out neat ways to step in hours for eg but step then next tick to check open - if not met swtich back to 1hour etc 

# need checking data inport functions =  since sometimes seconds wont have all timerange while 1hour will - then fuck things up 


## NEED TO CLEAN DATA
- DATA COLLECTION FIX AND SQL connection etc
- Back Tester
    - get panels working
    - indicators
    - tester
- Data Anltyics

current larger increment bar is not upaded

# now need to make list
# add functionality in strategy class where specifc time range for allowed trades 
#  add absoulte expriry for trade - if using breaks in data
# need to deal reset avaible data for new day if break in data 
#  thinking best way is to write different strats to get the occurances i want to fix 
# need to fix trading signal functionality so it can have mutiple singals in a single bar
# need to come back to indicator functionality and get personal indicators working and plotting etc 
# need to do moving indicator eg like regression plotting
# need to make stratgey implmentations better (less messy)
#### problems with how exiting marakrt happens and is checked for open intraday trades that have expired. 
# WANT TO MODEL HOW  MOVES can RECOVER TO WHAT DEGREE AND HOW FAST, AND what CONTEXT.
#FIX BROKER