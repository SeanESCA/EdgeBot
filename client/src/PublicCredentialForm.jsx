import {useState} from 'react'


function PublicCredentialForm() {

    const [isUobEmail, setIsUobEmail] = useState(true)

    return(
        <form method='POST' id='credential_form'>
            <label for='email'>
                <h3>Email</h3>
                <p>Which email did you use to sign up to the <a href='https://bath10.artifaxagora.com/room-bookings'>Edge booking site</a>?</p>
                <p>If you have not signed up with them, please do so first.</p>
            </label>
            <input name='is_uob_email' type='radio' onClick={() => setIsUobEmail(true)} checked={isUobEmail} />
            <label for='uob_username'>My UoB email</label>

            <input name='is_uob_email' type='radio' onClick={() => setIsUobEmail(false)}/>
            <label for='email'>Another email </label>

            { isUobEmail ? (
                <div>
                    <h4>UoB Username</h4>
                    <input id="username" name='username' type='text' required />
                </div>) : (
                <input id="email" name='email' placeholder='Does_Not_End_With@bath.ac.uk' type='email' required />
                )
            }

            <label for='password'>
                <h3>Password</h3>
            </label>
            <input id="password" name='password' type='password' required />
            <input type='submit'/>
        </form>
    )
}

export default PublicCredentialForm