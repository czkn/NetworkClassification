import os, random, time, subprocess

pages=['/watch/80113701', '/watch/80091938', '/watch/80117291', '/watch/70272479', '/watch/80092801', '/watch/60020949', '/watch/60004480', '/watch/80230402', '/watch/80135073', '/watch/80089198', '/watch/70264888', '/watch/70197057', '/watch/70142386', '/watch/80133042', '/watch/70136129', '/watch/70140391', '/watch/70136126', '/watch/70136120', '/watch/70204970', '/watch/80002667', '/watch/80118100', '/watch/70142436', '/watch/80057281', '/watch/80156386', '/watch/70302573', '/watch/80195377', '/watch/70142388', '/watch/80117470', '/watch/70293316', '/watch/80123729', '/watch/60000901', '/watch/70305883', '/watch/70197042', '/watch/80109536', '/watch/70153408', '/watch/80082647', '/watch/70153404', '/watch/80158104', '/watch/80095314', '/watch/70197049', '/watch/80018988', '/watch/70143811', '/watch/80135164', '/watch/70279852', '/watch/70178217', '/watch/80108495', '/watch/80160689', '/watch/70050483', '/watch/80002612', '/watch/70251894', '/watch/80018987', '/watch/80007945', '/watch/80025744', '/watch/80063224', '/watch/80027042', '/watch/80115432', '/watch/80071348', '/watch/80159566', '/watch/80077977', '/watch/80108237', '/watch/80100172', '/watch/70157130', '/watch/80098101', '/watch/80084660', '/watch/80108238', '/watch/80108239', '/watch/80109128', '/watch/80066080', '/watch/80002537', '/watch/80044950', '/watch/80065182', '/watch/80122759', '/watch/80221860', '/watch/80133311', '/watch/80075820', '/watch/80109194', '/watch/80084164', '/watch/70180183', '/watch/80063740', '/watch/80077417', '/watch/80088567', '/watch/80197912', '/watch/80204927', '/watch/70198116', '/watch/80117552', '/watch/80113612', '/watch/80131167', '/watch/80146284', '/watch/70283260', '/watch/70143836', '/watch/80107084', '/watch/70177007', '/watch/80099656', '/watch/70280714', '/watch/80074249', '/watch/70180057', '/watch/80181555', '/watch/14607635', '/watch/80160759', '/watch/80039394', '/watch/80176878', '/watch/70157152', '/watch/80117545', '/watch/80095299', '/watch/80149706', '/watch/80117540', '/watch/80050063', '/watch/80018869', '/watch/80198661', '/watch/70283264', '/watch/80169546', '/watch/80222177', '/watch/80135414', '/watch/80208337', '/watch/70196145', '/watch/80155477', '/watch/80146758', '/watch/80095900', '/watch/70140403', '/watch/80117498', '/watch/80190283', '/watch/80121839', '/watch/80174974', '/watch/70143844', '/watch/70143843', '/watch/70143842', '/watch/80022632', '/watch/80164456', '/watch/70210884', '/watch/80109415', '/watch/70155629', '/watch/80072207', '/watch/70155582', '/watch/70301344', '/watch/70266998', '/watch/80097726', '/watch/70305929', '/watch/70056429', '/watch/80053653', '/watch/80065386', '/watch/80117560', '/watch/80002566', '/watch/70155574', '/watch/70124975', '/watch/80083977', '/watch/80214777', '/watch/70302484', '/watch/80029103', '/watch/80094319', '/watch/70296346', '/watch/70172488', '/watch/70136152', '/watch/80119234', '/watch/70155618', '/watch/70153390', '/watch/80122179', '/watch/80049714', '/watch/80079258', '/watch/80216224', '/watch/80025172', '/watch/80171362', '/watch/70283198', '/watch/80063265', '/watch/80192098', '/watch/80175722', '/watch/70184207', '/watch/70175633', '/watch/80051137', '/watch/80117526', '/watch/80074220', '/watch/70242311', '/watch/80165247', '/watch/70254851', '/watch/80177803', '/watch/70143825', '/watch/80050008', '/watch/80119411', '/watch/848396', '/watch/80092415', '/watch/80002479', '/watch/70245163', '/watch/70177057', '/watch/70105599', '/watch/705761', '/watch/80010655', '/watch/70143860', '/watch/80092799', '/watch/80020540', '/watch/80105699', '/watch/80108182', '/watch/70205012', '/watch/80000770', '/watch/80149092', '/watch/70269479', '/watch/80100929', '/watch/80025678', '/watch/80027158', '/watch/80114855', '/watch/80117694', '/watch/70204981', '/watch/80039517', '/watch/70185015', '/watch/80037657', '/watch/80024057', '/watch/70272726', '/watch/80158485', '/watch/80094603', '/watch/80178726', '/watch/70187727', '/watch/80097141', '/watch/70095147', '/watch/80171965', '/watch/70219642', '/watch/80091879', '/watch/80212127', '/watch/70136135', '/watch/70202589', '/watch/80146805', '/watch/70047819', '/watch/80021955', '/watch/80117038', '/watch/80020542', '/watch/70281312', '/watch/80017537']
domain='https://www.netflix.com'
killChrome=1
while True:
	if killChrome:
		os.system("taskkill /IM chrome.exe")
		time.sleep(1)
	url= domain+ random.choice(pages)
	#os.system("start "+ url)
	p = subprocess.Popen(["C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",  url ])
	time.sleep(60)