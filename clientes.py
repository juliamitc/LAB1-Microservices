from datetime import datetime
from flask import jsonify, make_response, abort

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/") # Local
db = client.clientes

def get_dict_from_mongodb():
 itens_db = db.clientes.find()
 PEOPLE = {}
 for i in itens_db:
  i.pop('_id') # retira id: criado automaticamente
  item = dict(i)
  PEOPLE[item["lname"]] = (i)
 return PEOPLE
 
def get_timestamp():
 return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
 
def read_all():
 PEOPLE = get_dict_from_mongodb()
 dict_clientes = [PEOPLE[key] for key in sorted(PEOPLE.keys())]
 clientes = jsonify(dict_clientes)
 qtd = len(dict_clientes)
 content_range = "clientes 0-"+str(qtd)+"/"+str(qtd)
 # Configura headers
 clientes.headers['Access-Control-Allow-Origin'] = '*'
 clientes.headers['Access-Control-Expose-Headers'] = 'Content-Range'
 clientes.headers['Content-Range'] = content_range
 return clientes
 
def read_one(lname):
 PEOPLE = get_dict_from_mongodb()
 if lname in PEOPLE:
  person = PEOPLE.get(lname)
 else:
  abort(
   404, "Pessoa com sobrenome {lname} nao encontrada".format(lname=lname)
  )
 return person
 
def create(person):
 lname = person.get("lname", None)
 fname = person.get("fname", None)
 PEOPLE = get_dict_from_mongodb()
 if lname not in PEOPLE and lname is not None:
  item = {
   "lname": lname,
   "fname": fname,
   "timestamp": get_timestamp(),
  }
  db.clientes.insert_one(item)
  return make_response(
   "{lname} criado com sucesso".format(lname=lname), 201
 )
 else:
  abort(
   406,
   "Pessoa com sobrenome {lname} ja existe".format(lname=lname),
  )
  
def update(lname, person):
 query = { "lname": lname }
 update = { "$set": {
 "lname": lname,
 "fname": person.get("fname"),
 "timestamp": get_timestamp(), }
  }
 PEOPLE = get_dict_from_mongodb()
 if lname in PEOPLE:
  db.clientes.update_one(query, update)
  PEOPLE = get_dict_from_mongodb()
  return PEOPLE[lname]
 else:
  abort(
   404, "Pessoa com sobrenome {lname} nao encontrada".format(lname=lname)
  )
  
def delete(lname):
 query = { "lname": lname }
 PEOPLE = get_dict_from_mongodb()
 if lname in PEOPLE:
  db.clientes.delete_one(query)
  return make_response(
   "{lname} deletado com sucesso".format(lname=lname), 200
  )
 else:
  abort(
   404, "Pessoa com sobrenome {lname} nao encontrada".format(lname=lname)
 )