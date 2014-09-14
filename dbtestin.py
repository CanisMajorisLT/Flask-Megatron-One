import re
import datetime, time
from bs4 import BeautifulSoup

st = """<a name="top"></a><div id="fb-root"></div>
	<script src="//files.cvonline.lt/static/liitu.inc" type="text/javascript" rel="nofollow"></script>
	<div id="popup-big" style="width: 640px;">
		<table border="0" width="99%">
		   <tr>
			<td class="helpPageHead" align="left"><h1>Aurimas Gudas - 3274901</h1></td>
			<td align="right"><p><a href="//www.cvonline.lt/" target="_blank"><img src="//files.cvonline.lt/ln_images/icons/help_logo_cvonline.gif" valing="bottom" /></a></p></td>
		   </tr>
		</table>
	</div>
	<table width="640" style="width: 640px;" class="popup-table"><tbody>
	   <tr>
		<td><div class="border4"><div class="border3"><div class="border2"><div class="border1"><!-- Middle part start //-->
<table border="0" class="top_inf"><tbody>
   <tr>
	<td align="left"><nobr><strong>CV kodas: 3274901</strong></nobr></td>
	<td width="33%" align="center"><nobr>Atnaujinimo data: 06. rugsėjo 2014</nobr></td>
	<td align="right"><nobr><a href="/CVC/3274901.html?cv_id=3274901&tegevus=print" target="PrintWindow" onclick="fullcv_win(this.href, this.target);return(false);" class="Button">Spausdinti</a><a href="/CVC/3274901.html?cv_id=3274901&tegevus=print&pdf=1" rel="nofollow" class="cvpdflink"><img src="//files.cvonline.lt/ln_images/icons/pdf.png" class="pdficon"></a> &nbsp; <a href="/CVC/3274901.html?cv_id=3274901&tegevus=print&print_history=1" target="PrintWindow" onclick="fullcv_win(this.href, this.target);return(false);" class="Button">Spausdinti su papildoma info</a><a href="/CVC/3274901.html?cv_id=3274901&tegevus=print&pdf=1&print_history=1" rel="nofollow" class="cvpdflink"><img src="//files.cvonline.lt/ln_images/icons/pdf.png" class="pdficon"/></a></nobr></td>
   </tr>
</tbody></table><div class="popup-content ">
<div class="clear"></div><div class="cvVormHeading" style="width: 100%;">Asmeniniai duomenys</div><div class="clear"></div>
<table width="100%" class="CvVormTable">  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">Vardas:</td>
    <td class="cvVormText" height="20" width="252" align="left" valign="top">Aurimas Gudas<div class="cvVormPicture"><div><img src="//www.cvonline.lt/client/fullcv_image.php/3274901.gif" alt="" border="0" /></div></div></td>
  </tr>
  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">Amžius:</td>
    <td class="cvVormText" height="20" align="left" valign="top">29</td>
  </tr>
  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">Gimimo data:</td>
    <td class="cvVormText" height="20" align="left" valign="top">02. rugsėjo 1985</td>
  </tr>
  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">Lytis:</td>
    <td class="cvVormText" height="20" align="left" valign="top">Vyras</td>
  </tr>
  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">Adresas:</td>
    <td class="cvVormText" height="20" align="left" valign="top">Kaunas, Kauno, Lietuva</td>
  </tr>
  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">El. paštas:</td>
    <td class="cvVormText" height="20" align="left" valign="top"><a href="//www.cvonline.lt/client/email_seeker.php?cv_id=3274901" onClick="return(aken(this.href, 'mail_aken', '500','450'));">aurimas@gudas.lt</a></td>
  </tr>
  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">Skype:</td>
    <td class="cvVormText" height="20" colspan="2" width="372" align="left" valign="top"><a href="skype:aurimas_gudas?add">aurimas_gudas</a></td>
  </tr>
  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">Nuorodos:</td>
    <td class="cvVormText" height="20" colspan="2" width="372" align="left" valign="top"><a href="http://gudas.lt" target="_blank" class="arrow">Tinklaraštis</a></td>
  </tr>
  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">Kontaktinis telefonas:</td>
    <td class="cvVormText" height="20" colspan="2" width="372" align="left" valign="top">8 (671) 18800</td>
  </tr>
  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">Išsilavinimas:</td>
    <td class="cvVormText" height="20" colspan="2" width="372" align="left" valign="top">Aukštasis universitetinis</td>
  </tr>
  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">Dabartinio darbo statusas:</td>
    <td class="cvVormText" height="20" colspan="2" width="372" align="left" valign="top">Studijuojantis</td>
  </tr>
  <tr>
    <td class="cvVormSpacer" colspan="3">&nbsp;</td>
  </tr>
  <tr>
    <td class="cvVormLeftSide" height="20" width="174" align="left" valign="top">CV redagavimo data:</td>
    <td class="cvVormText" height="20" colspan="2" width="372" align="left" valign="top">06. rugsėjo 2014</td>
  </tr>
  <form method="post">
  <tr class="no-background">
    <td colspan="3" class="textSmall" align="right"><input type="button" value="Siųsti el.žinutę" class="Button" onClick="javascript:aken('//www.cvonline.lt/client/email_seeker.php?cv_id=3274901', 'mail_aken', '500','450');"/></td>
  </tr>
  </form>
</table>"""

soup = BeautifulSoup(st, 'lxml')
personal_data = soup.find('table', class_="CvVormTable")

personal_data_list = [x.text for x in personal_data.find_all('td')]
first_name, last_name, phone, email = None, None, None, None
for y, x in enumerate(personal_data_list):
    if x == "Vardas:":
        try:
            first_name, last_name = personal_data_list[y+1].split(' ')[0], personal_data_list[y+1].split(' ')[1]
        except Exception as e:
            print(e)
    if x == "El. paštas:" or x == "E-mail:":
        email = personal_data_list[y+1]
    if x == "Kontaktinis telefonas:" or x == "Contact telephone:":
        phone = personal_data_list[y+1]

print([type(datetime.date(2014, 9, 7).strftime("%Y-%m-%d"))])