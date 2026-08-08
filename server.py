from flask import Flask, flash, redirect, render_template_string, request, session, url_for

# On dit à Flask de chercher les fichiers HTML dans le même dossier (.)
app = Flask(__name__, template_folder='.')
app.secret_key = 'super_secret_key_rp_animateurs'

# Données simulées (stockées en mémoire)
site_data = {
    'annonces': 'Bienvenue sur le site officiel des animateurs RP !',
    'recrutement_ouvert': True
}

@app.route('/')
def index():
    # Lit le contenu du fichier index.html et injecte les données dynamiques
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content, data=site_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'gazpartoutetjuleslesbg':
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('Mot de passe incorrect !')
    
    # Page de connexion intégrée rapidement
    return '''
        <h2>Accès Administrateur</h2>
        <form method="POST">
            <input type="password" name="password" placeholder="Mot de passe">
            <button type="submit">Valider</button>
        </form>
        <p><a href="/">Retour à l'accueil</a></p>
    '''

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        site_data['annonces'] = request.form.get('annonce')
        site_data['recrutement_ouvert'] = 'recrutement' in request.form
        return redirect(url_for('admin'))
        
    # Panneau admin intégré
    return f'''
        <h2>Panneau Administrateur - Animateurs RP</h2>
        <form method="POST">
            <textarea name="annonce" rows="4" cols="50">{site_data['annonces']}</textarea><br><br>
            <label>
                <input type="checkbox" name="recrutement" {"checked" if site_data["recrutement_ouvert"] else ""}> 
                Recrutement Ouvert
            </label><br><br>
            <button type="submit">Mettre à jour le site</button>
        </form>
        <br>
        <p><a href="/">Voir le site public</a> | <a href="/logout">Se déconnecter</a></p>
    '''

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)