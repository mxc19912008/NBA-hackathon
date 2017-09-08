# NBA-hackathon
##Writeup: Solving Process Explanation
In this Bonus question, we take three steps to get the result of when a team is eliminated from the Playoffs.
1)	Read the rules and figure out what to do.
2)	Get the most useful tables from original data. The tables include:
	Daily team vs team wins table, which would help us break ties;
	Daily team cumulative performance table, which would help us rank teams.
3)	Build the algorithms to determine when a team is eliminated.
	Determine which team is the 8th team in each conference;
	Determine the “Maximum possible winning rate” and “Minimum possible winning rate”, and compare the “Minimum possible winning rate” of the 8th team to the “Maximum possible winning rate” of teams ranked after 8th. If the former is greater, then the compared team is eliminated on that day.
	Break ties based on the rules and priority given.
	Use a dictionary to update elimination date (loop from the last game day to the first game day).
	Complete the result list by filling the teams that entered the Playoffs.
Then we get the final result：

Team	Date Eliminated
 Boston Celtics	 Playoffs
 Brooklyn Nets	 2017/3/8
 New York Knicks	 2017/3/29
 Philadelphia 76ers	 2017/3/28
 Toronto Raptors	 Playoffs
 Chicago Bulls	 Playoffs
 Cleveland Cavaliers	 Playoffs
 Detroit Pistons	 2017/4/6
 Indiana Pacers	 Playoffs
 Milwaukee Bucks	 Playoffs
 Atlanta Hawks	 Playoffs
 Charlotte Hornets	 2017/4/8
 Miami Heat	 2017/4/12
 Orlando Magic	 2017/3/28
 Washington Wizards	 Playoffs
 Denver Nuggets	 2017/4/9
 Minnesota Timberwolves	 2017/4/1
 Oklahoma City Thunder	 Playoffs
 Portland Trail Blazers	 Playoffs
 Utah Jazz	 Playoffs
 Golden State Warriors	 Playoffs
 LA Clippers	 Playoffs
 Los Angeles Lakers	 2017/3/17
 Phoenix Suns	 2017/3/21
 Sacramento Kings	 2017/3/29
 Dallas Mavericks	 2017/4/1
 Houston Rockets	 Playoffs
 Memphis Grizzlies	 Playoffs
 New Orleans Pelicans	 2017/4/4
 San Antonio Spurs	 Playoffs

