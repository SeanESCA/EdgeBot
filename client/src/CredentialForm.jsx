function CredentialForm() {

    // onSubmit = e => {
    //     e.preventDetafult()
    // }

    return(
        <form method='POST' id='credential_form'>
            <h2>Credentials</h2>
            <p>If you have not signed up on the <a href="https://bath10.artifaxagora.com/room-bookings" target="_blank">Edge booking site</a>, please do so first.</p>
            <label for='username'>
                <h3>UoB Username</h3>
            </label>
            <input id="username" name='username' type='text' required />

            <label for='password'>
                <h3>Password</h3>
                <p>This password may be different from your UoB password. To check your password, try logging in to the <a href="https://bath10.artifaxagora.com/room-bookings" target="_blank">Edge booking site</a>.</p>
            </label>
            <input id="password" name='password' type='password' required />
            <input type='submit'/>
        </form>
    )
}

export default CredentialForm