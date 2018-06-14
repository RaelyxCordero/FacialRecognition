import React, { Component } from 'react';
import { Button, Container } from 'semantic-ui-react';

export default class Inside extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			name: this.props.name
		}
	}
  render(){
    let draw = ''
    if(this.props.logged){
      draw = <p>Bienvenido {this.state.name}!<br /><Button id="sign_out" content='Salir' onClick={this.props.handleLogout.bind(this)} /></p>
    }
    else{
      draw = <p>No estas autenticado.</p>
    }
    return(
        <Container style={{background: 'none'}}>
          {/*<h3>Protected</h3>*/}
          {draw}
        </Container>
    )
  }
}