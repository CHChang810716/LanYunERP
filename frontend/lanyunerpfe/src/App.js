import React, { useEffect, useState } from 'react';
import be from 'be';
const LOADING = 0;
const NO_AUTH = 1;
const LOGINED = 2;

function Header({loginState}) {
  return <div>{loginState}</div>
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
  const [username, setUsername] = useState('')
  const [passwd, setPasswd] = useState('')
  async function postAuthData() {
    const auth_res = await be.post('/login', {
      'username': username,
      'password': passwd
    });
    if(auth_res.code === 0) {
      setLoginState(LOGINED)
    } else {
      setLoginState(NO_AUTH)
    }
  }
  const onSubmit = () => {
    postAuthData();
  }
  return <div>
    <form onSubmit={onSubmit}>
      <input type="text" value={username} onChange={setUsername} />
      <input type="text" value={passwd} onChange={setPasswd} />
      <input type="submit" value="Submit" />
    </form>
  </div>
}
const User = ({setLoginState}) => {
  return <div></div>
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
  return (
    <div className="App">
      <Header {...headerProps} />
      { loginState === LOADING && <Loading {...loadingProps}/>}
      { loginState === NO_AUTH && <Login {...loginProps}/>}
      { loginState === LOGINED && <User {...userProps}/>}
    </div>
  );
}

export default App;
