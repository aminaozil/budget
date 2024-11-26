from flask import Flask, flash, redirect,render_template, request, url_for
from sqlalchemy import func
# Package Python pour l'interfaçage avec des bases de données
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'flash message'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost:3306/gestion_budget"
app.config['SQLALCHEMY_TRACK_MODICATIONS'] = False

#configuration SQLAlchemy la base de données et le nom de la bd est gestion_app
db = SQLAlchemy(app)

class Depense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre_depense = db.Column(db.String(100), nullable=False)
    montant_depense = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Gestion_budget: {self.titre_depense, self.montant_depense}"

#liste page index pour depense
@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)  # par defaut 1
    #variable depenses pour listes les depenses par ordre 
    depenses = Depense.query.order_by(Depense.titre_depense).paginate(page=page, per_page=5, error_out=False)
    page = request.args.get('page', 1, type=int)
    revenus = Revenu.query.order_by(Revenu.titre_revenu).paginate(page=page, per_page=5, error_out=False)
     #calcul de la somme des depenses on récupère tout les dep puis on util la fonc sum pour faire la somme 
    # et scalar() pour renvoyer une seule valeur
    total_deps = db.session.query(db.func.sum(Depense.montant_depense)).scalar()
    budget = db.session.query(db.func.sum(Revenu.montant_revenu)).scalar()
    solde = budget - total_deps

    return render_template("index.html",total_deps=total_deps, budget=budget, solde=solde, depenses=depenses, revenus=revenus, page=page)
    

@app.route("/depense")
def index_depense():
    
    page = request.args.get('page', 1, type=int)  # par defaut 1
    #variable depenses pour listes les depenses par ordre 
    depenses = Depense.query.order_by(Depense.titre_depense).paginate(page=page, per_page=5, error_out=False)
   
    return render_template("/depense/index_depense.html", depenses=depenses, page=page)

#create depense
@app.route("/create_dep", methods=["GET","POST"])
def create_dep():

    if request.method == "POST":
        titre_depense = request.form['titre_depense']
        montant_depense = request.form['montant_depense']
        dep = Depense(titre_depense=titre_depense,montant_depense=montant_depense)
        
        try:
            db.session.add(dep)
            db.session.commit()
            flash("Ajout fait avec success", "success")
            return redirect("/")
        except Exception:
            return "erreure "
    else:
        
        redirect("/")

    return render_template("/depense/create_depense.html")

#supprimer depense
@app.route("/delete_depense/<int:id>/")
def delete_depense(id):
    
    depenses = Depense.query.get_or_404(id)
    try:
        db.session.delete(depenses)
        db.session.commit()
        flash("La supression a reussi !!")
        return redirect("/")
    except Exception:
        
        print("une erreure s'est produite")

@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    depense = Depense.query.get_or_404(id)
    if request.method == "POST":
        depense.titre_depense = request.form['titre_depense']
        depense.montant_depense = request.form['montant_depense']
        
        try:
            db.session.commit()
            flash("La modification a reussi !!")
            return redirect("/")
        except Exception:
            print("erreur")
    
    return render_template("/depense/update.html", depense=depense)



#la classe revenu creation des tables
class Revenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre_revenu = db.Column(db.String(100), nullable=False)
    montant_revenu = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Gestion_budget: {self.titre_revenu, self.montant_revenu}"

#index revenu
@app.route("/revenu")
def index_revenu():
    page = request.args.get('page', 1, type=int)
    revenus = Revenu.query.order_by(Revenu.titre_revenu).paginate(page=page, per_page=5, error_out=False)

    return render_template("/revenu/index_revenu.html", revenus=revenus, page=page)

#supprimer revenu
@app.route("/delete_revenu/<int:id>/")
def delete_revenu(id):
    revenus = Revenu.query.get_or_404(id)
    try:    
        db.session.delete(revenus)
        db.session.commit()
        flash("Supression fait avec success", "success")
        return redirect("/")
    except Exception:
        print("invalid")

#ajouter revenu
@app.route("/create_revenu", methods=["GET", "POST"])
def create_revenu():
    if request.method == "POST":
        titre_revenu = request.form['titre_revenu']
        montant_revenu = request.form['montant_revenu']
        try:
            rev=Revenu(titre_revenu=titre_revenu, montant_revenu=montant_revenu)
            db.session.add(rev)
            db.session.commit()
            flash("Ajout fait avec success", "success")
            return redirect("/")
        except Exception:
            print("une s'est produite")
        
    return render_template("/revenu/create_revenu.html")
# modifier revenu
@app.route("/update_revenu/<int:id>/", methods=["GET", "POST"])
def update_revenu(id):
    revenu = Revenu.query.get_or_404(id)
    if request.method == "POST":
        revenu.titre_revenu = request.form['titre_revenu']
        revenu.montant_revenu = request.form['montant_revenu']
        try:
            db.session.commit()
            flash("Modification fait avec success", "success")
            return redirect("/")
        except Exception:
            print("erreur est pro")
    return render_template("/revenu/update_revenu.html", revenu=revenu)

if __name__ == "__main__":
    app.run(debug=True)