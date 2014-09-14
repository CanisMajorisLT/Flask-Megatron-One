__author__ = 'vyt'
from bs4 import BeautifulSoup
lol = 	'''	<select name="otsing[par2]" class="textSmall" width="100" style="width:350px;">
		<option value="0"> - select month -</option>
		<option value="1">January</option>
		<option value="2">February</option>
		<option value="3">March</option>
		<option value="4">April</option>
		<option value="5">May</option>
		<option value="6">June</option>
		<option value="7">July</option>
		<option value="8">August</option>
		<option value="9" selected="selected">September</option>
		<option value="10">October</option>
		<option value="11">November</option>
		<option value="12">December</option>
	</select>'''
nigga= {}
x = BeautifulSoup(lol, 'lxml')
for y, x in enumerate(x.find_all('option')):
    nigga[x.text] = y

print(nigga)