import React from 'react'
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect
} from 'react-router-dom'
import MainContainer from '../main'
import Inside from '../inside'

const fakeAuth = {
  isAuthenticated: false,
  authenticate(cb) {
    this.isAuthenticated = true
    setTimeout(cb, 100) // fake async
  },
  signout(cb) {
    this.isAuthenticated = false
    setTimeout(cb, 100)
  }
}
class MainRouter extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      redirectToReferrer: false,
      redirectToHome: false,
      name: ''
    }
  }
  handleLogin = (rs, name) => {
    // redirect
    console.log('desde routes', rs, name)
    fakeAuth.authenticate(() => {
      console.log('fake auth', name)
      this.setState({ redirectToReferrer: true, redirectToHome: false, name: name })
    })
  }
  handleLogout = () => {
    fakeAuth.signout(() => {
      this.setState({ redirectToHome: true , redirectToReferrer: false})
    })
  }
  render(){
    const { from } = { from: { pathname: '/welcome' } }
    const from2 = { from: { pathname: '/' } }
    let rd = ''
    let rd2 = ''
    if (this.state.redirectToReferrer) {
      rd = <Redirect to={from}/>
    }
    if (this.state.redirectToHome) {
      rd2 = <Redirect to="/"/>
    }

    return (
      <Router>
        <div className='container' >
          <Route exact path="/" render={() => <MainContainer handleLogin={this.handleLogin}/>} />
          <Route path="/welcome" render={() => <Inside handleLogout={this.handleLogout} logged={fakeAuth.isAuthenticated} name={this.state.name}/>} />
          {rd}
          {rd2}
        </div>
      </Router>
    )
  }

}
export default MainRouter