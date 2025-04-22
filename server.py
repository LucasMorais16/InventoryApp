from flask import Flask, request, render_template_string
import auth

app = Flask(__name__)

@app.route('/verify_email')
def verify_email_ep():
    token = request.args.get('token', '')
    if auth.verify_email(token):
        return '<h2>Email confirmed!</h2><p>You can now return to the app and log in.</p>'
    return '<h2>Invalid or expired link.</h2>'

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_ep():
    token = request.args.get('token', '')
    if request.method == 'GET':
        return render_template_string('''
            <form method="post">
                <label>New password:</label><br>
                <input type="password" name="password" /><br><br>
                <button type="submit">Save</button>
            </form>
        ''')
    new_pw = request.form.get('password', '')
    if auth.reset_password(token, new_pw):
        return '<h2>Password reset!</h2><p>Use the new password to log in.</p>'
    return '<h2>Invalid or expired link.</h2>'

if __name__ == '__main__':
    app.run(debug=True)
