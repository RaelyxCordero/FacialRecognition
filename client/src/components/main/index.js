import React, { Component } from 'react';
import { Container, Grid, TransitionablePortal } from 'semantic-ui-react'
import VideoSignUp from '../video-signup';
import VideoSignIn from '../video-signin';
import MenuPrincipal from '../menu';
import RegForm from '../registro';
import Info from '../info';

class MainContainer extends Component {
  constructor(props){
    super(props);
    this.handleMenuClick = this.handleMenuClick.bind(this);
    this.state = { 
      activeItem: 'home',
      name: '',
      uid: ''
     };
  }
  handleMenuClick = (activeItem) => {
    this.setState({activeItem: activeItem});
  }
  handleDataUser = (uid) => {
    console.log(uid, typeof(uid))
    this.setState({uid: uid})
    this.handleMenuClick('signup_next')
  }
  handleLogin = (rs, name) =>{
    console.log(rs)
    this.props.handleLogin(rs, name)
  }

  render() {
    var segment = ''
    var pro = ''
    switch(this.state.activeItem){
      case 'signin':
        segment = <VideoSignIn handleLogin={this.handleLogin}/>
        break;
      case 'signup':
        segment = <RegForm handleMenuClick={this.handleMenuClick} handleDataUser={this.handleDataUser} />
        break;
      case 'signup_next':
        segment = <VideoSignUp uid={this.state.uid} handleReg={this.handleMenuClick}/>
        break;
      case 'home':
        segment = <Info />
        break;
    }
    return (
        <Container style={{background: 'none'}} location={this.props.location}>
          <Grid columns={2} divided>
            <Grid.Row>
              <Grid.Column width={12}>
                {segment}
              </Grid.Column>
              <Grid.Column width={1}>
                <MenuPrincipal handleMenuClick={this.handleMenuClick}/>
              </Grid.Column>
            </Grid.Row>
          </Grid>
        </Container>
    )
  }
}

export default MainContainer;

