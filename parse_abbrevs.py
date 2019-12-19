import yaml

LINES_PER_PAGE = 36

files = [
    "appendix.tex",
    "cover.tex",
    "disco.tex",
    "intro.tex",
    "methods.tex",
    "report.tex",
    "theory.tex",
    "theory2.tex",
]

punctuation = [
    ",", ".", "\'", "\"",
    ":", ";", "(", ")",
    "+", "-", "/", "*",
    "{", "}", "[", "]",
    "<", ">", "_", "^",
    "\\", "|"
]

whitespace = [
    "\t", "\t", "\r", "\f",
    "\n", "  ", "   ", "    ",
    "     ", "      ", "       ",
    "        "
]

acronyms = []

for fname in files:
    # print("\n", fname)
    with open(fname, "r") as file:
        text = file.read()

    for p in punctuation:
        text = text.replace(p, " ")
    for w in whitespace:
        text = text.replace(w, " ")
    words = text.split(" ")
    words = [word[:-1] if (len(word)>0 and word[-1] =="s") else word for word in words]
    all_upper = [word for word in words if word.isupper()]
    all_upper = [word for word in all_upper if word.find("$") < 0]
    all_upper = [word for word in all_upper if len(word) > 1]

    # print("\n")
    # for word in all_upper:
        # print("\t", word)
    acronyms.extend(list(set(all_upper)))

acronyms = list(set(acronyms))
acronyms.sort()


with open("acronym_blacklist.txt", "r") as file:
    blacklist = file.read()
blacklist = blacklist.split("\n")
blacklist = [word.strip() for word in blacklist]

acronyms = [word for word in acronyms if word not in blacklist]

print("\nFound acronyms (%d):"%len(acronyms))
for word in acronyms:
    print("\t", word)

# defs = {}
# for word in acronyms:
    # defs[word] = ""

# with open("abbrevs.yaml", 'w') as file:
    # documents = yaml.dump(defs, file)

with open("abbrevs.yaml", 'r') as file:
    defs = yaml.load(file)

print("\nChecking detected acronyms against database, abbrevs.yaml")
print("New abbreviations:")
for word in acronyms:
    if word not in defs:
        print("\t", word)
        defs[word] = ""

with open("abbrevs.yaml", 'w') as file:
    documents = yaml.dump(defs, file)

print("\nChecking abbreviations no longer in use:")
print("Disused abbreviations:")
for word in list(defs):
    if word not in acronyms:
        print("\t", word)


def make_table(acronyms, defs):
    s = ""
    s += "\t\\begin{table}[htb!]\n"
    s += "\t\\renewcommand*{\\arraystretch}{1.45}\\large\n"
    s += "\t\\begin{tabular}{@{}ll}\n"
    for acronym in acronyms:
        s += "\t\t\\textbf{\\textsf{%s}}\t&\t%s \\\\\n"%(acronym, defs[acronym])
    s += "\t\\end{tabular}\n"
    s += "\t\\end{table}\n"
    return s

s = ""

pages = []
n = 0
for word in acronyms:
    if n%LINES_PER_PAGE == 0:
        pages.append([])
    pages[-1].append(word)
    n += 1

# s += "\\pagebreak\n"
# s += "\\null\n"

for n, page in enumerate(pages):
    # s += "\\pagebreak\n"
    if n==0:
        s += "\\section*{Abbreviations.}\n"
    s += make_table(page, defs)

# print("\nGenerated abbrev.tex:")
print(s)

with open("abbrev.tex", "w") as file:
    file.write(s)

