import re 
import os
numset = [
	"0", "1",  "2",  "3",  "4",  "5",
 	"6",  "7",  "8",  "9",  "."
 	]

def scale(s, loc, factor):
	n = 1
	while loc - n > 0:
		# print(loc-n, s[loc-n])
		if s[loc-n] not in numset:
			break
		n += 1
	n -= 1
	if n == 0: return s, 0
	else:
		num = float(s[loc-n:loc])*factor
		return (s[:loc-n] + "%.5f"%num + s[loc:], len("%.5f"%num)-len(s[loc-n:loc]))

fname_save = fname = "filt_design2.tex"
# fname_save = "basic_pll.tex"
factor = 0.7

os.system("cp ~/%s ./"%fname)
os.system("cp ~/%s.ps ./"%fname.split(".")[0])

f = open(fname, "r")
text = f.read()
f.close()
locs = [i.start() for i in re.finditer("in", text)]
offset = 0 
for loc in locs:
	text, delta = scale(text, loc+offset, factor)
	offset += delta
text=text.replace("scale=1", "scale=%0.5f"%factor)
sans = "\\fontfamily{\\sfdefault}\\selectfont\n"
serif = "\\fontfamily{\\rmdefault}\\selectfont\n"

if text.find(".pdf") < 0:
	loc = text.find("\\includegraphics")
	n = 1
	while text[loc+n] != "{":
		n+=1
	n += 1
	m = 1
	while text[loc+n+m] != "}":
		m+=1
	os.system("ps2pdf -dEPSCrop %s.ps"%text[loc+n:loc+n+m])
	text = text[:loc+n+m] + ".pdf" + text[loc+n+m:]
if text.find(sans) < 0:
	text = sans + text + serif
if text.find("./figs/") < 0:
	loc = text.find("\\includegraphics")
	n = 1
	while text[loc+n] != "{":
		n += 1
	n += 1
	text = text[:loc+n] + "./figs/" + text[loc+n:]

print(text)
f = open(fname_save, "w")
f.write(text)
f.close()
