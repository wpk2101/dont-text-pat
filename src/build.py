import json
draft = {
# Kerns
"Franz Wagner":17,"Jalen Williams":27,"Tyler Herro":6,"Cooper Flagg":35,"Chet Holmgren":36,"Kevin Durant":29,"Jalen Brunson":31,"Rudy Gobert":2,"D'Angelo Russell":1,"Brandon Ingram":8,"Cam Thomas":4,"Dylan Harper":1,"Mark Williams":2,
# SD
"Anthony Davis":60,"Trey Murphy III":6,"Giannis Antetokounmpo":69,"Donovan Mitchell":38,"Ausar Thompson":9,"Kawhi Leonard":11,"Immanuel Quickley":1,"Donovan Clingan":1,"Dereck Lively II":1,"Devin Vassell":1,"Kyrie Irving":1,"Cason Wallace":1,"Jared McCain":1,
# Switz
"Dyson Daniels":10,"Deni Avdija":6,"Scottie Barnes":28,"Anthony Edwards":67,"Devin Booker":48,"DeMar DeRozan":6,"Jaren Jackson Jr.":20,"Naz Reid":4,"John Collins":5,"Stephon Castle":3,"Jaylen Wells":1,"Isaiah Hartenstein":1,"Zaccharie Risacher":1,
# Dema
"Victor Wembanyama":56,"Ivica Zubac":13,"Austin Reaves":8,"Trae Young":44,"De'Aaron Fox":23,"Stephen Curry":41,"OG Anunoby":8,"Shaedon Sharpe":1,"Onyeka Okongwu":2,"Deandre Ayton":1,"VJ Edgecombe":1,"Malik Monk":1,"RJ Barrett":1,
# Denning
"Amen Thompson":7,"James Harden":39,"Jaylen Brown":35,"Domantas Sabonis":38,"Myles Turner":38,"Jamal Murray":16,"Paul George":4,"Jakob Poeltl":7,"Jarrett Allen":2,"Norman Powell":5,"CJ McCollum":3,"Cameron Johnson":2,"Bub Carrington":1,
# Koulet
"Pascal Siakam":27,"Karl-Anthony Towns":53,"Evan Mobley":34,"Coby White":17,"Jordan Poole":5,"Jimmy Butler III":7,"Walker Kessler":13,"Mikal Bridges":10,"Lauri Markkanen":12,"Darius Garland":11,"Jalen Suggs":2,"Julius Randle":4,"Andrew Nembhard":5,
# Bran
"Shai Gilgeous-Alexander":53,"Jalen Johnson":23,"Zion Williamson":24,"Desmond Bane":19,"Kevin Porter Jr.":2,"Ja Morant":25,"Michael Porter Jr.":12,"Reed Sheppard":3,"Jayson Tatum":12,"Jalen Duren":8,"Matas Buzelis":4,"Tari Eason":1,"Kel'el Ware":3,
# Daigle
"Miles Bridges":16,"Toumani Camara":6,"Tyrese Maxey":23,"LaMelo Ball":38,"LeBron James":27,"Nikola Vucevic":25,"Alperen Sengun":33,"Kristaps Porzingis":10,"Anfernee Simons":7,"Zach LaVine":10,"Jabari Smith Jr.":3,"Bradley Beal":1,"Bennedict Mathurin":1,
# Dionne
"Christian Braun":8,"Josh Hart":10,"Derrick White":16,"Luka Doncic":79,"Bam Adebayo":29,"Paolo Banchero":32,"Brandon Miller":13,"Draymond Green":2,"Jaden McDaniels":1,"Keegan Murray":1,"Tyrese Haliburton":2,"Ace Bailey":2,"Keyonte George":1,
# Scully
"Josh Giddey":9,"Cade Cunningham":57,"Payton Pritchard":6,"Nikola Jokic":83,"Jalen Green":10,"Alex Sarr":13,"Joel Embiid":15,"Dejounte Murray":2,"Santi Aldama":1,"Klay Thompson":1,"Donte DiVincenzo":1,"Buddy Hield":1,"Andrew Wiggins":1,
}
assert len(draft)==130, len(draft)
# years kept in 2025 (from keeper sheet)
kept25 = {"Dyson Daniels":1,"Deni Avdija":1,"Scottie Barnes":2,"Christian Braun":1,"Josh Hart":1,"Derrick White":2,"Franz Wagner":1,"Tyler Herro":1,"Jalen Williams":2,"Anthony Davis":2,"Trey Murphy III":1,"Giannis Antetokounmpo":1,"Pascal Siakam":1,"Victor Wembanyama":2,"Ivica Zubac":1,"Austin Reaves":1,"Amen Thompson":1,"James Harden":1,"Jaylen Brown":2,"Miles Bridges":2,"Toumani Camara":1,"Tyrese Maxey":2,"Josh Giddey":1,"Cade Cunningham":4,"Payton Pritchard":1,"Shai Gilgeous-Alexander":3,"Jalen Johnson":1,"Zion Williamson":1}
owners={"PK":"Kerns","SD":"D'Arcy","SWIT":"Switzer","DEMA":"Dema","DENN":"Denning","KOU":"Koulet","BRAN":"Bran","TRIS":"Daigle","DION":"Dionne","CURT":"Scully"}
DEADLINE="2026-02-23"
teams=[];players=[]
for line in open('rosters_2026.txt'):
    ab,name,rest=line.strip().split('~')
    teams.append({"ab":ab,"name":name,"owner":owners[ab]})
    for p in rest.split(';'):
        n,a,v,d=p.rsplit(',',3); v=int(v); d="20"+d
        kind={"D":"draft","A":"pickup","T":"trade"}[a]
        dp=draft.get(n)
        eligible = not (kind=="pickup" and d>DEADLINE)
        base=max(v, dp or 0)
        yrs=kept25.get(n,0)+1
        players.append(dict(n=n,t=ab,kind=kind,date=d,paid=v,draft=dp,eligible=eligible,base=base,yrs=yrs,
          price=base+5*yrs if eligible else None))
undrafted_off=[n for n in draft if n not in {p['n'] for p in players}]
json.dump({"teams":teams,"players":players,"offRoster":undrafted_off},open('data.json','w'))
for p in sorted(players,key=lambda p:-(p['price'] or 0))[:12]: print(p['n'],p['price'],p['base'],p['yrs'])
print(sum(not p['eligible'] for p in players),'ineligible')
for p in players:
  if p['kind']!='draft' and p['draft'] and p['draft']!=p['paid']: print('diff',p['n'],p['kind'],p['paid'],p['draft'],p['eligible'])
