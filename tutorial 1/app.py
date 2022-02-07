from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db=SQLAlchemy(app)
api=Api(app)
ma=Marshmallow(app)



class Publicacion(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    titulo = db.Column( db.String(50))
    contenido = db.Column( db.String(255))

class PublicacionSchema(ma.Schema):
    class Meta:
        fields=('id','titulo','contenido')

publicacion_schema=PublicacionSchema()
publicaciones_schema=PublicacionSchema(many=True)

class PublicacionesResource(Resource):
    def get(self):
        publicaciones=Publicacion.query.all()
        return publicaciones_schema.dump(publicaciones)
    def post(self):
        new_publicacion=Publicacion(titulo=request.json["titulo"],contenido=request.json["contenido"])
        db.session.add(new_publicacion)
        db.session.commit()
        return publicacion_schema.dump(new_publicacion)
class PublicacionResource(Resource):
    def get(self,id):
        publicacion=Publicacion.query.get_or_404(id)
        return publicacion_schema.dump(publicacion)
    def put(self,id):
        publicacion=Publicacion.query.get_or_404(id)
        publicacion.titulo=request.json["titulo"]
        publicacion.contenido=request.json["contenido"]
        db.session.commit()
        return publicacion_schema.dump(publicacion)
    def delete(self,id):
        publicacion=Publicacion.query.get_or_404(id)
        db.session.delete(publicacion)
        db.commit()
        return publicacion_schema.dump(publicacion)

@app.before_request
def create_tables():
    db.create_all()

api.add_resource(PublicacionesResource,'/publicaciones')
api.add_resource(PublicacionResource,'/publicaciones/<int:id>')

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')