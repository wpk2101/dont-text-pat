# Rebuild index.html from src/: python3 src/build_page.py
import os
os.chdir(os.path.join(os.path.dirname(__file__),".."))
t=open("src/page.tpl.html").read()
body=t.replace("__DATA__",open("src/data.json").read()).replace("__LOGO__",open("src/logo.b64").read())
i=body.index("</style>")+len("</style>")
open("index.html","w").write(open("src/head.html").read()+body[:i]+"\n</head>\n<body>\n"+body[i:]+"\n</body>\n</html>\n")
