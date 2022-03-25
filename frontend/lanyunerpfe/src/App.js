import React, { useEffect, useState } from 'react';
import be from './be';
const LOADING  = 0;
const NO_AUTH  = 1;
const LOGINED  = 2;
const REGISTER = 3;

function Header({loginState}) {
  return <div>{loginState}</div>
}

const e2value = (f) => { return (e) => f(e.target.value) }
const useInputState = (...val) => {
  const [v, setter] = useState(...val)
  return [v, e2value(setter)]
}
const Loading = ({setLoginState}) => {
  async function getPersonInfo() {
    const person_info = await be.get('/person_info');
    if(person_info.code === 0) {
      setLoginState(LOGINED)
    } else {
      setLoginState(NO_AUTH)
    }
  }
  useEffect(()=>{ getPersonInfo(); }, [])
  return <div>loading...</div>
}
const Login = ({setLoginState}) => {
  const [username, setUsername ] = useInputState('')
  const [password, setPassword ] = useInputState('')
  async function postAuthData() {
    const form = new FormData()
    form.append('username', username)
    form.append('password', password)
    const auth_res = await be.post('/login', form);
    if(auth_res.data.code === 0) {
      setLoginState(LOGINED)
    } else {
      setLoginState(NO_AUTH)
    }
  }
  const onSubmit = (e) => {
    e.preventDefault();
    postAuthData();
  }
  return <div>
    <form onSubmit={onSubmit} method="post" action="login">
      <input type="text" value={username} onChange={setUsername} />
      <input type="password" value={password} onChange={setPassword} />
      <input type="submit" value="登入" />
    </form>
    <input type="button" onClick={() => setLoginState(REGISTER)} value="註冊"/>
  </div>
}
const User = ({setLoginState}) => {
  return <div></div>
}
const Register = ({setLoginState}) => {
  const [username,   setUsername  ] = useInputState('')
  const [password,   setPassword  ] = useInputState('')
  const [email,      setEmail     ] = useInputState('')
  const [first_name, setFirstName ] = useInputState('')
  const [last_name,  setLastName  ] = useInputState('')
  const [sn,         setSN        ] = useInputState('')
  const [sArYear,    setsArYear   ] = useInputState('')
  async function postData() {
    const form = new FormData();
    form.append("username",   username,  )
    form.append("password",   password,  )
    form.append("email",      email,     )
    form.append("first_name", first_name,)
    form.append("last_name",  last_name, )
    form.append("sn",         sn,        )
    form.append("sArYear",    sArYear,   )
    const res = await be.post('/create_person', form);
    if(res.data.code === 0) {
      setLoginState(NO_AUTH)
    } else {
      // TODO: identify which field error
    }
  }
  const onSubmit = (e) => {
    e.preventDefault();
    postData();
  }
  return <div>
    <form onSubmit={onSubmit}>
      <input type="text"      value={username}   onChange={setUsername}  />
      <input type="password"  value={password}   onChange={setPassword}  />
      <input type="text"      value={email}      onChange={setEmail}     />
      <input type="text"      value={first_name} onChange={setFirstName} />
      <input type="text"      value={last_name}  onChange={setLastName}  />
      <input type="text"      value={sn}         onChange={setSN}        />
      <input type="text"      value={sArYear}    onChange={setsArYear}   />
      <input type="submit"    value="註冊" />
    </form>
  </div>
}
function App() {
  const [loginState, setLoginState] = useState(LOADING);
  const headerProps = {
    loginState
  }
  const loadingProps = {
    setLoginState
  }
  const loginProps = {
    setLoginState
  }
  const userProps = {}
  const registerProps = {
    setLoginState
  }
  return (
    <div className="App">
      <Header {...headerProps} />
      { loginState === LOADING  && <Loading {...loadingProps}/>}
      { loginState === NO_AUTH  && <Login {...loginProps}/>}
      { loginState === LOGINED  && <User {...userProps}/>}
      { loginState === REGISTER && <Register {...registerProps}/>}
    </div>
  );
}

export default App;
