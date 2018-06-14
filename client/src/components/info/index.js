import React, { Component } from 'react'
import { Container, Segment } from 'semantic-ui-react'

export default class Info extends Component {
  state = { activeItem: '', count: 0 }

  handleItemClick = (e, { name }) => this.setState({ activeItem: name })
  componentWillMount(){
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/count')
    xhr.onreadystatechange = () => {
      if(xhr.readyState == 4) {
        if(xhr.status == 200){
          let rs = JSON.parse(xhr.responseText);
          console.log(rs)
          this.setState({count: rs.count})
        }
      }
    }
    xhr.send();
  }
  render() {
    const { activeItem } = this.state

    return (
      <Container style={{background: 'none'}} textAlign='right'>
        <Segment as='h1' className='headerT' style={{background: 'none'}} textAlign='right'>
          {this.state.count} usuarios registrados.
        </Segment>
        <Segment.Group>
          <Segment  inverted as='h3' className='headerT' style={{background: 'none'}}>
              Modulo de autenticación y registro de usuarios
          </Segment>
          <Segment inverted style={{background: 'none', fontWeight: 'normal', fontSize: '1em'}}>
              <h4>Prototipo realizado para optar por el título de </h4>
              <h5>Ingeniero en Informática</h5>
          </Segment>
        </Segment.Group>
      </Container>
    )
  }
}