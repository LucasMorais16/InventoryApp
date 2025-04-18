from flask import Flask, request, render_template_string
import auth

app = Flask(__name__)

@app.route('/verify_email')
def verify_email_ep():
    token = request.args.get('token', '')
    if auth.verify_email(token):
        return '<h2>Email confirmado!</h2><p>Agora você pode voltar ao app e fazer login.</p>'
    return '<h2>Link inválido ou expirado.</h2>'

@app.route('/reset_password', methods=['GET','POST'])
def reset_password_ep():
    token = request.args.get('token', '')
    if request.method == 'GET':
        return render_template_string('''
            <form method="post">
                <label>Nova senha:</label><br>
                <input type="password" name="password" /><br><br>
                <button type="submit">Salvar</button>
            </form>
        ''')
    new_pw = request.form.get('password','')
    if auth.reset_password(token, new_pw):
        return '<h2>Senha redefinida!</h2><p>Use a nova senha para entrar.</p>'
    return '<h2>Link inválido ou expirado.</h2>'

if __name__ == '__main__':
    app.run(debug=True)