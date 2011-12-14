class PokefansTunnel:
	def Name2Typ(self, typx):
		Types = {
	0x0: "Normal",
	0x1: "Feuer",
	0x2: "Eis",
	0x3: "Pflanze",
	0x4: "Boden",
	0x5: "Gestein",
	0x6: "Kampf",
	0x7: "Geist",
	0x8: "Elektro",
	0x9: "Psycho",
	0xa: "Gift",
	0xb: "Wasser",
	0xc: "Flug",
	0xd: "Kaefer",
	0xe: "Drache",
	0xf: "null"
}
		for typ in Types:
			if Types[typ] == typx: return typ
			
	def get_pokemon_data(self, pkmn, atk_func):
		import urllib
		import urllib2
		# fetch pokedex_informations (like color etc) :)
		a = "http://pokefans.net/pokedex/pokemon/%s/1" % (pkmn.lower())
		casrc = urllib2.urlopen(a).read()
		asrc = casrc.split('<p>Die wesentlichen Erkennungsmerkmale von')[1]
		asrc = asrc.split('<ul style="line-height: 25px;">')[1]
		asrc = asrc.split("</ul>")[0]
		u = 0
		for i in asrc.split("<li>")[1:]:
			u = u + 1
			if u == 1:
				size = i.split("</li>")[0]
				sizex = size.split(" ")[1]
				sizex += size.split(" ")[2]
			elif u == 2:
				wsize = i.split("</li>")[0]
				wsizex = wsize.split(" ")[1]
				wsizex += wsize.split(" ")[2]
			elif u == 3:
				print i
				color = i.split("</li>")[0].split("Farbe: ")[1]
		XDATA = {}
		XDATA = {
				'color':color,
				'groesse':sizex,
				'gewicht':wsizex}
		d = casrc.split("<p>Verschiedene Daten:</p>")[1]
		d = d.split("</ul>")[0]
		u = 0
		for i in d.split("<li>")[1:]:
			u = u + 1
			if u == 1:
				spezies = i.split("Spezies: ")[1].split("</li>")[0]
			elif u == 2:
				catchrate = int(i.split("Fangrate: ")[1].split("</li>")[0])
			elif u == 3:
				base_happiness = int(i.split("Base-Happiness: ")[1].split("</li>")[0])
			elif u == 4:
				exp_type = int(i.split("100: ")[1].split("</li>")[0])
		XDATA["spezies"] = spezies	
		XDATA["catchrate"] = catchrate
		XDATA["base_happiness"] = base_happiness
		XDATA["lvl100exp"] = exp_type
			
		u = "http://pokefans.net/pokedex/pokemon/%s/1/statuswerte" % (pkmn.lower())
		xsrc = urllib2.urlopen(u).read()
		
		# typ definition
		xsrc2 = xsrc.split('<br/><span class="fakt">Typ</span>: ')[1].split("<br/><span")[0]
		if "+" in xsrc2:
			typ1 = self.Name2Typ(xsrc2.split(" + ")[0])
			typ2 = self.Name2Typ(xsrc2.split(" + ")[1])
			
		else: typ1 = self.Name2Typ(xsrc2)
		
		src = xsrc.split('<table class="table-w" cellpadding="7" cellspacing="1" border="0">')[1].split("</table>")[0]
		base_kp = int(src.split('name="base_1" value="')[1].split('"')[0])
		base_atk = int(src.split('name="base_2" value="')[1].split('"')[0])
		base_def = int(src.split('name="base_3" value="')[1].split('"')[0])
		base_spd = int(src.split('name="base_4" value="')[1].split('"')[0])
		base_satk = int(src.split('name="base_5" value="')[1].split('"')[0])
		base_sdef = int(src.split('name="base_6" value="')[1].split('"')[0])
		
		x = {"base_kp":base_kp,"base_atk":base_atk, "base_def":base_def,"base_spd":base_spd,"base_satk":base_satk,"base_sdef":base_sdef}
		#insert type here
		try: x['types'] = [typ1, typ2]
		except: x['types'] = [typ1]
		# get attacks in here
		u = "http://pokefans.net/pokedex/pokemon/%s/1/attacken" % (pkmn.lower())
		sx = urllib2.urlopen(u).read()
		src = sx.split('<tr class="tb_head-w" align="center"><th align="left" width="105">Attacke</th><th>Methode</th><th>Typ</th><th>SP</th><th>TQ</th><th>AP</th><th>Modus</th></tr>')[1].split('<tr class="tb_head-w" align="center"><th align="left" width="105">Attacke</th><th>Methode</th><th>Typ</th><th>SP</th><th>TQ</th><th>AP</th><th>Modus</th></tr><tr class="z1" align="center" style="height: 30px">')[0]
		c = {}
		for atk in src.split("</tr><tr"):
			
			name = atk.split("/attacken/")[1].split('">')[1].split("</a>")[0].capitalize()
			c[name] = {
				'level': int(atk.split('">Level ')[1].split("</td>")[0]),
				'id': atk_func(name)
			}
		x["attacks"] = c
		w = {}
		v = {}
		try:
			wsrc = sx.split('<tr class="tb_head-w" align="center"><th align="left" width="105">Attacke</th><th>Methode</th><th>Typ</th><th>SP</th><th>TQ</th><th>AP</th><th>Modus</th></tr>')[3].split('<tr class="tb_head-w" align="center"><th align="left" width="105">Attacke</th><th>Methode</th><th>Typ</th><th>SP</th><th>TQ</th><th>AP</th><th>Modus</th></tr><tr class="z1" align="center" style="height: 30px">')[0]
		
			for watk in wsrc.split("</tr><tr"):
				name = watk.split("/attacken/")[1].split('">')[1].split("</a>")[0].capitalize()
				w[name] = {
					'id':atk_func(name),
					'is_tm':True,
				}
		except: pass
		
		try:
			vmsrc = sx.split('<tr class="tb_head-w" align="center"><th align="left" width="105">Attacke</th><th>Methode</th><th>Typ</th><th>SP</th><th>TQ</th><th>AP</th><th>Modus</th></tr>')[4].split('<tr class="tb_head-w" align="center"><th align="left" width="105">Attacke</th><th>Methode</th><th>Typ</th><th>SP</th><th>TQ</th><th>AP</th><th>Modus</th></tr><tr class="z1" align="center" style="height: 30px">')[0]
		
			for vatk in vmsrc.split("</tr><tr"):
				name = vatk.split("/attacken/")[1].split('">')[1].split("</a>")[0].capitalize()
				v[name] = {
					'id':atk_func(name),
					'is_vm':True,
				}
		except: pass
		x["attacks"]["vm"] = v
		x["attacks"]["tm"] = w

		x.update(XDATA)
		return x
			
	def print_attacks(self, rangex=560):
		import pprint
		import urllib
		import urllib2
		
		a = {}
		url = "http://pokefans.net/pokedex/attacken/liste"
		source = "".join(urllib2.urlopen(url).read().split('<tr class="zh">')[1].split("</tr>\n")[1:]).split("</table>")[0].split('<tr class="')
		for i in range(1,rangex):
			
			# check for generation
			if source[i].__contains__("1. Generation"): 
			
				name = source[i].split('">')[3].split("</a>")[0]
				print name
				typ = source[i].split('alt="')[1].split('"')[0]
				try: blocks = source[i].split('class="icon" /></td>')[1].split("<td>")
				except:
					blocks = source[i].split("<td></td>")[1].split("<td>")
				#1 => angriff, #2 => acc, #3 => ap
				dmg = blocks[1].split("</td>")[0].replace("KO.","0").replace("-","0")
				acc = blocks[2].split("</td>")[0]
				ap = blocks[3].split("</td>")[0]
				typ2hex = lambda x: x+1
				a[("__" + (hex(i)) + "__")] = {
					"name": name,
					"typ": typ2hex(typ),
					"atk": "__" + hex(int(dmg)) + "__",
					"ap": "__" + hex(int(ap)) + "__",
					"acc": "__" + hex(int(acc)) +"__"
				}
				
			
		f = open("attacks.dict.txt", "w")
		pp = pprint.PrettyPrinter(stream=f, indent=4, depth=6)
		pp.pprint(a)
		#f
		f.close()
		x = open("attacks.dict.txt", "r+")
		s = x.read().replace("'__", '').replace("__'", '')
		x.close()
		return s

if __name__ == "__main__":
	from pokemon import Pokemon
	from attacks import Attacks
	import pprint 
	import sys
	
	def atk2id(name):
		for atk in Attacks:
			if Attacks[atk]["name"] == name:
				return atk
	
	x = PokefansTunnel().get_pokemon_data
	pkmn = {}

	for pokemon in Pokemon:
		print Pokemon[pokemon]["name"]
		pkmn[pokemon] = x(Pokemon[pokemon]["name"].replace(" ", "_"), atk2id)
		pkmn[pokemon]["name"] = Pokemon[pokemon]["name"]
	
	
	f = open("awk_list.txt", "w")
	pprint.pprint(pkmn, f)
	f.close()
	
	
"""
if __name__ == "__main__":			
	from pokemon import Pokemon
	from attacks import Attacks

	def atk2id(name):
		for atk in Attacks:
			if Attacks[atk]["name"] == name:
				return atk
			
	x = PokefansTunnel().get_pokemon_data
	pkmn = {}
	for pokemon in Pokemon:
		print pokemon
		pkmn[Pokemon.index(pokemon)] = x(pokemon.replace(" ", "_"), atk2id)
		pkmn[Pokemon.index(pokemon)]["name"] = pokemon
	
	f = open("awk_list.txt", "w")
	f.write(str(pkmn))
	f.close()
	
"""
