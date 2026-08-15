import argparse,hashlib,json,re
TOKEN=re.compile(r"\{\{([a-zA-Z][a-zA-Z0-9_]*)\}\}")
def render(template,values,max_chars=100000):
 if not isinstance(template,str) or len(template)>max_chars or not isinstance(values,dict): return {"ok":False,"errors":["invalid_input"]}
 required=set(TOKEN.findall(template)); missing=sorted(required-set(values)); extra=sorted(set(values)-required)
 if missing or extra or any(not isinstance(v,(str,int,float,bool)) for v in values.values()): return {"ok":False,"errors":{"missing":missing,"extra":extra}}
 body=TOKEN.sub(lambda m:str(values[m.group(1)]),template)
 return {"ok":True,"markdown":body,"sha256":hashlib.sha256(body.encode()).hexdigest(),"fields":sorted(required)}
def probe():
 g=render("# {{title}}",{"title":"Demo"}); b=render("{{missing}}",{}); return {"ok":g["ok"] and not b["ok"],"counter_proof":not b["ok"]}
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("command",choices=("render","probe"));p.add_argument("--input");a=p.parse_args(argv);data=json.load(open(a.input)) if a.input else {};out=probe() if a.command=="probe" else render(data.get("template"),data.get("values"));print(json.dumps(out,sort_keys=True));return 0 if out["ok"] else 2
